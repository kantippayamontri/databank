from flask import Blueprint, redirect, render_template, request, session, url_for, flash

from .utils import service_type

bp = Blueprint("service", __name__, url_prefix="/service")


@bp.route("/form", methods=["GET", "POST"])
def form():
    choose_service_type = ""
    choose_service_name = ""

    if request.method == "POST":
        

        _service_name = request.form["service_name"]
        _service_type = request.form["service_type"]

        session["service"] = {
            "service_name": _service_name,
            "service_type": _service_type,
        }

        return redirect(url_for("main_page"))

    if request.method == "GET":

        if "device" not in session.keys():
            return render_template("index.html")

        if "service" in session.keys():
            choose_service_type = session["service"]["service_type"]
            choose_service_name = session["service"]["service_name"]

        return render_template(
            "forms/service_form.html",
            service_type=service_type,
            choose_service_name=choose_service_name,
            choose_service_type=choose_service_type,
        )

    return "Service Form Page"


@bp.route("/delete", methods=["GET"])
def delete():
    if "service" in session.keys():
        del session["service"]
    return redirect(url_for("main_page"))
