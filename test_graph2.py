import matplotlib.pyplot as plt
import graphviz
import random
 
data = {
    "type_device": {
        "data": ["Security Camera", "Smartmetre", "Light"],
        "choose": "Security Camera",
    },
    "cate_raw_data": {"data": ["low", "medium", "high"], "choose": "high"}, # Category of xxx
    "cate_service": {"data": ["low", "medium", "high"], "choose": "low"}, # Category of xxx
    "action": {"data": ["average", "anonymise", "transfer"], "choose": "transfer"},
    "service_type": {
        "data": [
            "Advertising Company",
            "Health Tracking Service",
            "Medical Service",
            "Insurance",
            "Social Network Platform",
            "Tech Company",
        ],
        "choose": "Tech Company",
    },
}
 
# graph = graphviz.Digraph(comment="databank",format="png")
# for k in data.keys():
#     graph.node(k ,k)
#     print(k)
# plt.show()
 
############################## TONMAI EDIT ####################################
 
"""
Plot Graph V 1.0
"""
# graph = graphviz.Digraph(comment="databank", format="png")
 
# for category, category_data in data.items():
#     chosen_value = next((item for item in category_data["data"] if item == category_data["choose"]), None)
#     category_name = category.replace("_", " ").capitalize()  
#     label = f"{category_name} : {chosen_value}" if chosen_value else category_name  
#     graph.node(category, label=label, shape="box")
 
# keys = list(data.keys())
# for i in range(len(keys) - 1):
#     graph.edge(keys[i], keys[i + 1])
 
# graph.render(filename="graph", format="png", view=True)
 
# graph = graphviz.Digraph(comment="databank", format="png")
 
"""
Plot Graph V 1.1
"""
# graph = graphviz.Digraph(comment="databank", format="png")
 
# # Add nodes for each category with all options
# keys = list(data.keys())
# for i in range(len(keys)):
#     category = keys[i]
#     category_data = data[category]
#     options = category_data["data"]
#     chosen_option = category_data["choose"]
#     category_name = category.replace("_", " ").capitalize()
 
#     # Add nodes 
#     for option in options:
#         label = f'"{option}"'
#         if option == chosen_option:
#             graph.node(f"{category}_{option}", label=label, shape="box", color="blue")
#         else:
#             graph.node(f"{category}_{option}", label=label, shape="box", color="red")
 
#     # Add edges 
#     if i > 0:
#         prev_category = keys[i - 1]
#         prev_chosen_option = data[prev_category]["choose"]
#         for option in options:
#             if category == "type_device":
#                 graph.edge(f"{prev_category}_{prev_chosen_option}", f"{category}_{option}", color="blue" if option == chosen_option else "red")
#             else:
#                 graph.edge(f"{prev_category}_{prev_chosen_option}", f"{category}_{option}", color="blue" if option == chosen_option else "red")
 
# # Render and display the graph
# graph.render(filename="graph", format="png", view=True)
 
"""
Plot V1.2
"""
device_data_types = {
    "Security Camera": "footage",
    "Smartmetre": "energy usage",
    "Light": "light status",
} 
 
graph = graphviz.Digraph(comment="databank", format="png", graph_attr={'rankdir': 'LR'})
 
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
graph.node("blank_node2", label="Service : Meta Platforms, Inc.", width="0", height="0")
 
# Add edge from "cate_raw_data_action" to "blank_node"
graph.edge("service_type", "blank_node2", dir="none")
 
# Render and display the graph
graph.render(filename="graph", format="png", view=True)
 
 
 
"""
User
type_device: Light -> device_data_types (light status) -> cate_raw_data (low) -> cate_service (high) -> action (transfer) -> service_type (Insurance)
"""