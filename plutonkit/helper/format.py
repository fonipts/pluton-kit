import re


def git_name(name):
    rep_name = re.sub(r"^([\///])", "", name).strip()
    rep_name = re.sub(r"([\///])$", "", rep_name)

    return rep_name
