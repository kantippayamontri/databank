from flask import Flask, render_template, request


def create_app():
    app = Flask(
        __name__,
    )

    type_device = ["Security Camera", "Smartmetre", "Light"]

    cate_raw_data = ["low", "medium", "high"]

    cate_service = ["low", "medium", "high"]

    action = ["average", "anonymise", "transfer"]

    service_type= [
        "Advertising Company",
        "Health Tracking Service",
        "Medical Service",
        "Insurance",
        "Social Network Platform",
        "Tech Company",
    ]

    @app.route("/", methods=["POST", "GET"])
    def main_page():
        if request.method == "GET":
            return render_template(
                "main_page.html",
                type_device=enumerate(type_device),
                cate_raw_data=enumerate(cate_raw_data),
                cate_service=enumerate(cate_service),
                action=enumerate(action),
                service_type=enumerate(service_type),
            )
        elif request.method == "POST":
            _type_device = request.form["type_device"]
            _cate_raw_data = request.form["cate_raw_data"]
            _cate_service = request.form["cate_service"]
            _action = request.form["action"]
            _service_type = request.form["service_type"]

            return "".join(
                [
                    f"type of device : {_type_device}<br>",
                    f"cate of raw data : {_cate_raw_data}<br>",
                    f"cate of cate service: {_cate_service}<br>",
                    f"cate of action: {_action}<br>",
                    f"cate of service type: {_service_type}<br>",
                ]
            )
    
    def create_graph(data:dict):
         
        return

    @app.route("/hello")
    def hello():

        return "Hello, world"

    return app
