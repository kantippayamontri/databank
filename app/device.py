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

        # return render_template(
        #     "forms/device_form.html",
        #     form_utils={
        #         "device": {
        #             "type_device": enumerate(type_device),
        #             "unprocessed_data": enumerate(data_in_dropdown),
        #         },
        #         "new_device": False,
        #     },
        # )
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

    if not new_device:
        del _device["new_device"]
        session["devices"][str(device_id)] = _device
    
    return jsonify(success=True)

@bp.route("/add", methods=["POST"])
def add():
    _device = request.get_json()
    # print(f"_device: {_device}")
    device_name = _device["device_name"]
    device_type = _device["device_type"]
    device_unprocessed = _device["device_unprocessed"]
    new_device = _device["new_device"]

    # session["device"] = _device
    # record the device data
    if "devices" not in session.keys():
        del _device["new_device"]
        session["devices"] = {"0": _device}
    else:

        if new_device:
            # add new device
            print("add new device")
            device_id_new_device = (
                max(list([int(device_id) for device_id in session["devices"].keys()]))
                + 1
            )
            del _device["new_device"]
            session["devices"][str(device_id_new_device)] = _device

        # # check device type
        # session["device"]["device_name"] = device_name
        # if device_type == session["device"]["device_type"]:
        #     # assign new unprocessed
        #     session["device"]["device_unprocessed"] = device_unprocessed

        #     # check unprocessed in device and raw data
        #     if "raw_data" in session.keys():
        #         _del_p = []
        #         for _un_p_raw in session["raw_data"].keys():
        #             if _un_p_raw not in session["device"]["device_unprocessed"]:
        #                 _del_p.append(_un_p_raw)

        #         for _d in _del_p:
        #             del session["raw_data"][_d]

        #         # check in cate_service
        #         if "cate_service" in session.keys():
        #             for _d in _del_p:
        #                 if _d in session["cate_service"].keys():
        #                     del session["cate_service"][_d]

        # else:
        #     # new device type and device unprocessed
        #     session["device"]["device_name"] = device_name
        #     session["device"]["device_type"] = device_type
        #     session["device"]["device_unprocessed"] = device_unprocessed

        #     if "raw_data" in session.keys():
        #         del session["raw_data"]

        #     if "cate_service" in session.keys():
        #         del session["cate_service"]

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
    if "devices" in session.keys():
        if str(device_id) in session["devices"].keys():
            del session["devices"][str(device_id)]

    # # also raw data
    # if "raw_data" in session.keys():
    #     del session["raw_data"]

    # # also cate service
    # if "cate_service" in session.keys():
    #     del session["cate_service"]

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
