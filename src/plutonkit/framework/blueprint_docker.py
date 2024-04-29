from plutonkit.config.package import (DOCKER_IMAGE_PYTHON,
DOCKER_IMAGE_NGINX ,
DOCKER_IMAGE_APACHE ,
DOCKER_IMAGE_APACHE2)
from plutonkit.helper.config import get_config

class FrameworkBluePrintDocker:
    def __init__(self,reference_value,framework_name) -> None:
        self.command_value  = get_config(reference_value)
        self.framework_name = framework_name
        self.list_image = {
            "docker_image_python":DOCKER_IMAGE_PYTHON,
            "docker_image_nginx":DOCKER_IMAGE_NGINX,
            "docker_image_apache":DOCKER_IMAGE_APACHE,
            "docker_image_apache":DOCKER_IMAGE_APACHE2
        }
        self.var_expose_port = ""
        self.var_run = ""
    def getDocker(self):
        self.__packageList()
        str_img = "FROM %s\n"%(self.list_image[self.command_value["docker_image_type"]])
        str_img += "WORKDIR /usr\n"
        str_img += "EXPOSE %s\n"%(self.var_expose_port)
        str_img += "RUN %s\n"%(self.var_run)
        return str_img
    def getDockerFile(self):
        return ""

    def __packageList(self):
        if self.framework_name in ["package_django","package_django_rest","package_django_graphbox"] :
            self.var_expose_port = "8080"
            self.var_run = "python manage.py runserver"
        if self.framework_name in ["package_flask"] :
            self.var_expose_port = "5000"
            self.var_run = "python main.py"
        if self.framework_name in ["package_fastapi"] :
            self.var_expose_port = "8000"
            self.var_run = "python main.py"
        if self.framework_name in ["package_bottle"]:
            self.var_expose_port = "8080"
            self.var_run = "python main.py"
