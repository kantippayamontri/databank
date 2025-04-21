from flask import (
    Blueprint,
    jsonify,
    redirect,
    render_template,
    request,
    session,
    url_for,
)
import json
from .utils.constants import type_device, type_device_details, unprocessed_data
from flask_session import Session
from .models import User

from app.app import db

from sqlalchemy import text

from collections import defaultdict
from flask import current_app

bp = Blueprint("device", __name__, url_prefix="/device")

@bp.route("/device_page", methods=["GET"])
def device_page():
    cookie_value = cookie_value = session.get('user_id')
    if cookie_value==None:
            return redirect('/')
    result = db.session.execute(text("SELECT devices.*,device_types.name as type_name FROM devices left join device_types on device_types.id=devices.device_type_id where devices.user_id= "+str(cookie_value)+" order by id desc"))
    devices = result.fetchall()
    result_type = db.session.execute(text("SELECT * FROM device_types order by id desc"))
    device_type = result_type.fetchall()
    result_data = db.session.execute(text("SELECT * FROM device_datas order by id desc"))
    device_data = result_data.fetchall()
    grouped_data = defaultdict(list)
    for item in device_data:
        grouped_data[item[1]].append(item)
    try:
        # if(cookie_value == None):
        #     return render_template("user_select.html",user="not-show-path")
        if len(devices) ==0:
            return render_template(
                "device_page.html",
                form_utils={
                    "device": {
                        "type_device": enumerate(device_type),
                        "unprocessed_data": grouped_data,
                    },
                    "new_device": True,
                    "name":cookie_value
                },
                devices=enumerate(devices),
                device_count=len(devices),
                device_name=devices
            )
        else:
            return render_template(
                "device_page.html",
                form_utils={
                    "device": {
                        "type_device": enumerate(device_type),
                        "unprocessed_data": grouped_data,
                    },
                    "new_device": False,
                    "name":cookie_value
                },
                devices=enumerate(devices),
                device_count=len(devices),
                device_name=devices
            )
    except Exception as e:
            return render_template("user_select.html",user="not-show-path")
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


@bp.route("/update/<int:device_id>", methods=["POST"])
def update_with_id(device_id):
    _device = request.get_json()
    cookie_value = session.get('user_id')
    device_name = _device["device_name"]
    device_type = _device["device_type"]
    device_unprocessed = _device["device_unprocessed"]
    device_sensitivity = _device["device_sensitivity"]
    new_device = _device["new_device"]
    if device_type==-1:
        result = db.session.execute(text("INSERT INTO device_types (name) VALUES (?)", (device_name)))
        device_type = result.lastrowid
    sql = text("update devices set name=:name, device_type_id=:type, sensitivity=:sensitivity where id="+str(device_id))
    params = {"name": device_name, "type": device_type, "sensitivity": device_sensitivity}
    result=db.session.execute(sql, params)
    result=db.session.execute(text('delete from device_datas where device_id='+str(device_id)))
    category=''
    match device_sensitivity:
        case 'low':
            category= 1
        case 'medium':
            category= 2
        case 'high':
            category= 3
        case _:
            category= 4
    sql = text("""
        INSERT INTO device_datas (name, user_id, category, device_id)
        VALUES (:name, :user_id, :category, :device_id)
    """)
    data_to_insert = [
        {"name": data, "user_id": 1, "category": category, "device_id": device_id}
        for data in device_unprocessed
    ]
    db.session.execute(
        sql, data_to_insert
    )
    db.session.commit()

    # cookie_value = request.cookies.get('user')
    # if not new_device:
    #     del _device["new_device"]
    #     session[cookie_value]["devices"][str(device_id)]["device_name"]= _device["device_name"]
    #     session[cookie_value]["devices"][str(device_id)]["device_type"]= _device["device_type"]
    #     # check unprocessed data 
    #     old_un = session[cookie_value]["devices"][str(device_id)]["device_unprocessed"]
    #     new_un = _device["device_unprocessed"]

    #     for _o in old_un:
    #         if _o not in new_un:
    #             # check _o in raw_data
    #             if "raw_data" in session[cookie_value]["devices"][str(device_id)].keys():
    #                 del session[cookie_value]["devices"][str(device_id)]["raw_data"][_o]
                    
    #                 if session[cookie_value]["devices"][str(device_id)]["raw_data"] == {}:
    #                     del session[cookie_value]["devices"][str(device_id)]["raw_data"] 
        
        
        
    #     session[cookie_value]["devices"][str(device_id)]["device_unprocessed"]= _device["device_unprocessed"]
        
    
    return jsonify(success=True)

@bp.route("/add", methods=["POST"])
def add():
    _device = request.get_json()
    cookie_value = session.get('user_id')
    device_name = _device["device_name"]
    device_type = _device["device_type"]
    device_unprocessed = _device["device_unprocessed"]
    device_sensitivity = _device["device_sensitivity"]
    new_device = _device["new_device"]
    if device_type==-1:
        result = db.session.execute(text("INSERT INTO device_types (name) VALUES (?)", (device_name)))
        device_type = result.lastrowid
    sql = text("INSERT INTO devices (name, device_type_id, sensitivity, user_id) VALUES (:name, :type, :sensitivity, :user_id)")
    params = {"name": device_name, "type": device_type, "sensitivity": device_sensitivity,"user_id":cookie_value}

    result=db.session.execute(sql, params)
    device_id = result.lastrowid
    category=''
    match device_sensitivity:
        case 'low':
            category= 1
        case 'medium':
            category= 2
        case 'high':
            category= 3
        case _:
            category= 4
    sql = text("""
        INSERT INTO device_datas (name, user_id, category, device_id)
        VALUES (:name, :user_id, :category, :device_id)
    """)
    data_to_insert = [
        {"name": data, "user_id": 1, "category": category, "device_id": device_id}
        for data in device_unprocessed
    ]
    db.session.execute(
        sql, data_to_insert
    )
    db.session.commit()


    # session["device"] = _device
    # record the device data
    # if "devices" not in session[cookie_value].keys():
    #     del _device["new_device"]
    #     session[cookie_value]["devices"] = {"0": _device}
    # else:

    #     if new_device:
    #         # add new device
    #         print("add new device")
    #         device_id_new_device = (
    #             max(list([int(device_id) for device_id in session[cookie_value]["devices"].keys()]))
    #             + 1
    #         )
    #         del _device["new_device"]
    #         session[cookie_value]["devices"][str(device_id_new_device)] = _device

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
    cookie_value = session.get('user_id')
    if cookie_value==None:
            return redirect('/')
    try:
        if cookie_value==None:
            return redirect('/')
        db.session.execute(
            text("Delete FROM device_datas where device_id="+device_id)
        )
        db.session.commit()
        db.session.execute(
            text("Delete FROM devices where id="+device_id)
        )
        db.session.commit()
        # if "devices" in session[cookie_value].keys():
        #     if str(device_id) in session[cookie_value]["devices"].keys():
        #         del session[cookie_value]["devices"][str(device_id)]
        
        #     if session[cookie_value]["devices"] == {}:
        #         del session[cookie_value]["devices"]

        # # check device in services and delete
        # if "services" in session.keys():
        #     for _service_id in session.get("services").keys():
        #         if "cate_service" in session["services"][_service_id]:
        #             for _device_id in session.get("services")[_service_id]["cate_service"].keys():
        #                 if device_id == _device_id:
        #                     del session["services"][_service_id]["cate_service"][device_id]
                        
        #                 if session["services"][_service_id]["cate_service"] == {}:
        #                     del session["services"][_service_id]["cate_service"]
        
        # # also raw data
        # if "raw_data" in session.keys():
        #     del session["raw_data"]

        # # also cate service
        # if "cate_service" in session.keys():
        #     del session["cate_service"]

        return redirect(url_for("device.device_page"))  # back to homepage
    except Exception as e:
            return render_template("user_select.html",user="not-show-path")

@bp.route("/get-unprocessed-data/<int:device_id>", methods=["GET"])
def get_unprocessed_data(device_id):
    result=db.session.execute(
        text("Select * FROM device_datas where device_id="+str(device_id))
    )
    data = result.fetchall()
    columns = result.keys()
    data = [dict(zip(columns, row)) for row in data]
    resp = jsonify(data)
    resp.status_code = 200
    return resp
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
