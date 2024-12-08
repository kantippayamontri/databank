type_device = ["Security Camera", "Smartmetre", "Light"]

unprocessed_data = ["Footage", "Energy usage", "Light status", "Colour", "Notification", "Temperature", "Activity period"]

type_device_details = {
    "Security Camera": ["Footage","Energy Usage" ],
    "Smartmetre": ["Energy Usage", "Notification", "Temperature",],
    "Light": ["Light Status", "Color", "Activity period"],
}

cate_raw_data = ["Low", "Medium", "High"]

cate_service = ["Low", "Medium", "High"]

raw_data_action = ["Average", "Anonymise", "Encrtpt", "Upload", "Blur"]

service_action = ["View Data","Read Data", "Report Data", "Send Notification",]


service_type = [
    "Advertising Company",
    "Health Tracking Service",
    "Medical Service",
    "Insurance",
    "Social Network Platform",
    "Tech Company",
    "Family Member",
    "Authority",
    "Energy Suplier",
    "Product Provider"
]

frequency = [
    "Daily",
    "Weekly",
    "Yearly",
    "No fix time",
]