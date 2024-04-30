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
