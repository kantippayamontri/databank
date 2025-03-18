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

from .models import User

from app.app import db

from sqlalchemy import text

bp = Blueprint("category", __name__, url_prefix="/category")

@bp.route("/show", methods=["GET"])
def show():
    result = db.session.execute(text("SELECT * FROM data_preprocessing_category"))
    data = result.fetchall()
    data_count = len(data)
    result_service = db.session.execute(text("SELECT * FROM service_categories"))
    data_service = result_service.fetchall()
    data_count_service = len(data)
    return render_template('category.html',data=enumerate(data),data_count=data_count,data_service=enumerate(data_service),data_count_service=data_count_service)
