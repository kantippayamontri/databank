from flask import (
    Blueprint, 
    redirect, 
    render_template,
    request,
)

from .utils import frequency, service_action

bp = Blueprint("cate_service", __name__, "/cate_service")

@bp.route("/form", methods=["GET", "POST"])
def form():
    if request.method == "GET":
        ...
        
    if request.method == "POST":
        ...
        
    return "Service Form Page"
