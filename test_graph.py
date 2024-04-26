import graphviz

data = {
    "type_device": {
        "data": ["Security Camera", "Smartmetre", "Light"],
        "choose": "Light",
    },
    "cate_raw_data": {"data": ["low", "medium", "high"], "choose": "low"},
    "cate_service": {"data": ["low", "medium", "high"], "choose": "high"},
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
        "choose": "Insurance",
    },
}

# graph = graphviz.Digraph(comment="databank",format="png")
# for k in data.keys():
#     graph.node(k ,k)
#     print(k)
# plt.show()

############################## TONMAI EDIT ####################################


graph = graphviz.Digraph(comment="databank", format="png")

for category, category_data in data.items():
    chosen_value = next(
        (item for item in category_data["data"] if item == category_data["choose"]), None)
    category_name = category.replace("_", " ").capitalize()
    label = f"{category_name} : {
        chosen_value}" if chosen_value else category_name
    graph.node(category, label=label, shape="box")

keys = list(data.keys())
for i in range(len(keys) - 1):
    graph.edge(keys[i], keys[i + 1])

graph.render(filename="graph", format="png", view=True)


"""
data = {
    "type_device": {
        "data": ["Security Camera", "Smartmetre", "Light"],
        "choose": "Security Camera",
    },
    "cate_raw_data": {"data": ["low", "medium", "high"], "choose": "low"},
    "cate_service": {"data": ["low", "medium", "high"], "choose": "high"},
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
        "choose": "Insurance",
    },
}

: 
type_device : box of "Security Camera", box of "Smartmetre", box of "Light"
cate_raw_data : box of  "low", box of  "medium", box of  "high"
cate_service : box of  "low", box of  "medium", box of "high"
action : box of  "average", box of  "anonymise", box of  "transfer"
service_type : box of "Advertising Company", box of "Health Tracking Service",box of "Medical Service",box of "Insurance",box of "Social Network Platform",box of "Tech Company"


"""
