from plutonkit.framework.tymplu.the_short_cut_word import TheShortCutWord
from plutonkit.framework.tymplu.the_template import TheTemplate


def convert_template(content: str, args,block) -> str:
    nwcls = TheTemplate(content, args,block)

    return nwcls.content


def convert_shortcode(content: str, args) -> str:
    nwcls = TheShortCutWord(content, args)

    return nwcls.get_convert()
