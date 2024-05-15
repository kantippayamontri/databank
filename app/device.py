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
    # print(f"_device: {_device}")
    device_name = _device["device_name"]
    device_type = _device["device_type"]
    device_unprocessed = _device["device_unprocessed"]

    # session["device"] = _device
    # record the device data
    if "device" not in session.keys():
        session["device"] = _device
    else:
        # check device type
        session["device"]["device_name"] = device_name
        if device_type == session["device"]["device_type"]:
            # assign new unprocessed
            session["device"]["device_unprocessed"] = device_unprocessed

            # check unprocessed in device and raw data
            if "raw_data" in session.keys():
                _del_p = []
                for _un_p_raw in session["raw_data"].keys():
                    if _un_p_raw not in session["device"]["device_unprocessed"]:
                        _del_p.append(_un_p_raw) 
                
                for _d in _del_p:
                    del session["raw_data"][_d]
                
                # check in cate_service
                if "cate_service" in session.keys():
                    for _d in _del_p:
                        if _d in session["cate_service"].keys():
                            del session["cate_service"][_d]
                        
        else:
            # new device type and device unprocessed
            session["device"]["device_name"] = device_name
            session["device"]["device_type"] = device_type
            session["device"]["device_unprocessed"] = device_unprocessed

            if "raw_data" in session.keys():
                del session["raw_data"]
            
            if "cate_service" in session.keys():
                del session["cate_service"]


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
        
    # also cate service
    if "cate_service" in session.keys():
        del session["cate_service"]

    return redirect(url_for("main_page"))  # back to homepage


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
