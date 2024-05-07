from flask import (
    Blueprint,
    jsonify,
    redirect,
    render_template,
    request,
    session,
    url_for,
)

from app import type_device, type_device_details, unprocessed_data

bp = Blueprint("device", __name__, url_prefix="/device")


@bp.route("/form", methods=["GET"])
def form():

    if "device" not in session.keys():
        return render_template(
            "forms/device_form.html",
            form_utils={
                "device": {
                    "type_device": enumerate(type_device),
                    "unprocessed_data": enumerate(unprocessed_data),
                }
            },
        )
    else:
        
        data_in_dropdown = []
        if session["device"]["device_type"] in type_device_details.keys():
            data_in_dropdown = type_device_details[session["device"]["device_type"]]
        else:
            data_in_dropdown = unprocessed_data
             
        
        return render_template(
            "forms/device_form.html",
            form_utils={
                "device": {
                    "type_device": enumerate(type_device),
                    "unprocessed_data": enumerate(data_in_dropdown),
                }
            },
        )
        

@bp.route("/add", methods=["POST"])
def add():
    _device = request.get_json()
    print(f"_device: {_device}")
    device_name = _device["device_name"]
    device_type = _device["device_type"]
    device_unprocessed = _device["device_unprocessed"]

    # record the device data
    session["device"] = _device

    # add raw data
    # if "raw_data" in session.keys():
    #     ...
    # un_data_session =

    return jsonify(success=True)


@bp.route("/clear", methods=["GET"])
def clear():
    session["device"] = None
    return "remove data session success"


@bp.route("/get", methods=["GET"])
def get():
    if ("device" not in session.keys()) or (session["device"] is None):
        resp = jsonify()
        resp.status_code = 404
        return resp
    resp = jsonify(session["device"])
    resp.status_code = 200
    return resp


@bp.route("/delete", methods=["GET"])
def delete():
    if "device" in session.keys():
        del session["device"]

    # also raw data
    if "raw_data" in session.keys():
        del session["raw_data"]

    return redirect(url_for("main_page"))  # back to homepage


@bp.route("/get_details", methods=["POST"])
def get_details():
    _data = request.get_json()
    print(f"data is {_data}")
    
    resp = {"unprocessed_data": []}
    if _data["data"] in type_device_details.keys():
        resp["unprocessed_data"] = type_device_details[_data["data"]]
    else: 
        resp["unprocessed_data"] = unprocessed_data

    resp = jsonify(resp)
    resp.status_code = 200
    return resp
