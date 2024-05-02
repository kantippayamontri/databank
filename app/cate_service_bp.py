from flask import (
    Blueprint,
    jsonify,
    redirect,
    render_template,
    request,
    session,
    url_for,
)

from .utils import cate_service, frequency, service_action

bp = Blueprint("cate_service", __name__, "/cate_service")


@bp.route("/form", methods=["GET", "POST"])
def form():

    if request.method == "POST":

        _unprocessed = request.form["cate_service_unprocessed"]
        _frequency = request.form["cate_service_frequency"]
        _action = request.form["cate_service_action"]
        _cate = request.form["cate_service_cate"]

        print(f"cate from form : {_cate}")

        # record the cate_service data
        if "cate_service" not in session.keys():
            session["cate_service"] = {}

        session["cate_service"][_unprocessed] = {
            "action": _action,
            "frequency": _frequency,
            "category": _cate,
        }

        return redirect(url_for("main_page"))

    if request.method == "GET":

        # choose_action = ""
        # choose_frequency = ""
        unprocessed_data = []

        # find cate_service in session
        # if "cate_service" in session.keys():
        #     choose_action = session["cate_service"]["action"]
        #     choose_frequency = session["cate_service"]["frequency"]

        if "raw_data" in session.keys():
            if len(session["raw_data"].keys()) > 0:
                unprocessed_data = session["raw_data"].keys()

        return render_template(
            "forms/cate_service_form.html",
            frequency=frequency,
            action=service_action,
            unprocessed_data=unprocessed_data,
            cate_service=cate_service,
            # choose_action=choose_action,
            # choose_frequency=choose_frequency,
        )

    return "Service Form Page"


@bp.route("/forms/<unprocessed>", methods=["GET", "POST"])
def form_edit(unprocessed):
    print(f"form_edit")

    unprocessed_data = []

    if "raw_data" in session.keys():
        if len(session["raw_data"].keys()) > 0:
            unprocessed_data = session["raw_data"].keys()
    
    choose_data = {"data" : {
        "unprocessed_data" : unprocessed,
        "action" : session["cate_service"][unprocessed]['action'],
        "frequency" : session["cate_service"][unprocessed]['frequency'],
        "category" : session["cate_service"][unprocessed]['category'],
    }}

    print(f"choose_data : {choose_data}")
    
    return render_template(
        "forms/cate_service_form.html",
        frequency=frequency,
        action=service_action,
        unprocessed_data=unprocessed_data,
        cate_service=cate_service,
        choose_data=choose_data
    )


@bp.route("/delete", methods=["GET"])
def delete():
    if "cate_service" in session.keys():
        del session["cate_service"]

    return redirect(url_for("main_page"))

@bp.route("/delete_unprocessed/<unprocessed>", methods=["GET"])
def delete_unprocessed(unprocessed):
    if "cate_service" in session.keys():
        if unprocessed in session["cate_service"].keys():
            del session["cate_service"][unprocessed]
    return redirect(url_for("main_page"))