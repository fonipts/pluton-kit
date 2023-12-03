import re

class DjangoScript:
    def __init__(self,argSetting={},argUrl={}) -> None:
        self.argSetting=argSetting
        self.argUrl=argUrl
    def getSettings(self,content):

        arg_import = self.argSetting.get("import",[])
        arg_setting = self.argSetting.get("value",[])
        arg_append = self.argSetting.get("append",[])

        content ="\n".join([x for x in arg_import])+"\n"+content

        results = re.findall(r"(INSTALLED_APPS[\s\n]{0,}\=[\s\n]{0,}\[\n[\n\s\'\w\.\,]{0,}\])",content)

        get_replace_install = results[0]

        content_replace  = get_replace_install.replace("\n]","\n"+",\n".join([ '"'+x+'"' for x in arg_setting])+"\n]")

        content  = content.replace(get_replace_install,content_replace)
        content =content+"\n".join([x for x in arg_append])+"\n"
        return content
    def getUrl(self,content):
        arg_import = self.argUrl.get("import",[])
        arg_url = self.argUrl.get("value",[])

        content ="\n".join([x for x in arg_import])+"\n"+content
        results = re.findall(r"(urlpatterns[\s\n]{0,}=[\s\n]{0,}\[\n[\n\s\'\w\.\,\(\)\/]{0,}\])",content)

        if len(results)>0:
            get_replace_install = results[0]

            content_replace  = get_replace_install.replace("\n]","\n"+",\n".join([ x for x in arg_url])+"\n]" )

            content  = content.replace(get_replace_install,content_replace)
        return content
