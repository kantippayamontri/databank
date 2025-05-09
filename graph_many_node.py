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
    resize_image(
        image_path=url_for("static", filename=filename), new_width=2000
    )  # resize image to max width 2000 pixel
    # return filename
    return render_template("show_graph.html", graph_filename=filename)


def resize_image(image_path, new_width=None, new_height=None):
    image_path = "app/" + image_path
    # print(f"image path: {image_path}")
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

    # data = {
    #     "cate_service": {
    #         "Colour": {
    #             "action": "Report Data",
    #             "category": "Low",
    #             "frequency": "Daily",
    #         },
    #         "Energy usage": {
    #             "action": "Send Notification",
    #             "category": "High",
    #             "frequency": "No fix time",
    #         },
    #         "Gauge Value": {
    #             "action": "View Data",
    #             "category": "High",
    #             "frequency": "Daily",
    #         },
    #         "Light status": {
    #             "action": "View Data",
    #             "category": "High",
    #             "frequency": "Daily",
    #         },
    #     },
    #     "device": {
    #         "device_name": "Gauge",
    #         "device_type": "Digital Gauge",
    #         "device_unprocessed": [
    #             "Light status",
    #             "Energy usage",
    #             "Colour",
    #             "Gauge Value",
    #         ],
    #     },
    #     "raw_data": {
    #         "Colour": {
    #             "action": "Upload",
    #             "frequency": "Yearly",
    #             "sensitivity": "Medium",
    #         },
    #         "Energy usage": {
    #             "action": "Transfer",
    #             "frequency": "Yearly",
    #             "sensitivity": "High",
    #         },
    #         "Gauge Value": {
    #             "action": "Average",
    #             "frequency": "Weekly",
    #             "sensitivity": "High",
    #         },
    #         "Light status": {
    #             "action": "Anonymise",
    #             "frequency": "Weekly",
    #             "sensitivity": "Medium",
    #         },
    #     },
    #     "service": {"service_name": "The8thFloor", "service_type": "Tech Company"},
    # }

    # data = {
    #     "device": session["device"],
    #     "raw_data": session["raw_data"],
    #     "cate_service": session["cate_service"],
    #     "service": session["service"],
    # }
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
                        "device_unprocessed": "Light status",
                        "action": "View Data",
                        "category": "Low",
                        "frequency": "Daily"
                    }
                }
            }
        }
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
        # Initialize dictionaries to store service type and service name nodes
        self.service_type_node_name = None
        self.service_name_nodes = {}
        self.create_graph()
    def create_graph(self):
        # Define a set to keep track of connections between combined nodes and cate_service nodes
        connection_set = set()

        # for entry in self.data:
        if True:
            entry = self.data
            for key in entry["devices"]:
                device_type = entry["devices"][key]["device_type"]
                device_name = entry["devices"][key]["device_name"]
                #add unprocessed_data
                unprocessed_data = entry["devices"][key]["device_unprocessed"]
            # Add device node (1st node)
            self.add_device_node(device_name, device_type)
            # Add unprocessed data nodes (2nd nodes)
            self.add_unprocessed_data_nodes(device_name, unprocessed_data)

            for data_item in unprocessed_data:
                # Add unprocessed data nodes (2nd nodes)
                unprocessed_data_node_name = (
                    f"{device_name}_{data_item.replace(' ', '_')}_UnprocessedData"
                )
                self.graph.node(
                    unprocessed_data_node_name,
                    label=data_item,
                    style="filled",
                    fillcolor="lightgreen",
                    fontsize="24",
                    fontcolor="black",
                    fontname="bold",
                    shape="circle",
                )

                # Connect device node with unprocessed data nodes
                self.graph.edge(
                    device_name, unprocessed_data_node_name, dir="none", penwidth="3"
                )

                # Add sensitivity nodes (3rd nodes)
                sensitivity_level = entry["raw_data"][data_item]["sensitivity"]
                sensitivity_action = entry["raw_data"][data_item]["action"]
                sensitivity_frequency = entry["raw_data"][data_item]["frequency"]
                self.add_sensitivity_node(
                    device_name,
                    sensitivity_level,
                    data_item,
                    sensitivity_action,
                    sensitivity_frequency,
                )

                # Add action nodes
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
                    device_name,
                    sensitivity_level,
                    sensitivity_action,
                    data_item,
                    sensitivity_action,
                    sensitivity_frequency,
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

                if "cate_service" in entry:
                    cate_service = entry["cate_service"]
                    if data_item in cate_service:
                        service_data = cate_service[data_item]
                        action = service_data["action"]
                        category = service_data[
                            "category"
                        ]  # Retrieve category from service_data
                        frequency = service_data[
                            "frequency"
                        ]  # Retrieve frequency from service_data
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

                        # Add the 7th node (category node)
                        category_node_name = self.add_category_node(
                            device_name, data_item, action, frequency, category
                        )
                        # Connect the category node with the cate_service node
                        self.graph.edge(
                            cate_service_node_name,
                            category_node_name,
                            dir="none",
                            penwidth="3",
                        )

                        if self.service_type_node_name is None:
                            # Add the 8th node (service_type node), if not already added
                            service_type = entry["service"]["service_type"]
                            self.service_type_node_name = self.add_service_type_node(
                                device_name, data_item, action, service_type
                            )
                        # Connect the service_type node with the category node
                        self.graph.edge(
                            category_node_name,
                            self.service_type_node_name,
                            dir="none",
                            penwidth="3",
                        )

        # # Add the 9th node (service_name node), if not already added
        # service_name = entry["service"]["service_name"]
        # if data_item not in self.service_name_nodes:
        #     service_name_node_name = self.add_service_name_node(
        #         device_name, data_item, action, service_name
        #     )
        #     self.service_name_nodes[data_item] = service_name_node_name
        # else:
        #     service_name_node_name = self.service_name_nodes[data_item]
        # # Connect the service_name node with the service_type node
        # self.graph.edge(
        #     self.service_type_node_name,
        #     service_name_node_name,
        #     dir="none",
        #     penwidth="3",
        # )

    # Add device node (1st node)
    def add_device_node(self, device_name, device_type):
        label = f"{device_type}\n{device_name}"
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
            node_label = f"{data_item}"
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
    def add_sensitivity_node(
        self,
        device_name,
        sensitivity_level,
        data_item,
        sensitivity_action,
        sensitivity_frequency,
    ):
        node_name = f"{device_name}_{data_item}_Sensitivity"
        # Call determine_category method to get the category
        category = self.determine_category(
            sensitivity_action, sensitivity_frequency, sensitivity_level
        )
        node_label = f"{category}"
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

    # Function to determine category based on action, frequency, and sensitivity
    def determine_category(self, action, frequency, sensitivity):
        category_mapping = {
            ("Average", "Daily", "Low"): "Private",
            ("Transfer", "Daily", "Low"): "Private",
            ("Anonymise", "Daily", "Low"): "Private",
            ("Average", "Daily", "High"): "Protected",
            ("Transfer", "Daily", "High"): "Protected",
            ("Anonymise", "Daily", "High"): "Protected",
            ("Average", "Daily", "Medium"): "Secert",
            ("Transfer", "Daily", "Medium"): "Secert",
            ("Anonymise", "Daily", "Medium"): "Secert",
            ("Average", "Weekly", "Low"): "Confidential",
            ("Transfer", "Weekly", "Low"): "Confidential",
            ("Anonymise", "Weekly", "Low"): "Confidential",
            ("Average", "Weekly", "High"): "Restricted",
            ("Transfer", "Weekly", "High"): "Restricted",
            ("Anonymise", "Weekly", "High"): "Restricted",
            ("Average", "Monthly", "Low"): "Private",
            ("Transfer", "Monthly", "Low"): "Private",
            ("Anonymise", "Monthly", "Low"): "Private",
            ("Average", "Monthly", "High"): "Protected",
            ("Transfer", "Monthly", "High"): "Protected",
            ("Anonymise", "Monthly", "High"): "Protected",
            ("Average", "Monthly", "Medium"): "Protected",
            ("Transfer", "Monthly", "Medium"): "Protected",
            ("Anonymise", "Monthly", "Medium"): "Protected",
            ("Average", "Yearly", "Low"): "Confidential",
            ("Transfer", "Yearly", "Low"): "Confidential",
            ("Anonymise", "Yearly", "Low"): "Confidential",
            ("Average", "Yearly", "High"): "Restricted",
            ("Transfer", "Yearly", "High"): "Secret",
            ("Average", "Yearly", "High"): "Restricted",
            ("Upload", "Yearly", "Medium"): "Protected",

        }

        return category_mapping.get((action, frequency, sensitivity), "Private")

    # Add action nodes (4th nodes)
    def add_action_node(self, device_name, action, data_item):
        node_name = f"{device_name}_{data_item}_{action}_Action"
        self.graph.node(
            node_name,
            label=f"{action}",
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
        self,
        device_name,
        sensitivity_level,
        raw_data_action,
        data_item,
        sensitivity_action,
        sensitivity_frequency,
    ):
        # Determine category based on sensitivity level
        category = self.determine_category(
            sensitivity_action, sensitivity_frequency, sensitivity_level
        )
        node_name = (
            f"{device_name}_{data_item}_{sensitivity_level}_{raw_data_action}_Combined"
        )
        self.graph.node(
            node_name,
            label=f"{category}\n{raw_data_action}",
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

    # Add the 8th node (category node) based on action, frequency, and category
    def add_category_node(self, device_name, data_item, action, frequency, category):
        category_mapping = {
            ("View Data", "Daily", "Low"): "Complete",
            ("View Data", "Daily", "Medium"): "Medium trust",
            ("View Data", "Daily", "High"): "High trust",
            ("View Report", "Daily", "Low"): "Low trust",
            ("View Report", "Daily", "Medium"): "Medium trust",
            ("View Report", "Daily", "High"): "High trust",
            ("Read Data", "Daily", "Low"): "High distrust",
            ("Read Data", "Daily", "Medium"): "Low trust",
            ("Read Data", "Daily", "High"): "Medium trust",
            ("View Data", "Weekly", "Low"): "Low trust",
            ("View Data", "Weekly", "Medium"): "Medium trust",
            ("View Data", "Weekly", "High"): "High trust",
            ("View Report", "Weekly", "Low"): "High distrust",
            ("View Report", "Weekly", "Medium"): "Low trust",
            ("View Report", "Weekly", "High"): "Medium trust",
            ("Read Data", "Weekly", "Low"): "Distrust",
            ("Read Data", "Weekly", "Medium"): "High distrust",
            ("Read Data", "Weekly", "High"): "Low trust",
            ("View Data", "Monthly", "Low"): "High distrust",
            ("View Data", "Monthly", "Medium"): "Low trust",
            ("View Data", "Monthly", "High"): "Medium trust",
            ("View Report", "Monthly", "Low"): "Distrust",
            ("Report Data", "Daily", "Low"): "Medium trust",
            ("View Report", "Monthly", "Medium"): "Medium trust",
            ("View Report", "Monthly", "High"): "High trust",
            ("Read Data", "Monthly", "Low"): "Distrust",
            ("Read Data", "Monthly", "Medium"): "Distrust",
            ("Read Data", "Monthly", "High"): "Low trust",
            ("View Data", "Yearly", "Low"): "Distrust",
            ("View Data", "Yearly", "Medium"): "Medium trust",
            ("View Data", "Yearly", "High"): "High trust",
            ("View Report", "Yearly", "Low"): "Distrust",
            ("View Report", "Yearly", "Medium"): "Distrust",
            ("View Report", "Yearly", "High"): "Low trust",
            ("Read Data", "Yearly", "Low"): "Distrust",
            ("Read Data", "Yearly", "Medium"): "Distrust",
            ("Read Data", "Yearly", "High"): "Distrust",
        }

        category_node_name = f"{device_name}_{data_item}_{action}_Category"
        category_label = (
            f"{category_mapping.get((action, frequency, category), 'Low trust')}"
        )
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
        node_label = f"{service_type}"
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
        node_label = f"{service_name}"
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
        # self.graph.render(filename="graph2", format="png", view=False)
        filename = generate_random_filename()
        filename_path = f"./app/static/{filename}"
        self.graph.render(filename=filename_path, format="png", view=False)
        graph_img_filename = f"{filename}.png"
        return graph_img_filename

