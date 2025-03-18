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
from app.app import db
from sqlalchemy import text

from .utils.constants import type_device, type_device_details, unprocessed_data

bp = Blueprint("filter", __name__, url_prefix="/filter")
# data = data = {
#         "devices": {
#             "0": {
#                 "device_name": "Gauge",
#                 "device_type": "Smartmetre",
#                 "device_unprocessed": [
#                     "Footage",
#                     "Energy usage",
#                     "Light status"
#                 ],
#                 "raw_data": {
#                     "Energy usage": {
#                         "action": "Average",
#                         "frequency": "Daily",
#                         "sensitivity": "Low"
#                     },
#                     "Footage": {
#                         "action": "Average",
#                         "frequency": "Daily",
#                         "sensitivity": "Low"
#                     },
#                     "Light status": {
#                         "action": "Average",
#                         "frequency": "Daily",
#                         "sensitivity": "Low"
#                     }
#                 }
#             },
#             "1": {
#                 "device_name": "Smart TV",
#                 "device_type": "Digital TV",
#                 "device_unprocessed": [
#                     "Video",
#                     "channel"
#                 ]
#             }
#         },
#         "services": {
#             "0": {
#                 "cate_service": {
#                     "0": {
#                         "Energy usage": {
#                             "action": "Read Data",
#                             "category": "Medium",
#                             "frequency": "Yearly"
#                         }
#                     }
#                 },
#                 "service_name": "The8thFloor",
#                 "service_type": "Tech Company"
#             }
#         }
#     }

@bp.route("/show_data", methods=["GET"])
def form():
    return render_template(
        "forms/filter_data_form.html",
    )

@bp.route("/filter", methods=["GET"])
def filter():
    cookie_value = request.cookies.get('user')
    type = request.args.get('type')
    data = session[cookie_value]
    match type:
        case 'devices':
            result = db.session.execute(text("SELECT devices.*,device_types.name as type_name FROM devices left join device_types on device_types.id=devices.device_type_id order by id desc"))
            devices = result.fetchall()
            column_names = result.keys()
            devices_list = [dict(zip(column_names, row)) for row in devices]
            json_data = json.dumps(devices_list, indent=4)
            return json_data
        case 'services':
            result = db.session.execute(text("SELECT services.* FROM services order by id desc"))
            services = result.fetchall()
            column_names = result.keys()
            devices_list = [dict(zip(column_names, row)) for row in services]
            json_data = json.dumps(devices_list, indent=4)
            return json_data
        case 'data_by_device':
            result = db.session.execute(text("SELECT device_datas.*,devices.name as device_name FROM device_datas left join devices on devices.id = device_datas.device_id order by id desc"))
            services = result.fetchall()
            column_names = result.keys()
            devices_list = [dict(zip(column_names, row)) for row in services]
            json_data = json.dumps(devices_list, indent=4)
            return json_data
        case 'data_by_service':
            devices = []
            if "devices" in data:
                if data["devices"]:
                    devices = data["devices"]
            services = []
            if "services" in data:
                if data["services"]:
                    services = data["services"]
            return [devices,services]
