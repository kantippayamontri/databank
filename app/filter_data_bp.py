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

bp = Blueprint("filter", __name__, url_prefix="/filter")
data = {
    "devices": {
        "0": {
            "device_name": "Smart TV",
            "device_type": "Digital TV",
            "device_unprocessed": [
                "Light status",
                "Energy usage",
                "Colour"
            ],
            "raw_data": {
                "Colour": {
                    "action": "Anonymise",
                    "frequency": "Yearly",
                    "sensitivity": "Medium"
                },
                "Energy usage": {
                    "action": "Transfer",
                    "frequency": "Yearly",
                    "sensitivity": "Medium"
                },
                "Light status": {
                    "action": "Average",
                    "frequency": "Daily",
                    "sensitivity": "Low"
                }
            }
        },
        "1": {
            "device_name": "Gauge",
            "device_type": "Light",
            "device_unprocessed": [
                "Light Status",
                "Color",
                "Activity period"
            ],
            "raw_data": {
                "Activity period": {
                    "action": "Transfer",
                    "frequency": "No fix time",
                    "sensitivity": "Medium"
                },
                "Color": {
                    "action": "Upload",
                    "frequency": "Yearly",
                    "sensitivity": "High"
                },
                "Light Status": {
                    "action": "Average",
                    "frequency": "Daily",
                    "sensitivity": "Low"
                }
            }
        }
    },
    "services": {
        "0": {
            "service_name": "The8thFloor",
            "service_type": "Tech Company",
            "cate_service": {
                "0": { 
                    "device_id": 0,
                    "device_unprocessed": "Colour",
                    "action": "Report Data",
                    "category": "Low",
                    "frequency": "Daily"
                },
                "1":{
                    "device_id": 0,
                    "device_unprocessed": "Type Status",
                    "action": "View Data",
                    "category": "Low",
                    "frequency": "Daily"
                }
            }
        },
        "1": {
            "service_name": "JameCompany",
            "service_type": "Security Company",
            "cate_service": {
                "0": { 
                    "device_id": 1,
                    "device_unprocessed": "Colour",
                    "action": "Read Data",
                    "category": "Low",
                    "frequency": "Daily"
                },
                "1": { 
                    "device_id": 0,
                    "device_unprocessed": "Light Status",
                    "action": "View Data",
                    "category": "Low",
                    "frequency": "Daily"
                },
                "2": { 
                    "device_id": 0,
                    "device_unprocessed": "New Status",
                    "action": "View Data",
                    "category": "Low",
                    "frequency": "Daily"
                }
            }
        },
        "2": {
            "service_name": "Techneena",
            "service_type": "Tech Company",
            "cate_service": {
                "0": { 
                    "device_id": 0,
                    "device_unprocessed": "Colour",
                    "action": "Report Data",
                    "category": "Low",
                    "frequency": "Daily"
                },
                "1":{
                    "device_id": 0,
                    "device_unprocessed": "Show me Status",
                    "action": "View Data",
                    "category": "Low",
                    "frequency": "Daily"
                }
            }
        }
    }
}

@bp.route("/show_data", methods=["GET"])
def form():
    print('hello')
    data_in_dropdown = []
    if session["device"]["device_type"] in type_device_details.keys():
        data_in_dropdown = type_device_details[session["device"]["device_type"]]
    else:
        data_in_dropdown = unprocessed_data
    
    return render_template(
        "forms/filter_data_form.html",
        form_utils={
            "device": {
                "type_device": enumerate(type_device),
                "unprocessed_data": enumerate(data_in_dropdown),
            }
        },
    )

@bp.route("/filter", methods=["GET"])
def filter():
    type = request.args.get('type')
    match type:
        case 'devices':
            return data["devices"]
        case 'services':
            return data["services"]
        case 'data_by_device':
            return data["devices"]
        case 'data_by_service':
            return [data["devices"],data["services"]]
