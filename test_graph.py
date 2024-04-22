import networkx as nx
import matplotlib.pyplot as plt
import graphviz

data = {
    "type_device": {
        "data": ["Security Camera", "Smartmetre", "Light"],
        "choose": "Security Camera",
    },
    "cate_raw_data": {"data": ["low", "medium", "high"], "choose": "low"},
    "cate_service": {"data": ["low", "medium", "high"], "choose": "medium"},
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


graph = graphviz.Digraph(comment="databank",format="png")
for k in data.keys():
    graph.node(k ,k)

plt.show()