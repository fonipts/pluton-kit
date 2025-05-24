import os
import re

from plutonkit.framework.request.ValidateSource import ValidateSource


def template_load(content,sub_content): # pylint: disable=unused-argument
    valid_source = ValidateSource(content)
    data_content = ""
    is_valid_template = False

    if valid_source.arch_type == "local":
        directory = os.getcwd()
        try:
            path = os.path.join(directory, content.strip())
            base_name = os.path.splitext(path)
            if len(base_name) > 1:
                if re.match(r"^(.tpl)", base_name[1]):
                    is_valid_template = True
            f_read = open(path, "r", encoding="utf-8")
            data_content = str(f_read.read())
            f_read.close()
        except Exception as e:
            print("Invalid source:",e)

    return {
        "content": data_content,
        "is_valid_template": is_valid_template
    }

def template_content(content,sub_content): # pylint: disable=unused-argument
    return content
