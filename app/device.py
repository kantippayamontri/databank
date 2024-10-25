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

bp = Blueprint("device", __name__, url_prefix="/device")

@bp.route("/device_page", methods=["GET"])
def device_page():
    cookie_value = request.cookies.get('user')
    if(cookie_value == None):
        return redirect('/users')
    if "devices" not in session[cookie_value].keys():
        return render_template(
            "device_page.html",
            form_utils={
                "device": {
                    "type_device": enumerate(type_device),
                    "unprocessed_data": enumerate(unprocessed_data),
                },
                "new_device": True,
                "name":cookie_value
            },
        )
    else:
        return render_template(
            "device_page.html",
            form_utils={
                "device": {
                    "type_device": enumerate(type_device),
                    "unprocessed_data": enumerate(unprocessed_data),
                },
                "new_device": False,
                "name":cookie_value
            },
        )
    # return render_template("device_page.html")

@bp.route("/form", methods=["GET"])
def form():

    if "devices" not in session.keys():
        return render_template(
            "forms/device_form.html",
            form_utils={
                "device": {
                    "type_device": enumerate(type_device),
                    "unprocessed_data": enumerate(unprocessed_data),
                },
                "new_device": True,
            },
        )
    else:
        return render_template(
            "forms/device_form.html",
            form_utils={
                "device": {
                    "type_device": enumerate(type_device),
                    "unprocessed_data": enumerate(unprocessed_data),
                },
                "new_device": False,
            },
        )

@bp.route("/form_edit/<int:device_id>", methods=["GET"])
def form_edit(device_id):
    data_in_dropdown = []
    data_in_dropdown = unprocessed_data
    # if session["devices"][str(device_id)]["device_type"] in type_device_details.keys():
    #     data_in_dropdown = type_device_details[session["devices"][str(device_id)]["device_type"]]
    # else:
    #     data_in_dropdown = unprocessed_data

    return render_template(
        "forms/device_form.html",
        form_utils={
            "device_id": device_id,
            "device": {
                "type_device": enumerate(type_device),
                "unprocessed_data": enumerate(data_in_dropdown),
            },
            "new_device": False,
        },
    )

    # return jsonify({"device id": device_id,
    #                 "data_dropdown": data_in_dropdown})

@bp.route("/form_new", methods=["GET"])
def form_new():
    return render_template(
        "forms/device_form.html",
        form_utils={
            "device": {
                "type_device": enumerate(type_device),
                "unprocessed_data": enumerate(unprocessed_data),
            },
            "new_device": True,
        },
    )

@bp.route("/update/<int:device_id>", methods=["POST"])
def update_with_id(device_id):
    _device = request.get_json()
    # print(f"_device: {_device}")
    # device_name = _device["device_name"]
    # device_type = _device["device_type"]
    # device_unprocessed = _device["device_unprocessed"]
    new_device = _device["new_device"]
    cookie_value = request.cookies.get('user')
    if not new_device:
        del _device["new_device"]
        session[cookie_value]["devices"][str(device_id)]["device_name"]= _device["device_name"]
        session[cookie_value]["devices"][str(device_id)]["device_type"]= _device["device_type"]
        # check unprocessed data 
        old_un = session[cookie_value]["devices"][str(device_id)]["device_unprocessed"]
        new_un = _device["device_unprocessed"]

        for _o in old_un:
            if _o not in new_un:
                # check _o in raw_data
                if "raw_data" in session[cookie_value]["devices"][str(device_id)].keys():
                    del session[cookie_value]["devices"][str(device_id)]["raw_data"][_o]
                    
                    if session[cookie_value]["devices"][str(device_id)]["raw_data"] == {}:
                        del session[cookie_value]["devices"][str(device_id)]["raw_data"] 
        
        
        
        session[cookie_value]["devices"][str(device_id)]["device_unprocessed"]= _device["device_unprocessed"]
        
    
    return jsonify(success=True)

@bp.route("/add", methods=["POST"])
def add():
    _device = request.get_json()
    cookie_value = request.cookies.get('user')
    device_name = _device["device_name"]
    device_type = _device["device_type"]
    device_unprocessed = _device["device_unprocessed"]
    new_device = _device["new_device"]

    # session["device"] = _device
    # record the device data
    if "devices" not in session[cookie_value].keys():
        del _device["new_device"]
        session[cookie_value]["devices"] = {"0": _device}
    else:

        if new_device:
            # add new device
            print("add new device")
            device_id_new_device = (
                max(list([int(device_id) for device_id in session[cookie_value]["devices"].keys()]))
                + 1
            )
            del _device["new_device"]
            session[cookie_value]["devices"][str(device_id_new_device)] = _device

    return jsonify(success=True)


@bp.route("/clear", methods=["GET"])
def clear():
    session["device"] = None
    return "remove data session success"


# TODO: delete this cuz it's for one device
@bp.route("/get", methods=["GET"])
def get():
    if ("device" not in session.keys()) or (session["device"] is None):
        resp = jsonify()
        resp.status_code = 404
        return resp
    resp = jsonify(session["device"])
    resp.status_code = 200
    return resp

@bp.route("/get/<int:device_id>", methods=["GET"])
def get_with_id(device_id):
    if ("devices" not in session.keys()) or (session["devices"] is None):
        resp = jsonify()
        resp.status_code = 404
        return resp
    resp = jsonify(session["devices"][str(device_id)])
    resp.status_code = 200
    return resp


@bp.route("/delete/<int:device_id>", methods=["GET"])
def delete(device_id):
    device_id = str(device_id)
    cookie_value = request.cookies.get('user')
    if "devices" in session[cookie_value].keys():
        if str(device_id) in session[cookie_value]["devices"].keys():
            del session[cookie_value]["devices"][str(device_id)]
    
        if session[cookie_value]["devices"] == {}:
            del session[cookie_value]["devices"]

    # check device in services and delete
    if "services" in session.keys():
        for _service_id in session.get("services").keys():
            if "cate_service" in session["services"][_service_id]:
                for _device_id in session.get("services")[_service_id]["cate_service"].keys():
                    if device_id == _device_id:
                        del session["services"][_service_id]["cate_service"][device_id]
                    
                    if session["services"][_service_id]["cate_service"] == {}:
                        del session["services"][_service_id]["cate_service"]
    
    # # also raw data
    # if "raw_data" in session.keys():
    #     del session["raw_data"]

    # # also cate service
    # if "cate_service" in session.keys():
    #     del session["cate_service"]

    return redirect(url_for("device.device_page"))  # back to homepage


@bp.route("/get_details", methods=["POST"])
def get_details():
    _data = request.get_json()
    # print(f"data is {_data}")

    resp = {"unprocessed_data": []}
    if _data["data"] in type_device_details.keys():
        resp["unprocessed_data"] = type_device_details[_data["data"]]
    else:
        resp["unprocessed_data"] = unprocessed_data

    resp = jsonify(resp)
    resp.status_code = 200
    return resp

@bp.route("/get_details/<int:device_id>", methods=["POST"])
def get_detail_with_id(device_id):
    print(f"device_is: {device_id}")

    device_type = session["devices"][str(device_id)]['device_type']

    resp = {"unprocessed_data": []} 
    if device_type in type_device_details.keys():
        resp["unprocessed_data"] = type_device_details[device_type]
    else:
        resp["unprocessed_data"] = unprocessed_data

    resp = jsonify(resp)
    resp.status_code = 200
    return resp
