from flask import (
    Blueprint,
    session,
    jsonify
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
    if 'service' in session.keys():
        del session['service']
    
    if 'cate_service' in session.keys():
        del session["cate_service"]

    return "clear service session success"

@bp.route("/clear_device", methods=["GET"])
def clear_device():
    if "device" in session.keys():
        del session['device']
    
    if "raw_data" in session.keys():
        del session["raw_data"]
    
    return "clear service session success"