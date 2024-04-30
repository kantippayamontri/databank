from flask import Blueprint, redirect, render_template, request, session, url_for, jsonify

from .utils import frequency, service_action

bp = Blueprint("cate_service", __name__, "/cate_service")


@bp.route("/form", methods=["GET", "POST"])
def form():

    if request.method == "POST":

        _frequency = request.form["cate_service_frequency"]
        _action = request.form["cate_service_action"]

        # record the cate_service data
        session["cate_service"] = {"action": _action, "frequency": _frequency}

        return redirect(url_for("main_page"))

    if request.method == "GET":

        choose_action = ""
        choose_frequency = ""

        # find cate_service in session
        if "cate_service" in session.keys():
            choose_action = session["cate_service"]["action"]
            choose_frequency = session["cate_service"]["frequency"]

        return render_template(
            "forms/cate_service_form.html",
            frequency=frequency,
            action=service_action,
            choose_action=choose_action,
            choose_frequency=choose_frequency,
        )

    return "Service Form Page"

@bp.route("/delete", methods=["GET"])
def delete():
    if "cate_service" in session.keys():
        del session["cate_service"]

    return redirect(url_for("main_page"))
