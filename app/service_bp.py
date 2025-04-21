from flask import Blueprint, jsonify, redirect, render_template, request, session, url_for, flash

from .utils import service_type

from app.app import db

from sqlalchemy import text

bp = Blueprint("service", __name__, url_prefix="/service")

@bp.route("/service_page", methods=["GET"])
def service_page():
    cookie_value = cookie_value = session.get('user_id')
    if cookie_value==None:
            return redirect('/')
    choose_service_name = ""
    choose_service_type = ""
    service_id = 0
    service_name_all = []
    result = db.session.execute(text("SELECT services.* FROM services where user_id="+str(cookie_value)+" order by id desc"))
    services = result.fetchall()
    # trust_level = []
    # for service in services:
    #     if service[2] not in trust_level:
    #         trust_level.append(service[2])
    # priority = {"high": 1, "medium": 2, "low": 3}
    # trust_level = sorted(trust_level, key=lambda x: priority[x])
    # if len(trust_level)==0:
    trust_level=['high','medium','low']
    # party_level = []
    # for service in services:
    #     if service[3] not in party_level:
    #         party_level.append(service[3])
    # priority = {"first party": 1, "support party": 2, "third party": 3}
    # party_level = sorted(party_level, key=lambda x: priority[x])
    # if len(party_level)==0:
    party_level=['first party','support party','third party']
    try:
        # if "services" in session[cookie_value].keys():
        #     service_id_max = max(list([int(k) for k in session[cookie_value]["services"].keys()]))
        #     service_id = service_id_max + 1

        #     # check service name is redundant
        #     service_name_all = list(
        #         [
        #             session[cookie_value]["services"][_service_id]["service_name"]
        #             for _service_id in session[cookie_value]["services"].keys()
        #             if _service_id != service_id
        #         ]
        #     )
        # if "devices" in session[cookie_value].keys():
        #     return render_template("service_page.html",
        #         service_name_all=service_name_all,
        #         service_id=str(service_id),
        #         service_type=service_type,
        #         device=session[cookie_value]["devices"],
        #         choose_service_name=choose_service_name,
        #         choose_service_type=choose_service_type,
        #         name=cookie_value)
        # else:
        #     return render_template("service_page.html",
        #         service_name_all=service_name_all,
        #         service_id=str(service_id),
        #         service_type=service_type,
        #         device=[],
        #         choose_service_name=choose_service_name,
        #         choose_service_type=choose_service_type,
        #         name=cookie_value)
        return render_template("service_page.html",party_levels=enumerate(party_level),trust_levels=enumerate(trust_level), services=services,sevice_count=len(services),name=cookie_value)
    except Exception as e:
        return render_template("user_select.html",user="not-show-path")
# @bp.route("/get_data", methods=["GET"])
# def get_data():

@bp.route("/form_submit/<int:service_id>", methods=["GET", "POST"])
def form_submit(service_id):

    if request.method == "POST":
        service_id = str(service_id)
        _service_name = request.form["service_name"]
        _service_type = request.form["service_type"]
        if "services" not in session.keys():
            session["services"] = {}

        # session["services"][service_id] = {
        #     "service_name": _service_name,
        #     "service_type": _service_type,
        # }
        if service_id not in session.get("services").keys():
            session["services"][service_id] = {}
            # check service is redundant
        for _service_id in session.get("services").keys():
            if _service_id == service_id:
                continue
            if "service_name" in session.get("services")[service_id].keys():
                if (
                    _service_name
                    == session.get("services")[_service_id]["service_name"]
                ):
                    _service_name = f"{_service_name}_(1)"

        session["services"][service_id]["service_name"] = _service_name
        session["services"][service_id]["service_type"] = _service_type

        return redirect(url_for("service.service_page"))

    return "Service Form Page"

@bp.route("/form_edit/<int:service_id>", methods=["GET", "POST"])
def form_edit(service_id):
    cookie_value = request.cookies.get('user')
    if request.method == "POST":
        service_id = str(service_id)
        _service_name = request.get_json()["service_name"]
        _trust_level = request.get_json()["trust_level"]
        _party_level = request.get_json()["party_level"]
        trust_level_array=['high','medium','low']
        party_level_array=['first_party','support_party','third_party']
        print(trust_level_array[int(_trust_level)-1],party_level_array[int(_party_level)-1])
        sql = text("UPDATE services set name=:name, trust_level=:trust_level, party_level=:party_level, party_level=:party_level where id="+str(service_id))
        params = {"name": _service_name, "trust_level": _trust_level, "party_level": _party_level}
        result = db.session.execute(sql, params)
        sql = text("delete from service_category_connect where service_id="+str(service_id))
        db.session.execute(sql)
        service_category = 0
        if trust_level_array[int(_trust_level)-1] == 'low' and (party_level_array[int(_party_level)-1] == 'third_party' or party_level_array[int(_party_level)-1] == 'support_party'):
            service_category=1
        elif trust_level_array[int(_trust_level)-1] == 'medium' and (party_level_array[int(_party_level)-1] == 'third_party' or party_level_array[int(_party_level)-1] == 'support_party'):
            service_category=2
        elif (trust_level_array[int(_trust_level)-1] == 'high' and (party_level_array[int(_party_level)-1] == 'third_party' or party_level_array[int(_party_level)-1] == 'support_party')) or party_level_array[int(_party_level)-1] == 'first_party':
            service_category=3
        sql = text("INSERT INTO service_category_connect (service_id,service_category_id) VALUES (:service_id, :service_category_id)")
        params = {"service_id": service_id, "service_category_id": service_category}
        db.session.execute(sql, params)
        db.session.commit()
        return jsonify(success=True)
    return "Service Form Page"

@bp.route("/form_add", methods=["POST"])
def form_add():
    cookie_value = session.get('user_id')
    _service_name = request.form["service_name"]
    _trust_level = request.form["trust_level"]
    _party_level = request.form["party_level"]
    # try:
    if(cookie_value == None):
        return redirect('/')
    sql = text("INSERT INTO services (name, trust_level, party_level, user_id) VALUES (:name, :trust_level, :party_level, :user_id)")
    params = {"name": _service_name, "trust_level": _trust_level, "party_level": _party_level, "user_id":cookie_value}
    result = db.session.execute(sql, params)
    service_id = result.lastrowid
    service_category = 0
    trust_level_array=['high','medium','low']
    party_level_array=['first_party','support_party','third_party']
    if trust_level_array[int(_trust_level)-1] == 'low' and (party_level_array[int(_party_level)-1] == 'third_party' or party_level_array[int(_party_level)-1] == 'support_party'):
        service_category=1
    elif trust_level_array[int(_trust_level)-1] == 'medium' and (party_level_array[int(_party_level)-1] == 'third_party' or party_level_array[int(_party_level)-1] == 'support_party'):
        service_category=2
    elif (trust_level_array[int(_trust_level)-1] == 'high' and (party_level_array[int(_party_level)-1] == 'third_party' or party_level_array[int(_party_level)-1] == 'support_party')) or party_level_array[int(_party_level)-1] == 'first_party':
        service_category=3
    sql = text("INSERT INTO service_category_connect (service_id,service_category_id) VALUES (:service_id, :service_category_id)")
    params = {"service_id": service_id, "service_category_id": service_category}
    db.session.execute(sql, params)
    db.session.commit()
    if(request.form["isTour"]== "1"):
        return redirect(url_for("service.service_page")+"?to=18")
    else:
        return redirect(url_for("service.service_page"))
    # except Exception as e:
    #     return render_template("user_select.html",user="not-show-path")

@bp.route("/form_page_new", methods=["GET"])
def form_page_new():
    cookie_value = request.cookies.get('user')
    choose_service_name = ""
    choose_service_type = ""
    service_id = 0
    service_name_all = []
    try:
        if(cookie_value == None):
            return render_template("user_select.html",user="not-show-path")
        if "services" in session[cookie_value].keys():
            service_id_max = max(list([int(k) for k in session[cookie_value]["services"].keys()]))
            service_id = service_id_max + 1

            # check service name is redundant
            service_name_all = list(
                [
                    session[cookie_value]["services"][_service_id]["service_name"]
                    for _service_id in session[cookie_value]["services"].keys()
                    if _service_id != service_id
                ]
            )

        return render_template(
            "forms/service_form.html",
            service_name_all=service_name_all,
            service_id=str(service_id),
            service_type=service_type,
            choose_service_name=choose_service_name,
            choose_service_type=choose_service_type,
        )

    except Exception as e:
        return render_template("user_select.html",user="not-show-path")

@bp.route("/form_page/<int:service_id>", methods=["GET"])
def form_page(service_id):
    # if "services" not in session[cookie_value].keys():
    #     return render_template("index.html")
    cookie_value = request.cookies.get('user')
    service_id = str(service_id)

    choose_service_type = ""
    choose_service_name = ""
    try:
        if(cookie_value == None):
            return render_template("user_select.html",user="not-show-path")
        if "services" in session[cookie_value].keys():
            if str(service_id) in session[cookie_value]["services"].keys():

                choose_service_type = session[cookie_value]["services"][str(service_id)]["service_type"]
                choose_service_name = session[cookie_value]["services"][str(service_id)]["service_name"]

                return render_template(
                    "forms/service_form.html",
                    service_id=str(service_id),
                    service_type=service_type,
                    choose_service_name=choose_service_name,
                    choose_service_type=choose_service_type,
                )
        else:
            return redirect(url_for("service.service_page"))
        
    except Exception as e:
            return render_template("user_select.html",user="not-show-path")


@bp.route("/delete/<string:service_id>", methods=["GET"])
def delete(service_id: str):
    cookie_value = request.cookies.get('user')
    # try:
    db.session.execute(text("delete from service_category_connect where service_id="+str(service_id)))
    db.session.execute(text("delete from services where id="+str(service_id)))
    db.session.commit()
    # if(cookie_value == None):
    #     return render_template("user_select.html",user="not-show-path")
    # if "services" in session[cookie_value].keys():
    #     del session[cookie_value]["services"][service_id]

    #     if session[cookie_value]["services"] == {}:
    #         del session[cookie_value]["services"]

    return redirect(url_for("service.service_page"))
    # except Exception as e:
    #     return render_template("user_select.html",user="not-show-path")
