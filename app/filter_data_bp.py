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

bp = Blueprint("filter", __name__, url_prefix="/filter")
data = {
        "devices": {
            "0": {
                "device_name": "Gauge",
                "device_type": "Security Camera",
                "device_unprocessed": [
                    "Footage"
                ]
            },
            "1": {
                "device_name": "smart meter",
                "device_type": "Security Camera",
                "device_unprocessed": [
                    "Footage",
                    "activity"
                ],
                "raw_data": {
                    "Footage": {
                        "action": "Average",
                        "frequency": "Daily",
                        "sensitivity": "Low"
                    }
                }
            }
        },
        "services": {
            "0": {
                "cate_service": {
                    "1": {
                        "Footage": {
                            "action": "View Data",
                            "category": "Low",
                            "frequency": "Daily"
                        }
                    }
                },
                "service_name": "Meta",
                "service_type": "Advertising Company"
            },
            "1": {
                "service_name": "Meta_(1)",
                "service_type": "Tech Company"
            }
        }
    }

@bp.route("/show_data", methods=["GET"])
def form():
    # data_in_dropdown = []
    # if session["device"]["device_type"] in type_device_details.keys():
    #     data_in_dropdown = type_device_details[session["device"]["device_type"]]
    # else:
    #     data_in_dropdown = unprocessed_data
    
    return render_template(
        "forms/filter_data_form.html",
        # form_utils={
        #     "device": {
        #         "type_device": enumerate(type_device),
        #         "unprocessed_data": enumerate(data_in_dropdown),
        #     }
        # },
    )

@bp.route("/filter", methods=["GET"])
def filter():
    type = request.args.get('type')
    match type:
        case 'devices':
            if "devices" in data:
                if data["devices"]:
                    return data["devices"]
            return []
        case 'services':
            if "services" in data:
                if data["services"]:
                    return data["services"]
            return []
        case 'data_by_device':
            if "devices" in data:
                if data["devices"]:
                    return data["devices"]
            return []
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
