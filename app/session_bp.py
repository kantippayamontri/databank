from flask import (
    Blueprint,
    session,
    jsonify,
    redirect,
    url_for,
)


bp = Blueprint("session", __name__, url_prefix="/session")

@bp.route("/get", methods=["GET"])
def get():
    resp = {}

    for key in session.keys():
        resp[key] = session[key]

    resp = jsonify(resp)
    resp.status_code = 200

    return resp

@bp.route("/clear", methods=["GET"])
def clear():
    session.clear()
    return "clear session success"

@bp.route("/clear_service", methods=["GET"])
def clear_service():
    if "services" in session.keys():
        del session["services"]
    
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
    _session_key = list(session.keys())
    for k in _session_key:
        del session[k]
    
    return redirect(url_for("main_page"))
    