import secrets
import matplotlib.pyplot as plt
from flask import Flask, jsonify, redirect, render_template, request, session, url_for, make_response
from flask_bootstrap import Bootstrap
from flask_wtf import CSRFProtect, FlaskForm
from icecream import ic
from wtforms.validators import DataRequired, Length
from flask_session import Session
from flask import (
    session,
)
from dash import Dash, html
import socket

from .forms import DeviceForm
from flask import request
from .utils import *
from flask_sqlalchemy import SQLAlchemy
from collections import defaultdict
from sqlalchemy import text
db = SQLAlchemy()
def create_app():
    app = Flask(
        __name__,
    )
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://culprit_lab:-6?j2+M63h??@147.79.70.44/databank'
    # app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root@127.0.0.1/databank'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)

    app.config["SESSION_PERMANENT"] = False
    app.config["SESSION_TYPE"] = "filesystem"
    Session(app)
    
    app.secret_key = secrets.token_urlsafe(16)

    from . import device
    app.register_blueprint(device.bp) # register device blueprint

    from . import session_bp
    app.register_blueprint(session_bp.bp) # register session blueprint

    from . import cate_raw_data_bp 
    app.register_blueprint(cate_raw_data_bp.bp) # register cate and action raw data blueprint

    from . import cate_service_bp
    app.register_blueprint(cate_service_bp.bp) # register cate and action service blueprint
    
    from . import service_bp
    app.register_blueprint(service_bp.bp) # register service blueprint

    from . import graph_bp
    app.register_blueprint(graph_bp.bp) # register graph blueprint

    from . import filter_data_bp
    app.register_blueprint(filter_data_bp.bp) # register filter blueprint

    from . import user_select_bp
    app.register_blueprint(user_select_bp.bp) # register filter blueprint

    from . import category
    app.register_blueprint(category.bp) # register filter blueprint

    from . import help
    app.register_blueprint(help.bp) # register filter blueprint
    # from . import category
    # app.register_blueprint(category.bp) # register filter blueprint
    # # Bootstrap-Flask requires this line
    # bootstrap = Bootstrap5(app)
    # # Flask-WTF requires this line
    # csrf = CSRFProtect(app)

    @app.route("/", methods=["POST", "GET"])
    def main_page():
        if request.method == "GET":
            # cookie_value = request.cookies.get('user')
            try:
                # if cookie_value == None:
                #     return render_template("user_select.html",user="not-show-path")
                # if 'tour' not in session[cookie_value].keys():
                #     session[cookie_value]['tour']=1
                if "graph_filename" in request.args.keys():
                    return render_template("index.html", graph_filename=request.args.get("graph_filename"),name=cookie_value)
                result = db.session.execute(text("SELECT devices.*,device_types.name as type_name FROM devices left join device_types on device_types.id=devices.device_type_id order by id desc"))
                devices = result.fetchall()
                result_type = db.session.execute(text("SELECT * FROM device_types order by id desc"))
                device_type = result_type.fetchall()
                result_data = db.session.execute(text("SELECT * FROM device_datas order by id desc"))
                device_data = result_data.fetchall()
                grouped_data = defaultdict(list)
                for item in device_data:
                    grouped_data[item[1]].append(item)

                result = db.session.execute(text("SELECT services.* FROM services order by id desc"))
                services = result.fetchall()
                ip = request.headers.get("X-Forwarded-For", request.remote_addr)
                result = db.session.execute(text("SELECT users.* FROM users where name='"+ip+"'"))
                user = result.fetchall()
                response = make_response("User cookie has been set!")
                if len(user) == 0:
                    sql = text("""
                        INSERT INTO users (name)
                        VALUES (:ip)
                    """)
                    result = db.session.execute(sql, {'ip': ip})
                    db.session.commit()
                    session['user_id'] = result.lastrowid
                else:
                    session['user_id'] = user[0][0]
                cookie_value = session.get('user_id')
                return render_template(
                    "index.html",
                    name=cookie_value,
                    device_type=device_type,
                    unprocessed_data=grouped_data,
                    devices=enumerate(devices),
                    device_count=len(devices),
                    device_name=devices,
                    services=services,
                    service_count=len(services)
                )
            except Exception as e:
                print(f"Error occurred: {e}")
                return f"Error occurred: {e}"
                # return render_template("user_select.html",user="not-show-path")
    return app