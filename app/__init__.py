from flask import Flask, render_template, request
import matplotlib.pyplot as plt
from icecream import ic
import graphviz
import random
import string


def create_app():
    app = Flask(
        __name__,
    )
    type_device = ["Security Camera", "Smartmetre", "Light"]

    type_device_details = {
        "Security Camera": ["Footage"],
        "Smartmetre": ["Energy Usage"],
        "Light": ["Light Status", "Color"],
    }

    cate_raw_data = ["low", "medium", "high"]

    cate_service = ["low", "medium", "high"]

    action = ["average", "anonymise", "transfer"]

    service_type = [
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

            tree_data = {
                "type_device": {"data": type_device, "choose": _type_device},
                "cate_raw_data": {"data": cate_raw_data, "choose": _cate_raw_data},
                "cate_service": {"data": cate_service, "choose": _cate_service},
                "action": {"data": action, "choose": _action},
                "service_type": {"data": service_type, "choose": _service_type},
            }

            # ic(tree_data)

            graph_img_filename = create_graph(data=tree_data)
            # print(f"graph_img_filename: {graph_img_filename}")

            # print(f"tree_data: ", tree_data)

            # return "".join(
            #     [
            #         f"type of device : {_type_device}<br>",
            #         f"cate of raw data : {_cate_raw_data}<br>",
            #         f"cate of cate service: {_cate_service}<br>",
            #         f"cate of action: {_action}<br>",
            #         f"cate of service type: {_service_type}<br>",
            #     ]
            # )
            return render_template("show_graph.html", graph_filename=graph_img_filename)

    def create_graph(data: dict):

        graph = graphviz.Digraph(comment="databank", format="png")

        for category, category_data in data.items():
            chosen_value = next(
                (
                    item
                    for item in category_data["data"]
                    if item == category_data["choose"]
                ),
                None,
            )
            category_name = category.replace("_", " ").capitalize()
            label = (
                f"{category_name} : {chosen_value}" if chosen_value else category_name
            )
            graph.node(category, label=label, shape="box")

        keys = list(data.keys())
        for i in range(len(keys) - 1):
            graph.edge(keys[i], keys[i + 1])

        filename = generate_random_filename()
        filename_path = f"./app/static/{filename}"
        graph.render(filename=filename_path, format="png", view=False)
        return f"{filename}.png"

    def generate_random_filename(length=15):
        """
        Generates a random filename with a specified length.

        Args:
            length (int, optional): The desired length of the filename. Defaults to 15.

        Returns:
            str: A random filename string.
        """

        # Allowed characters for filenames (avoid special characters that might cause issues on some systems)
        allowed_chars = string.ascii_lowercase + string.digits + string.ascii_uppercase

        # Generate a random string of the specified length
        random_string = "".join(random.choice(allowed_chars) for i in range(length))

        # Ensure the filename starts with a letter (avoid issues with some OS file systems)
        if not random_string[0].isalpha():
            random_string = (
                random.choice(string.ascii_lowercase + string.ascii_uppercase)
                + random_string[1:]
            )

        return f"graph_{random_string}"

    @app.route("/clear")
    def clear_img():
        return "clear image success."

    @app.route("/hello")
    def hello():
        return "Hello, world"

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
