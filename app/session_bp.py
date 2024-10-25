from flask import (
    Blueprint,
    session,
    jsonify,
    redirect,
    url_for,
    request,
)
import socket


bp = Blueprint("session", __name__, url_prefix="/session")

@bp.route("/get", methods=["GET"])
def get():
    resp = {}
    cookie_value = request.cookies.get('user')
    for key in session[cookie_value].keys():
        resp[key] = session[cookie_value][key]
    resp = jsonify(resp)
    resp.status_code = 200

    return resp
@bp.route("/setDone", methods=["POST"])
def setDone():
    resp = {}
    cookie_value = request.cookies.get('user')
    for key in session[cookie_value].keys():
        if(key=="tour"):
            session[cookie_value][key] = 0
        resp[key] = session[cookie_value][key]
    resp = jsonify(resp)
    resp.status_code = 200
    return resp
@bp.route("/clear", methods=["GET"])
def clear():
    cookie_value = request.cookies.get('user')
    session[cookie_value].clear()
    return "clear session success"

@bp.route("/clear_service", methods=["GET"])
def clear_service():
    cookie_value = request.cookies.get('user')
    if "services" in session[cookie_value].keys():
        del session[cookie_value]["services"]
    return "clear services success"

# @bp.route("/clear_device", methods=["GET"])
# def clear_device():
#     if "device" in session.keys():
#         del session['device']
    
#     if "raw_data" in session.keys():
#         del session["raw_data"]
    
#     return "clear service session success"

@bp.route("/clear_session", methods=["GET"])
def clear_session():
    cookie_value = request.cookies.get('user')
    _session_key = list(session[cookie_value].keys())
    for k in _session_key:
        del session[cookie_value][k]
    
    return redirect(url_for("main_page"))
    
@bp.route("/hostname", methods=["GET"])
def hostname():
    return {"hostname": socket.gethostname()}

@bp.route("/alert/toturial", methods=["GET"])
def toturial():
    users = ['User1','User2','User3','User4']
    cookie_value = request.cookies.get('user')
    if "tour" in session[cookie_value]:
        if session[cookie_value]['tour'] == 0:
            return '2'
    for user in users:
        if user != cookie_value:
            if user in session.keys():
                if session[user]['tour'] == 0:
                    return '1'
    return ''