from flask import Blueprint, jsonify, redirect, render_template, request, session, url_for, flash

from .utils import service_type


bp = Blueprint("service", __name__, url_prefix="/service")

@bp.route("/service_page", methods=["GET"])
def service_page():
    choose_service_name = ""
    choose_service_type = ""
    service_id = 0
    service_name_all = []
    
    if "services" in session.keys():
        service_id_max = max(list([int(k) for k in session["services"].keys()]))
        service_id = service_id_max + 1

        # check service name is redundant
        service_name_all = list(
            [
                session["services"][_service_id]["service_name"]
                for _service_id in session["services"].keys()
                if _service_id != service_id
            ]
        )
    if "devices" in session.keys():
        return render_template("service_page.html",
            service_name_all=service_name_all,
            service_id=str(service_id),
            service_type=service_type,
            device=session["devices"],
            choose_service_name=choose_service_name,
            choose_service_type=choose_service_type)
    else:
        return render_template("service_page.html",
            service_name_all=service_name_all,
            service_id=str(service_id),
            service_type=service_type,
            device=[],
            choose_service_name=choose_service_name,
            choose_service_type=choose_service_type)

# @bp.route("/get_data", methods=["GET"])
# def get_data():

@bp.route("/form_submit/<int:service_id>", methods=["GET", "POST"])
def form_submit(service_id):

    if request.method == "POST":
        service_id = str(service_id)
        _service_name = request.form["service_name"]
        _service_type = request.form["service_type"]
        if "services" not in session.keys():
            session["services"] = {}

        # session["services"][service_id] = {
        #     "service_name": _service_name,
        #     "service_type": _service_type,
        # }
        if service_id not in session.get("services").keys():
            session["services"][service_id] = {}
            # check service is redundant
        for _service_id in session.get("services").keys():
            if _service_id == service_id:
                continue
            if "service_name" in session.get("services")[service_id].keys():
                if (
                    _service_name
                    == session.get("services")[_service_id]["service_name"]
                ):
                    _service_name = f"{_service_name}_(1)"

        session["services"][service_id]["service_name"] = _service_name
        session["services"][service_id]["service_type"] = _service_type

        return redirect(url_for("service.service_page"))

    return "Service Form Page"

@bp.route("/form_edit/<int:service_id>", methods=["GET", "POST"])
def form_edit(service_id):

    if request.method == "POST":
        service_id = str(service_id)
        _service_name = request.get_json()["service_name"]
        _service_type = request.get_json()["service_type"]
        if "services" not in session.keys():
            session["services"] = {}
        if service_id not in session.get("services").keys():
            session["services"][service_id] = {}
        for _service_id in session.get("services").keys():
            if _service_id == service_id:
                continue
            if "service_name" in session.get("services")[service_id].keys():
                if (
                    _service_name
                    == session.get("services")[_service_id]["service_name"]
                ):
                    _service_name = f"{_service_name}_(1)"

        session["services"][service_id]["service_name"] = _service_name
        session["services"][service_id]["service_type"] = _service_type
        return jsonify(success=True)
    return "Service Form Page"

@bp.route("/form_add", methods=["POST"])
def form_add():
    _service_name = request.form["service_name"]
    _service_type = request.form["service_type"]

    if "services" not in session.keys():
        session["services"] = {"0": {"service_name":_service_name,"service_type":_service_type}}
    else:
        # add new service
        service_id_new_service = (
            max(list([int(service_id) for service_id in session["services"].keys()]))
            + 1
        )
        session["services"][str(service_id_new_service)] = {"service_name":_service_name,"service_type":_service_type}
    if(request.form["isTour"]== "1"):
        return redirect(url_for("service.service_page")+"?to=18")
    else:
        return redirect(url_for("service.service_page"))

@bp.route("/form_page_new", methods=["GET"])
def form_page_new():

    choose_service_name = ""
    choose_service_type = ""
    service_id = 0
    service_name_all = []

    if "services" in session.keys():
        service_id_max = max(list([int(k) for k in session["services"].keys()]))
        service_id = service_id_max + 1

        # check service name is redundant
        service_name_all = list(
            [
                session["services"][_service_id]["service_name"]
                for _service_id in session["services"].keys()
                if _service_id != service_id
            ]
        )

    return render_template(
        "forms/service_form.html",
        service_name_all=service_name_all,
        service_id=str(service_id),
        service_type=service_type,
        choose_service_name=choose_service_name,
        choose_service_type=choose_service_type,
    )


@bp.route("/form_page/<int:service_id>", methods=["GET"])
def form_page(service_id):
    # if "services" not in session.keys():
    #     return render_template("index.html")

    service_id = str(service_id)

    choose_service_type = ""
    choose_service_name = ""

    if "services" in session.keys():
        if str(service_id) in session["services"].keys():

            choose_service_type = session["services"][str(service_id)]["service_type"]
            choose_service_name = session["services"][str(service_id)]["service_name"]

            return render_template(
                "forms/service_form.html",
                service_id=str(service_id),
                service_type=service_type,
                choose_service_name=choose_service_name,
                choose_service_type=choose_service_type,
            )
    else:
        return redirect(url_for("service.service_page"))


@bp.route("/delete/<string:service_id>", methods=["GET"])
def delete(service_id: str):
    if "services" in session.keys():
        del session["services"][service_id]

        if session["services"] == {}:
            del session["services"]

    return redirect(url_for("service.service_page"))
