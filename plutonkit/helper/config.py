def get_config(reference_value):
    config = {}
    for val in reference_value["command"]:
        config[val["type"]] = val["name"]
    return config

def get_arg_cmd_value(args):
    local_obj = {}
    local_obj["extra"] = []

    for val in args:
        word_split = val.split("=")

        if len(word_split) > 0:
            local_obj[word_split[0]] = "=".join(word_split[1::])
        else:
            local_obj["extra"].append(val)

    return local_obj
