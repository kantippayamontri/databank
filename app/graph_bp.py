import random
import string
from pathlib import Path
from flask import request

import graphviz
from flask import (
    Flask,
    Blueprint,
    jsonify,
    redirect,
    render_template,
    request,
    session,
    url_for
)
import plotly.graph_objs as go
import plotly.io as pio
from PIL import Image
from icecream import ic

# TODO: making graph
# from dash import Dash, html, Input, Output, callback, no_update
# import dash_cytoscape as cyto

bp = Blueprint("graph", __name__, url_prefix="/graph")
# app_dash = Dash(__name__)
# app_dash.layout = html.Div("Hello from Dash!")

@bp.route("/show_graph", methods=["GET"])
def show_graph():
    cookie_value = session.get('user_id')
    # ip = request.headers.get("X-Forwarded-For", request.remote_addr)
    try:
        if(cookie_value == None):
            return redirect('/')
        # if "devices" in session[cookie_value].keys():
        #     return render_template("show_graph.html",devices=session[cookie_value]["devices"],session=session[cookie_value],id=cookie_value)
        return render_template("show_graph.html",id=cookie_value)
    except Exception as e:
        return render_template("user_select.html",user="not-show-path")
