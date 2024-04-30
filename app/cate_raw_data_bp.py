from flask import (
    Blueprint,
    jsonify,
    redirect,
    render_template,
    request,
    session,
    url_for,
)

from .utils import frequency, raw_data_action

bp = Blueprint("raw_data", __name__, url_prefix="/raw_data")


@bp.route("/get", methods=["GET"])
def get():
    return "get raw_data"


@bp.route("/form", methods=["GET", "POST"])
def form():
    if request.method == "POST":
        _frequency = request.form["raw_data_frequency"]
        _action = request.form["raw_data_action"]

        # record the raw_data data
        session["raw_data"] = {"action": _action, "frequency": _frequency}

        return redirect(url_for("main_page"))

    if request.method == "GET":

        choose_action = ""
        choose_frequency = ""

        # find raw_data in session
        if "raw_data" in session.keys():
            choose_action = session["raw_data"]["action"]
            choose_frequency = session["raw_data"]["frequency"]

        return render_template(
            "forms/raw_data_form.html",
            frequency=frequency,
            action=raw_data_action,
            choose_action=choose_action,
            choose_frequency=choose_frequency,
        )

    return "Cate Raw Data Form"


@bp.route("/delete", methods=["GET"])
def delete():
    if "raw_data" in session.keys():
        del session["raw_data"]
    return redirect(url_for("main_page"))
