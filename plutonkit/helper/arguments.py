def get_dict_value(key, obj):
    raw_key = key[0].strip()
    key.pop(0)
    if len(key) > 0:
        if obj.get(raw_key) is not None:
            return get_dict_value(key, obj.get(raw_key))
    return obj.get(raw_key)
