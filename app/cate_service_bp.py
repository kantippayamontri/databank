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


@bp.route("/form/<int:service_id>/<int:device_id>", methods=["GET", "POST"])
def form(service_id: int, device_id: int):
    service_id = str(service_id)
    device_id = str(device_id)

    if request.method == "POST":

        _unprocessed = request.form["cate_service_unprocessed"]
        _frequency = request.form["cate_service_frequency"]
        _action = request.form["cate_service_action"]
        _cate = request.form["cate_service_cate"]

        # print(f"cate from form : {_cate}")

        # record the cate_service data
        if "cate_service" not in session["services"][service_id].keys():
            session["services"][service_id]["cate_service"] = {}

        if device_id not in session["services"][service_id]["cate_service"].keys():
            session["services"][service_id]["cate_service"][device_id] = {}

        session["services"][service_id]["cate_service"][device_id][_unprocessed] = {
            "action": _action,
            "frequency": _frequency,
            "category": _cate,
        }

        return redirect(url_for("main_page"))

    if request.method == "GET":

        unprocessed_data = []

        if "raw_data" in session["devices"][device_id].keys():
            if len(session["devices"][device_id]["raw_data"].keys()) > 0:
                unprocessed_data = session["devices"][device_id]["raw_data"].keys()

        return render_template(
            "forms/cate_service_form.html",
            device_id=device_id,
            service_id=service_id,
            frequency=frequency,
            action=service_action,
            unprocessed_data=unprocessed_data,
            cate_service=cate_service,
        )

    return "Service Form Page"

@bp.route("/ajax/<int:service_id>/<int:device_id>", methods=["GET"])
def ajax(service_id: int, device_id: int):
    service_id = str(service_id)
    device_id = str(device_id)

    unprocessed_data = []

    if "raw_data" in session["devices"][device_id].keys():
        if len(session["devices"][device_id]["raw_data"].keys()) > 0:
            unprocessed_data = session["devices"][device_id]["raw_data"].keys()
    return{
        "device_id":device_id,
        "service_id":service_id,
        "frequency":frequency,
        "action":service_action,
        "unprocessed_data":unprocessed_data,
        "cate_service":cate_service
    }

@bp.route("/ajaxEdit/<int:service_id>/<int:device_id>", methods=["post"])
def ajaxEdit(service_id: int, device_id: int):
    cookie_value = request.cookies.get('user')
    service_id = str(service_id)
    device_id = str(device_id)
    cat_data = request.form['cat_data']
    data = session[cookie_value]["services"][service_id]['cate_service'][device_id][cat_data]
    data['action'] = request.form['action']
    data['frequency'] = request.form['frequency']
    data['category'] = request.form['category']
    return jsonify(success=True)

@bp.route("/ajaxData", methods=["GET"])
def ajaxData():
    return{
        "frequency":frequency,
        "action":service_action,
        "cate_service":cate_service
    }
@bp.route("/ajaxGetData/<string:service_id>/<string:device_id>", methods=["post"])
def ajaxGetData(service_id,device_id):
    cookie_value = request.cookies.get('user')
    return{
        "data":session[cookie_value]["services"][service_id]["cate_service"][device_id][request.form["cat_data"]],
        "frequency":frequency,
        "action":service_action,
        "cate_service":cate_service
    }
@bp.route("/form_edit_data/<string:service_id>/<string:device_id>", methods=["POST"])
def form_edit_data(service_id, device_id):
    cookie_value = request.cookies.get('user')
    _unprocessed = request.form["cate_service_unprocessed"]
    _frequency = request.form["cate_service_frequency"]
    _action = request.form["cate_service_action"]
    _cate = request.form["cate_service_cate"]

    # record the cate_service data
    if "cate_service" not in session[cookie_value]["services"][service_id].keys():
        session[cookie_value]["services"][service_id]["cate_service"] = {}

    if device_id not in session[cookie_value]["services"][service_id]["cate_service"].keys():
        session[cookie_value]["services"][service_id]["cate_service"][device_id] = {}

    session[cookie_value]["services"][service_id]["cate_service"][device_id][_unprocessed] = {
        "action": _action,
        "frequency": _frequency,
        "category": _cate,
    }
    return jsonify(success=True)
@bp.route("/form_edit/<string:service_id>/<string:device_id>/<string:unprocessed>", methods=["GET", "POST"])
def form_edit(service_id, device_id, unprocessed):
    # print(f"form_edit")
    unprocessed_data = []

    if "raw_data" in session["devices"][device_id].keys():
        if len(session["devices"][device_id]["raw_data"].keys()) > 0:
            unprocessed_data = session["devices"][device_id]["raw_data"].keys()

    choose_data = {
        "data": {
            "unprocessed_data": unprocessed,
            "action": session["services"][service_id]["cate_service"][device_id][unprocessed]["action"],
            "frequency": session["services"][service_id]["cate_service"][device_id][unprocessed]["frequency"],
            "category": session["services"][service_id]["cate_service"][device_id][unprocessed]["category"],
        }
    }

    # print(f"choose_data : {choose_data}")

    return render_template(
        "forms/cate_service_form.html",
        device_id=device_id,
        service_id=service_id,
        frequency=frequency,
        action=service_action,
        unprocessed_data=unprocessed_data,
        cate_service=cate_service,
        choose_data=choose_data,
    )


@bp.route("/delete", methods=["GET"])
def delete():
    cookie_value = request.cookies.get('user')
    if(cookie_value == None):
        return redirect('/users')
    if "cate_service" in session[cookie_value].keys():
        del session[cookie_value]["cate_service"]

    return redirect(url_for("service.service_page"))


@bp.route("/delete_unprocessed/<string:service_id>/<string:device_id>/<string:unprocessed>", methods=["GET"])
def delete_unprocessed(service_id, device_id, unprocessed):
    # return {"service_id": service_id, "device_id": device_id, "un_data": unprocessed}
    cookie_value = request.cookies.get('user')
    if(cookie_value == None):
        return redirect('/users')
    if "cate_service" in session[cookie_value].keys():
        if unprocessed in session[cookie_value]["cate_service"].keys():
            del session[cookie_value]["cate_service"][unprocessed]
    try:
        del session[cookie_value]["services"][service_id]["cate_service"][device_id][unprocessed]

        if session[cookie_value]["services"][service_id]["cate_service"][device_id] == {}:
            del session[cookie_value]["services"][service_id]["cate_service"][device_id] 
        
        if session[cookie_value]["services"][service_id]["cate_service"] == {}:
            del session[cookie_value]["services"][service_id]["cate_service"]
            
    except Exception as e:
        return {"error": "can not find this data",
                "e": e}

    return redirect(url_for("service.service_page"))
