import random
import string


def unique_value_generator(length=15)->string:

    characters = string.ascii_letters + string.digits

    replace_char=''.join(random.choice(characters) for _ in range(length))
    return f"#%{replace_char}%#"

def convert_unique_value(raw_contents="",replace_char="")->string:

    raw_contents_split = raw_contents.split("\n")
    raw_contents = "\n".join([ x for x in raw_contents_split if x != replace_char  ])
    raw_contents= raw_contents.replace(replace_char, "")
    return raw_contents
