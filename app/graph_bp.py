import random
import string
from pathlib import Path

import graphviz
from flask import (
    Blueprint,
    jsonify,
    redirect,
    render_template,
    request,
    session,
    url_for,
)
from PIL import Image

bp = Blueprint("graph", __name__, url_prefix="/graph")


@bp.route("/show_graph", methods=["GET"])
def show_graph():
    # print(f"!!! Show Graph !!!")
    filename = create()
    resize_image(image_path=url_for("static", filename=filename), new_width=2000) # resize image to max width 2000 pixel
    # return filename
    return render_template("show_graph.html", graph_filename=filename)


def resize_image(image_path, new_width=None, new_height=None):
    image_path = "app/" + image_path
    print(f"image path: {image_path}")
    image = Image.open(str(image_path))
    original_width, original_height = image.size

    if new_width and new_height:
        raise ValueError("Only one of new_width or new_height can be specified.")

    if new_width:
        aspect_ratio = original_width / original_height
        new_height = int(new_width / aspect_ratio)
    else:
        aspect_ratio = original_height / original_width
        new_width = int(new_height * aspect_ratio)

    resized_image = image.resize((new_width, new_height))
    resized_image.save(image_path)  # Change the filename as needed


def create():
    # print(f"in function create")
    # check that have all value
    all_keys = ["device", "raw_data", "cate_service", "service"]
    for key in all_keys:
        if key not in session.keys():
            resp = jsonify({"filename": ""})
            resp.status_code = 200
            return resp

    data = {
        "device": session["device"],
        "raw_data": session["raw_data"],
        "cate_service": session["cate_service"],
        "service": session["service"],
    }

    data_graph = DataGraph(data=data)
    img_filename = data_graph.plot_graph()

    return img_filename

    # print(f"img_filename: {img_filename}")

    # return redirect(url_for("main_page", graph_filename=img_filename))

    # return render_template( "index.html", graph_filename = img_filename)

    # resp = jsonify({"filename": img_filename})
    # resp.status_code = 200

    # return resp
    # return redirect(url_for("main_page", graph_filename=img_filename))


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


class DataGraph:
    def __init__(self, data):
        self.data = data
        self.graph = graphviz.Digraph(
            comment="databank", format="png", graph_attr={"rankdir": "LR", "dpi": "300"}
        )
        self.create_graph()

    def create_graph(self):
        # for entry in self.data:
        if True:
            entry = self.data
            device_type = entry["device"]["device_type"]
            device_name = entry["device"]["device_name"]
            # Add device node (1st node)
            self.add_device_node(device_name, device_type)
            # Add unprocessed data nodes (2nd nodes)
            unprocessed_data = entry["device"]["device_unprocessed"]
            self.add_unprocessed_data_nodes(device_name, unprocessed_data)

            # Connect device node with unprocessed data nodes
            for data_item in unprocessed_data:
                unprocessed_data_node_name = (
                    f"{device_name}_{data_item.replace(' ', '_')}_UnprocessedData"
                )
                self.graph.edge(
                    device_name, unprocessed_data_node_name, dir="none", penwidth="3"
                )

                # Add sensitivity nodes (3rd nodes)
                sensitivity_level = entry["raw_data"][data_item]["sensitivity"]
                self.add_sensitivity_node(device_name, sensitivity_level, data_item)

                # Add action nodes
                sensitivity_action = entry["raw_data"][data_item]["action"]
                self.add_action_node(device_name, sensitivity_action, data_item)

                # Connect unprocessed data nodes with sensitivity nodes
                self.graph.edge(
                    unprocessed_data_node_name,
                    f"{device_name}_{data_item}_Sensitivity",
                    dir="none",
                    penwidth="3",
                )

                # Add the 5th node (combined node)
                combined_node_name = f"{device_name}_{data_item}_{sensitivity_level}_{sensitivity_action}_Combined"
                self.add_combined_node(
                    device_name, sensitivity_level, sensitivity_action, data_item
                )
                # Add edge between action node and combined node
                self.graph.edge(
                    f"{device_name}_{data_item}_{sensitivity_action}_Action",
                    combined_node_name,
                    dir="none",
                    penwidth="3",
                )

                # Add the 6th node (independent node)
                self.add_independent_node(device_name, data_item, sensitivity_action)
                # Add edge between independent node and combined node
                self.graph.edge(
                    f"{device_name}_{data_item}_{sensitivity_action}_Independent",
                    combined_node_name,
                    dir="none",
                    penwidth="3",
                )

                # Add edges between 7th nodes (cate_service) and 5th nodes (combined)
                if "cate_service" in entry:
                    cate_service = entry["cate_service"]
                    if data_item in cate_service:
                        service_data = cate_service[data_item]
                        action = service_data["action"]
                        # Add the cate_service node
                        cate_service_node_name = (
                            f"{device_name}_{data_item}_{action}_CateService"
                        )
                        self.graph.node(
                            cate_service_node_name,
                            label=action,
                            style="filled",
                            fillcolor="lightblue",
                            fontsize="24",
                            fontcolor="black",
                            fontname="bold",
                            shape="circle",
                        )
                        # Connect the cate_service node with the corresponding combined node
                        self.graph.edge(
                            combined_node_name,
                            cate_service_node_name,
                            dir="none",
                            penwidth="3",
                        )
                    else:
                        print(f"No cate_service data found for {data_item}.")
                    # Add the 8th node (category node)
                    category = service_data["category"]
                    category_node_name = self.add_category_node(
                        device_name, data_item, action, category
                    )
                    # Connect the category node with the cate_service node
                    self.graph.edge(
                        cate_service_node_name,
                        category_node_name,
                        dir="none",
                        penwidth="3",
                    )

                    # Add the 9th node (service_type node)
                    service_type = entry["service"]["service_type"]
                    service_type_node_name = self.add_service_type_node(
                        device_name, data_item, action, service_type
                    )
                    # Connect the service_type node with the category node
                    self.graph.edge(
                        category_node_name,
                        service_type_node_name,
                        dir="none",
                        penwidth="3",
                    )

                    # Add the 10th node (service_name node)
                    service_name = entry["service"]["service_name"]
                    service_name_node_name = self.add_service_name_node(
                        device_name, data_item, action, service_name
                    )
                    # Connect the service_name node with the service_type node
                    self.graph.edge(
                        service_type_node_name,
                        service_name_node_name,
                        dir="none",
                        penwidth="3",
                    )

    # Add device node (1st node)
    def add_device_node(self, device_name, device_type):
        label = f"Type of Device: {device_type}\nName of Device: {device_name}"
        self.graph.node(
            device_name,
            label=label,
            style="filled",
            fillcolor="lightgreen",
            fontsize="24",
            fontcolor="black",
            fontname="bold",
            shape="circle",
        )

    # Add unprocessed data nodes (2nd nodes)
    def add_unprocessed_data_nodes(self, device_name, unprocessed_data):
        for data_item in unprocessed_data:
            node_name = f"{device_name}_{data_item.replace(' ', '_')}_UnprocessedData"
            node_label = f"Unprocessed Data: {data_item}"
            self.graph.node(
                node_name,
                label=node_label,
                style="filled",
                fillcolor="lightgreen",
                fontsize="24",
                fontcolor="black",
                fontname="bold",
                shape="circle",
            )

    # Add sensitivity nodes (3rd nodes)
    def add_sensitivity_node(self, device_name, sensitivity_level, data_item):
        node_name = f"{device_name}_{data_item}_Sensitivity"
        self.graph.node(
            node_name,
            label=f"Sensitivity: {sensitivity_level}",
            style="filled",
            fillcolor="lightgreen",
            fontsize="24",
            fontcolor="black",
            fontname="bold",
            shape="circle",
        )

    # Add action nodes (4th nodes)
    def add_action_node(self, device_name, action, data_item):
        node_name = f"{device_name}_{data_item}_{action}_Action"
        self.graph.node(
            node_name,
            label=f"Action: {action}",
            style="filled",
            fillcolor="lightgreen",
            fontsize="24",
            fontcolor="black",
            fontname="bold",
            shape="circle",
        )
        # Connect action nodes with sensitivity nodes
        self.graph.edge(
            f"{device_name}_{data_item}_Sensitivity",
            node_name,
            dir="none",
            penwidth="3",
        )

    # Add combined nodes (5th nodes)
    def add_combined_node(
        self, device_name, sensitivity_output, raw_data_action, data_item
    ):
        node_name = (
            f"{device_name}_{data_item}_{sensitivity_output}_{raw_data_action}_Combined"
        )
        self.graph.node(
            node_name,
            label=f"{sensitivity_output}\n{raw_data_action}",
            style="filled",
            fillcolor="orange",
            fontsize="24",
            fontcolor="black",
            fontname="bold",
            shape="circle",
        )

    # Add independent nodes (6th nodes)
    def add_independent_node(self, device_name, data_item, sensitivity_action):
        node_name = f"{device_name}_{data_item}_{sensitivity_action}_Independent"
        node_label = f"{sensitivity_action}\n{data_item}"
        self.graph.node(
            node_name,
            label=node_label,
            style="filled",
            fillcolor="orange",
            fontsize="24",
            fontcolor="black",
            fontname="bold",
            shape="circle",
        )

    # Add the 8th node (action of service)
    def add_category_node(self, device_name, data_item, action, category):
        category_node_name = f"{device_name}_{data_item}_{action}_Category"
        category_label = f"Category: {category}"
        self.graph.node(
            category_node_name,
            label=category_label,
            style="filled",
            fillcolor="lightblue",
            fontsize="24",
            fontcolor="black",
            fontname="bold",
            shape="circle",
        )
        return category_node_name

    # Add the 9th node (service_type node)
    def add_service_type_node(self, device_name, data_item, action, service_type):
        node_name = f"{device_name}_{data_item}_{action}_ServiceType"
        node_label = f"Service Type: {service_type}"
        self.graph.node(
            node_name,
            label=node_label,
            style="filled",
            fillcolor="lightblue",
            fontsize="24",
            fontcolor="black",
            fontname="bold",
            shape="circle",
        )
        return node_name

    # Add the 10th node (service_name node)
    def add_service_name_node(self, device_name, data_item, action, service_name):
        node_name = f"{device_name}_{data_item}_{action}_ServiceName"
        node_label = f"Service Name: {service_name}"
        self.graph.node(
            node_name,
            label=node_label,
            style="filled",
            fillcolor="lightblue",
            fontsize="24",
            fontcolor="black",
            fontname="bold",
            shape="circle",
        )
        return node_name

    def plot_graph(self):
        filename = generate_random_filename()
        filename_path = f"./app/static/{filename}"
        self.graph.render(filename=filename_path, format="png", view=False)
        graph_img_filename = f"{filename}.png"
        return graph_img_filename


# class DataGraph:
#    def __init__(self, data):
#        self.data = data
#        # print(f"self.data: {self.data}")
#        self.graph = graphviz.Digraph(
#            comment="databank", format="png", graph_attr={"rankdir": "LR", "dpi": "600"}
#        )
#        self.create_graph()
#
#    def create_graph(self):
#        # for entry in self.data:
#        if True:
#            entry = self.data
#            # Extract device information
#            device_type = entry["device"]["device_type"]
#            device_name = entry["device"]["device_name"]
#
#            # Add device node
#            self.graph.node(
#                device_name,
#                label=f"Type of Device: {device_type}\nName of Device: {device_name}",
#            )  # edit this
#
#            # Add node for unprocessed data
#            unprocessed_data = entry["device"]["device_unprocessed"]
#            unprocessed_data_label = f"Unprocessed Data: {', '.join(unprocessed_data)}"
#            self.graph.node(
#                f"{device_name}_UnprocessedData", label=unprocessed_data_label
#            )
#
#            # Process cate_raw_data to get sensitivity output
#            raw_data_frequency = entry["raw_data"]["frequency"]
#            raw_data_action = entry["raw_data"]["action"]
#            sensitivity_output = self.process_sensitivity(
#                raw_data_frequency, raw_data_action
#            )
#
#            # Add node for cate_raw_data output (sensitivity)
#            sensitivity_label = f"Sensitivity: {sensitivity_output}"
#            self.graph.node(f"{device_name}_Sensitivity", label=sensitivity_label)
#
#            raw_data_action_label = f"{raw_data_action}"
#            self.graph.node(f"{device_name}_RawDataAction", label=raw_data_action_label)
#
#            # Add node for connect function
#            connected_function_label = f"{sensitivity_output}{raw_data_action}"
#            print(connected_function_label)
#            self.graph.node(f"{device_name}_Function", label=connected_function_label)
#
#            # Add node for independent node
#            indy_node = f"{raw_data_action}\n{', '.join(unprocessed_data)}"
#            self.graph.node(f"{device_name}_Data", label=indy_node)
#
#            """
#            Service part
#            """
#            service_frequency = entry["cate_service"]["frequency"]
#            service_action = entry["cate_service"]["action"]
#
#            # Process cate_service to get trust level
#            trust_level = self.process_trust(service_frequency, service_action)
#
#            # node Trust
#            trust_label = f"Trust level: {trust_level}"
#            self.graph.node(f"{device_name}_Trust", label=trust_label)
#
#            # Add node for service action
#            service_action_label = f"Service Action: {service_action}"
#            self.graph.node(f"{device_name}_cate_service", label=service_action_label)
#
#            # Add service type
#            service_type = entry["service"]["service_type"]
#            service_name = entry["service"]["service_name"]
#
#            service_type_label = f"{service_type}"
#            self.graph.node(f"{device_name}_Service_Type", label=service_type_label)
#            service_name_label = f"{service_name}"
#            self.graph.node(f"{device_name}_Service_Name", label=service_name_label)
#
#            # Add edges
#            self.graph.edge(device_name, f"{device_name}_UnprocessedData", dir="none")
#            self.graph.edge(
#                f"{device_name}_UnprocessedData",
#                f"{device_name}_Sensitivity",
#                dir="none",
#            )
#            self.graph.edge(
#                f"{device_name}_Sensitivity", f"{device_name}_RawDataAction", dir="none"
#            )
#            self.graph.edge(
#                f"{device_name}_RawDataAction", f"{device_name}_Function", dir="none"
#            )
#            self.graph.edge(
#                f"{device_name}_Data", f"{device_name}_Function", dir="none"
#            )
#            self.graph.edge(
#                f"{device_name}_Function", f"{device_name}_cate_service", dir="none"
#            )
#            self.graph.edge(
#                f"{device_name}_cate_service", f"{device_name}_Trust", dir="none"
#            )
#            self.graph.edge(
#                f"{device_name}_Trust", f"{device_name}_Service_Type", dir="none"
#            )
#            self.graph.edge(
#                f"{device_name}_Service_Type", f"{device_name}_Service_Name", dir="none"
#            )
#
#    """
#    Generate function the sensitivity level from category of raw data. The params is random "frequency" and "Action"
#    """
#
#    def process_sensitivity(self, frequency, action):
#
#        sensitivity_levels = {
#            "Daily": {"Transfer": "Medium", "Average": "low", "Anonymise": "low"},
#            "Weekly": {"Transfer": "High", "Average": "low", "Anonymise": "low"},
#            "Monthly": {"Transfer": "High", "Average": "High", "Anonymise": "low"},
#            "Yearly": {"Transfer": "High", "Average": "High", "Anonymise": "High"},
#        }
#
#        sensitivity_level = sensitivity_levels.get(frequency, {}).get(action, "Unknown")
#
#        return sensitivity_level
#
#    """
#    Generate function of trust level from category of service. The params is random "frequency" and "Action"
#    """
#
#    def process_trust(self, frequency, action):
#
#        trust_levels = {
#            "Daily": {"View": "Low"},
#            "Weekly": {"View": "Medium"},
#            "Monthly": {"View": "Medium"},
#            "Yearly": {"View": "High"},
#        }
#
#        trust_level = trust_levels.get(frequency, {}).get(action, "Unknown")
#
#        return trust_level
#
#    def plot_graph(self):
#        filename = generate_random_filename()
#        filename_path = f"./app/static/{filename}"
#        self.graph.render(filename=filename_path, format="png", view=True)
#        graph_img_filename = f"{filename}.png"
#        return graph_img_filename
#        # self.graph.render(filename="graph", format="png", view=False)
#
