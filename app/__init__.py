from flask import Flask, render_template, request, jsonify
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

    action_detail = [
        "daily",
        "weekly",
        "yearly",
        "no fix time",
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
                action_detail=enumerate(action_detail),
                service_type=enumerate(service_type),
                
            )

    @app.route("/graph", methods=["POST"])
    def show_graph():

        if request.method == "POST":

            _type_device = request.form["type_device"]
            _cate_raw_data = request.form["cate_raw_data"]
            _cate_service = request.form["cate_service"]
            _action = request.form["action_choice"]
            _service_type = request.form["service_type"]

            data = {
                "type_device": {"data": type_device, "choose": _type_device},
                "cate_raw_data": {"data": cate_raw_data, "choose": _cate_raw_data},
                "cate_service": {"data": cate_service, "choose": _cate_service},
                "action": {"data": action, "choose": _action},
                "service_type": {"data": service_type, "choose": _service_type},
            }

            graph_img_filename = create_graph(data=data)

            return render_template("show_graph.html", graph_filename=graph_img_filename)
    
    def create_graph(data):

        device_data_types = {
            "Security Camera": "footage",
            "Smartmetre": "energy usage",
            "Light": "light status",
        }

        graph = graphviz.Digraph(
            comment="databank", format="png", graph_attr={"rankdir": "LR"}
        )

        # Add the first node "Type device"
        type_device = data["type_device"]["choose"]
        graph.node("Type_device", label=f"Type device : {type_device}")

        # Add the corresponding device data type node
        device_type = device_data_types.get(type_device, "")
        graph.node("Device_type", label=f"Device data type : {device_type}")

        # Add nodes for other categories
        for category, category_data in data.items():
            if category != "type_device":
                chosen_value = category_data["choose"]
                category_name = category.replace("_", " ").capitalize()
                label = f"{category_name} : {chosen_value}"
                graph.node(category, label=label)

        # Add edges from "Type device" to "Device data type" and from "Device data type" to the first selected category
        graph.edge("Type_device", "Device_type", dir="none")
        graph.edge("Device_type", "cate_raw_data", dir="none")
        graph.edge("cate_raw_data", "action", dir="none")

        # Add a new node representing the combination of "cate raw data" and "action"
        chosen_raw_data = data["cate_raw_data"]["choose"]
        chosen_action = data["action"]["choose"]
        raw_data_action_label = f"{chosen_raw_data} {chosen_action}"
        graph.node("cate_raw_data_action", label=raw_data_action_label)

        # Add edges to the new node "cate_raw_data_action"
        graph.edge("action", "cate_raw_data_action", dir="none")

        # Add the new independent node representing the combination of "action choosen value + Device data type value"
        independent_node_label = f"{chosen_action} {device_type}"
        graph.node("independent_node", label=independent_node_label)

        # Add edge from "independent_node" to "cate_raw_data_action" with constraint=false
        graph.edge("independent_node", "cate_raw_data_action", dir="none")

        # Add a blank node between "cate_raw_data_action" and "cate_service"
        graph.node("blank_node", label="Service Action : View", width="0", height="0")

        # Add edge from "cate_raw_data_action" to "blank_node"
        graph.edge("cate_raw_data_action", "blank_node", dir="none")

        # Add edge from "blank_node" to "cate_service"
        graph.edge("blank_node", "cate_service", dir="none")

        # Add the rest of the edges
        graph.edge("cate_service", "service_type", dir="none")

        # Add a blank node between "cate_raw_data_action" and "cate_service"
        graph.node(
            "blank_node2", label="Service : Meta Platforms, Inc.", width="0", height="0"
        )

        # Add edge from "cate_raw_data_action" to "blank_node"
        graph.edge("service_type", "blank_node2", dir="none")

        # Render and display the graph
        # graph.render(filename="graph", format="png", view=True)

        filename = generate_random_filename()
        filename_path = f"./app/static/{filename}"
        graph.render(filename=filename_path, format="png", view=False)
        graph_img_filename = f"{filename}.png"

        return graph_img_filename 

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
