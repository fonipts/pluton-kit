from plutonkit.framework.template.TheShortCutWord import TheShortCutWord
from plutonkit.framework.template.TheTemplate import TheTemplate


def convert_template(content: str, args) -> str:
    nwcls = TheTemplate(content, args)

    return nwcls.get_content()


def convert_shortcode(content: str, args) -> str:
    nwcls = TheShortCutWord(content, args)

    return nwcls.get_convert()
