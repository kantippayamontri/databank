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
        custom_port = 80  # Replace with your desired port
        new_url = f"{request.scheme}://{request.host.split(':')[0]}:{custom_port}{request.path}"
        return redirect(new_url)
    if cookie_value not in session.keys():
        session[cookie_value] = {}
    return redirect('/')


