def get_config(reference_value):
    config = {}
    for val in reference_value["command"]:
        config[val["type"]] = val["name"]
    return config
