from plutonkit.management.template.TheTemplate import TheTemplate
from plutonkit.management.template.TheShortCutWord import TheShortCutWord


def convert_template(content:str, args)->str:
    nwcls = TheTemplate(content, args)

    return nwcls.get_content()

def convert_shortcode(content:str, args)->str:
    nwcls = TheShortCutWord(content, args)

    return nwcls.get_convert()
