from flask import (
    Blueprint,
    jsonify,
    redirect,
    render_template,
    request,
    session,
    url_for,
)

from .utils.constants import type_device, type_device_details, unprocessed_data

bp = Blueprint("user_select", __name__, url_prefix="/users")

@bp.route("/", methods=["GET"])
def form():
    return render_template(
        "user_select.html",
    )
@bp.route("/get", methods=["GET"])
def get():
    cookie_value = request.cookies.get('user')
    if(cookie_value == None):
        return render_template("user_select.html",user="not-show-path")
    if cookie_value not in session.keys():
        session[cookie_value] = {}
    return redirect('/')


