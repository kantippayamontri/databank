from flask import (
    Blueprint,
    jsonify,
    redirect,
    render_template,
    request,
    session,
    url_for,
)
from .utils import frequency, raw_data_action, cate_raw_data

bp = Blueprint("raw_data", __name__, url_prefix="/raw_data")

@bp.route("/dump/data", methods=["GET"])
def dump():
    session['User1'] = {
        "tour": 0,
        "devices": {
        "0": {
            "device_name": "Smart TV",
            "device_type": "TV",
            "device_unprocessed": [
            "Viewing Habits",
            "Location Data",
            "Device Usage",
            "Voice and Interaction Data"
            ],
            "raw_data": {
            "Viewing Habits": [
                {
                "action": "Average",
                "frequency": "Daily",
                "sensitivity": "Low"
                }
            ],
            "Location Data": [
                {
                "action": "Anonymise",
                "frequency": "Weekly",
                "sensitivity": "High"
                }
            ],
            "Device Usage": [
                {
                "action": "Download",
                "frequency": "Yearly",
                "sensitivity": "Medium"
                }
            ],
            "Voice and Interaction Data": [
                {
                "action": "Transfer",
                "frequency": "No fix time",
                "sensitivity": "High"
                }
            ]
            }
        },
        "1": {
            "device_name": "Security Camera",
            "device_type": "Security Camera",
            "device_unprocessed": [
            "Footage",
            "Audio Data",
            "Motion and Activity Data"
            ],
            "raw_data": {
            "Footage": [
                {
                "action": "Anonymise",
                "frequency": "Daily",
                "sensitivity": "High"
                }
            ],
            "Audio Data": [
                {
                "action": "Download",
                "frequency": "Weekly",
                "sensitivity": "Low"
                }
            ],
            "Motion and Activity Data": [
                {
                "action": "Anonymise",
                "frequency": "Daily",
                "sensitivity": "High"
                }
            ]
            }
        },
        "2": {
            "device_name": "Smart Door Lock",
            "device_type": "Door lock",
            "device_unprocessed": [
            "User Credentials",
            "Access Logs",
            "Device Information",
            "Lock Status"
            ],
            "raw_data": {
            "User Credentials": [
                {
                "action": "Anonymise",
                "frequency": "Weekly",
                "sensitivity": "High"
                }
            ],
            "Access Logs": [
                {
                "action": "Anonymise",
                "frequency": "Weekly",
                "sensitivity": "Medium"
                }
            ],
            "Device Information": [
                {
                "action": "Average",
                "frequency": "Daily",
                "sensitivity": "Low"
                }
            ]
            }
        },
        "3": {
            "device_name": "Smart Electricity Metre",
            "device_type": "Smartmetre",
            "device_unprocessed": [
            "Historical Data",
            "Operational Data",
            " Consumption Data",
            "Location Data"
            ],
            "raw_data": {
            "Historical Data": [
                {
                "action": "Anonymise",
                "frequency": "Weekly",
                "sensitivity": "Low"
                }
            ],
            "Operational Data": [
                {
                "action": "Transfer",
                "frequency": "No fix time",
                "sensitivity": "High"
                }
            ],
            " Consumption Data": [
                {
                "action": "Average",
                "frequency": "Daily",
                "sensitivity": "Medium"
                }
            ],
            "Location Data": [
                {
                "action": "Anonymise",
                "frequency": "Daily",
                "sensitivity": "High"
                }
            ]
            }
        }
        },
        "services": {
        "0": {
            "service_name": "Mary",
            "service_type": "User",
            "cate_service": {
            "0": {
                "Viewing Habits": {
                "action": "Read Data",
                "frequency": "Daily",
                "category": "Low",
                "holiday": "true",
                "night": "true",
                "home": "true"
                },
                "Voice and Interaction Data": {
                "action": "View Data",
                "frequency": "Daily",
                "category": "Low",
                "holiday": "true",
                "night": "false",
                "home": "false"
                }
            },
            "2": {
                "Access Logs": {
                "action": "Read Data",
                "frequency": "Daily",
                "category": "High"
                }
            }
            }
        },
        "1": {
            "service_name": "Michael",
            "service_type": "User",
            "cate_service": {
            "0": {
                "Device Usage": {
                "action": "View Data",
                "frequency": "Daily",
                "category": "High"
                },
                "Location Data": {
                "action": "View Data",
                "frequency": "Daily",
                "category": "High"
                }
            },
            "3": {
                "Historical Data": {
                "action": "Report Data",
                "frequency": "No fix time",
                "category": "Low"
                }
            },
            "2": {
                "User Credentials": {
                "action": "View Data",
                "frequency": "No fix time",
                "category": "High"
                }
            }
            }
        },
        "2": {
            "service_name": "Police officer",
            "service_type": "Authority",
            "cate_service": {
            "1": {
                "Footage": {
                "action": "View Data",
                "frequency": "Daily",
                "category": "Medium",
                "holiday": "false",
                "night": "false",
                "home": "false"
                },
                "Motion and Activity Data": {
                "action": "Send Notification",
                "frequency": "Daily",
                "category": "High",
                "holiday": "false",
                "night": "false",
                "home": "false"
                },
                "Audio Data": {
                "action": "View Data",
                "frequency": "Daily",
                "category": "High",
                "holiday": "false",
                "night": "false",
                "home": "false"
                }
            },
            "2": {
                "Device Information": {
                "action": "Read Data",
                "frequency": "Daily",
                "category": "Medium",
                "holiday": "false",
                "night": "false",
                "home": "false"
                }
            }
            }
        },
        "3": {
            "service_name": "British Gas",
            "service_type": "Energy Suplier",
            "cate_service": {
            "3": {
                " Consumption Data": {
                "action": "View Data",
                "frequency": "Daily",
                "category": "Medium"
                },
                "Location Data": {
                "action": "Read Data",
                "frequency": "Daily",
                "category": "High"
                },
                "Historical Data": {
                "action": "View Data",
                "frequency": "Weekly",
                "category": "Low"
                },
                "Operational Data": {
                "action": "Report Data",
                "frequency": "Daily",
                "category": "Low"
                }
            }
            }
        },
        "4": {
            "service_name": "LG",
            "service_type": "Product Provider",
            "cate_service": {
            "0": {
                "Device Usage": {
                "action": "Read Data",
                "frequency": "Weekly",
                "category": "Low"
                },
                "Viewing Habits": {
                "action": "View Data",
                "frequency": "Daily",
                "category": "High"
                }
            }
            }
        }
        }
    }
    return redirect('/')
@bp.route("/get", methods=["GET"])
def get():
    return "get raw_data"


@bp.route("/form/<int:device_id>", methods=["GET", "POST"])
def form(device_id):
    if request.method == "POST":
        # print(f"data from form : {request.form}")
        # yes = "yes"
        # no = "no"
        # for d in request.form:
        #     print(
        #         f"{d} : {request.form[d]} , action: {yes if 'action_' in d else no }, frequency: {yes if 'frequency_' in d else no}"
        #     )
        data = {}
        for d in request.form:

            raw_data = ""
            if "action_" in d:
                raw_data = d.replace("action_", "")
            elif "frequency_" in d:
                raw_data = d.replace("frequency_", "")
            elif "sensitivity_" in d:
                raw_data = d.replace("sensitivity_" ,"")
            
            if raw_data not in data.keys():
                data[raw_data] = {"action": "" , "frequency" : "", "sensitivity" : ""}

            if "action_" in d:
                data[raw_data]["action"] = request.form[d]
            elif "frequency_" in d:
                data[raw_data]["frequency"] = request.form[d]
            elif "sensitivity_" in d:
                data[raw_data]["sensitivity"] = request.form[d]

        # print(f"data: {data}")

        session["devices"][str(device_id)]["raw_data"] = data

        return redirect(url_for("device.device_page"))

    if request.method == "GET":

        return render_template(
            "forms/raw_data_form.html",
            device_id=str(device_id),   
            frequency=frequency,
            action=raw_data_action,
            sensitivity=cate_raw_data,
        )

    return "Cate Raw Data Form"

@bp.route("/ajax/<int:device_id>", methods=["POST"])
def ajax(device_id):
    print(f"data from form : {request.form}")
    
    cookie_value = request.cookies.get('user')
    raw_data = request.form['raw_data']
    # if "raw_data" not in session[cookie_value]["devices"][str(device_id)]:
    #     session[cookie_value]["devices"][str(device_id)]["raw_data"] = list([])
    # else:
    #     session[cookie_value]["devices"][str(device_id)]["raw_data"] =[session[cookie_value]["devices"][str(device_id)]["raw_data"]]
    prepareData = {"action": "" , "frequency" : "", "sensitivity" : ""}
    prepareData["action"] = request.form["action"]
    prepareData["frequency"] = request.form["frequency"]
    prepareData["sensitivity"] = request.form["sensitivity"]
    if 'raw_data' not in session[cookie_value]["devices"][str(device_id)]:
        session[cookie_value]["devices"][str(device_id)]["raw_data"]={raw_data:list([])}
    session[cookie_value]["devices"][str(device_id)]["raw_data"][raw_data].append(prepareData)
    return session[cookie_value]["devices"][str(device_id)]["raw_data"]


@bp.route("/getData/<int:device_id>", methods=["GET"])
def getData(device_id):
    isData = 1
    cookie_value = request.cookies.get('user')
    if "raw_data" in session[cookie_value]["devices"][str(device_id)]:
        rawData = session[cookie_value]["devices"][str(device_id)]["raw_data"]
    else:
        rawData = None
        isData = 0

    data = {
        "device_id":str(device_id),   
        "frequency":frequency,
        "action":raw_data_action,
        "sensitivity":cate_raw_data,
        "raw_data":rawData,
        "is_raw_data": isData
    }
    return data
@bp.route("/getAll", methods=["GET"])
def getAll():
    # if "raw_data" in session["devices"][str(device_id)]:
    #     rawData = session["devices"][str(device_id)]["raw_data"]
    # else:
    #     rawData = session["devices"][str(device_id)]
    cookie_value = request.cookies.get('user')
    if "devices" in session[cookie_value].keys():
        return session[cookie_value]["devices"]
    else:
        return ''



@bp.route("/delete", methods=["GET"])
def delete():
    cookie_value = request.cookies.get('user')
    try:
        if(cookie_value == None):
            return render_template("user_select.html",user="not-show-path")
        if "raw_data" in session[cookie_value].keys():
            del session[cookie_value]["raw_data"]
        return redirect(url_for("device.device_page"))
    except Exception as e:
        return render_template("user_select.html",user="not-show-path")
