import re

from plutonkit.config.search import SEARCH_CHAR_ENCLOSE


def git_name(name):
    rep_name = re.sub(r"^([\///])", "", name).strip()
    rep_name = re.sub(r"([\///])$", "", rep_name)

    return rep_name

def spilt_char(content):
    raw_list =[]
    for val in content:

        bools = False
        for obVal in SEARCH_CHAR_ENCLOSE:
            if re.search(obVal["regex"], val):
                if bools is False:
                    name = obVal["name"]
                    raw_list.append(f"[:{name}]")
                bools = True
        if bools is False:
            raw_list.append(val)

    return "".join(raw_list)

def get_enclose_str(content,data):
    look_name = "none"
    for obVal in SEARCH_CHAR_ENCLOSE:
        obVal_name= obVal["name"]
        if re.search(re.compile(f"\\[:{obVal_name}\\]"), content):
            look_name = obVal_name

    if look_name != "none":
        match = re.search(re.compile(f"\\[:{look_name}\\](.*?)\\[:{look_name}\\]"), content)
        if match:
            raw_content = content.replace(match.group(0), "$%"+str(len(data))+"%$")
            data.append(match.group(0))
            return get_enclose_str(raw_content,data)
    return {
        "replace_ant":data,
        "content":content
    }

def replace_index_to_enclose(values):
    content = values["content"]
    cnt_search = 0
    for key,value in enumerate(values["replace_ant"]):
        if re.search("$%"+str(key)+"%$", content):
            cnt_search +=1
        content = content.replace("$%"+str(key)+"%$",value)

    for obVal in SEARCH_CHAR_ENCLOSE:
        content = content.replace("[:"+obVal["name"]+"]",obVal["value"])

    if cnt_search>0:
        values["content"] = content
        return replace_index_to_enclose(values)
    return content
