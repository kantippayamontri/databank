import secrets

import matplotlib.pyplot as plt
from flask import Flask, jsonify, redirect, render_template, request, session, url_for
from flask_bootstrap import Bootstrap5
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

from .utils import *

def create_app():
    app = Flask(
        __name__,
    )

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
    # # Bootstrap-Flask requires this line
    # bootstrap = Bootstrap5(app)
    # # Flask-WTF requires this line
    # csrf = CSRFProtect(app)

    @app.route("/", methods=["POST", "GET"])
    def main_page():
        if request.method == "GET":
            cookie_value = request.cookies.get('user')
            try:
                if cookie_value == None:
                    return render_template("user_select.html",user="not-show-path")
                if 'tour' not in session[cookie_value].keys():
                    session[cookie_value]['tour']=1
                if "graph_filename" in request.args.keys():
                    return render_template("index.html", graph_filename=request.args.get("graph_filename"),name=cookie_value)
                return render_template(
                    "index.html",
                    name=cookie_value
                )
            except Exception as e:
                return render_template("user_select.html",user="not-show-path")
    return app