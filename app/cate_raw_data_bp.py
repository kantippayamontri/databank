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
    if "raw_data" in session[cookie_value]["devices"][str(device_id)]:
        data = session[cookie_value]["devices"][str(device_id)]["raw_data"]
    else:
        data = session[cookie_value]["devices"][str(device_id)]["raw_data"] = []
    if data == []:
        data = {}
    data[raw_data] = {"action": "" , "frequency" : "", "sensitivity" : ""}
    data[raw_data]["action"] = request.form["action"]
    data[raw_data]["frequency"] = request.form["frequency"]
    data[raw_data]["sensitivity"] = request.form["sensitivity"]

    session[cookie_value]["devices"][str(device_id)]["raw_data"] = data

    return session[cookie_value]["devices"][str(device_id)]["raw_data"]

@bp.route("/getData/<int:device_id>", methods=["GET"])
def getData(device_id):
    isData = 1
    cookie_value = request.cookies.get('user')
    if "raw_data" in session[cookie_value]["devices"][str(device_id)]:
        rawData = session[cookie_value]["devices"][str(device_id)]["raw_data"]
    else:
        rawData = session[cookie_value]["devices"][str(device_id)]
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
    if "raw_data" in session[cookie_value].keys():
        del session[cookie_value]["raw_data"]
    return redirect(url_for("device.device_page"))
