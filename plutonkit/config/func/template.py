def template_content(content,sub_content): # pylint: disable=unused-argument
    return content

def template_python(content,sub_content):
    try:
        local_ns = {}
        local_ns["content"] = sub_content
        # pylint: disable-next=exec-used
        exec(content, None, local_ns)

        return local_ns["content"]
    except SyntaxError as e:  # [broad-exception-caught]
        print(e, "(error)", content)
        return ""
    except Exception as e:  # [broad-exception-caught]
        print(e, "(error)", content)
        return ""
