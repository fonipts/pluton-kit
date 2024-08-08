import re

from .TemplateStruct import TemplateStruct


class TheTemplate:
    def __init__(self, content: str, args=None):
        self.args = args
        self.content = self.__wragle_data(content)

    def __command_details(self, name, contents,sub_content):

        lst = []
        first_count_space = 0
        for k,v in enumerate(contents):

            check_space = re.findall(r"^([\s\n]{0,})", v)

            space_count = len(check_space[0].split(" "))
            if k == 0:
                first_count_space = space_count
                lst.append(v.lstrip())  #
            else:
                lst.append(v.replace("".join(check_space[first_count_space:space_count-first_count_space]), ""))

        if name == "content":
            return "\n".join(lst)
        if name == "script":
            try:
                local_ns = {}
                local_ns["content"] = sub_content
                # pylint: disable-next=exec-used
                exec("\n".join(lst), None, local_ns)

                return local_ns["content"]
            except SyntaxError as e:  # [broad-exception-caught]
                print(e,"(error)","\n".join(lst))
                return ""
            except Exception as e:  # [broad-exception-caught]
                print(e,"(error)","\n".join(lst))
                return ""
        return ""

    def __wragle_data(self, content: str):
        find_value = re.findall(r"(\{\$)([a-zA-Z0-9_]{1,})(\})", content)
        if len(find_value) > 0:
            for val in find_value:
                content = content.replace("".join(val), self.args.get(val[1], ""))

        template_struct = TemplateStruct(content, self.args)
        for mv in template_struct.convert_template:
            sub_content = ""
            for sv in mv["component"]:
                sub_content += self.__command_details(sv["name"], sv["input"],sub_content)
            content = content.replace(mv["template"], sub_content)

        return content

    def get_content(self):
        return self.content
