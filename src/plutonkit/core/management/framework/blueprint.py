from plutonkit.core.management.filesystem import generate_requirement
from plutonkit.core.management.command import pip_install_requirement,pip_run_command


from plutonkit.config.framework import SUPPORT_LIBRARY_DJANGO,\
SUPPORT_LIBRARY_DJANGO_REST_FRAMEWORK

import os

class FrameworkBluePrint:
    def __init__(self,path,reference_value) -> None:
        self.path = path
        self.reference_value = reference_value

    def package_django(self):
        generate_requirement(self.reference_value,SUPPORT_LIBRARY_DJANGO)
        pip_install_requirement(self.reference_value)

        pip_run_command(self.reference_value,['rm','-rf',self.reference_value['details']['project_name']])
        pip_run_command(self.reference_value,['django-admin','startproject',self.reference_value['details']['project_name']])#
        generate_requirement(self.reference_value,SUPPORT_LIBRARY_DJANGO) 

    def package_django_rest(self):
        generate_requirement(self.reference_value,SUPPORT_LIBRARY_DJANGO_REST_FRAMEWORK)
        pip_install_requirement(self.reference_value)

        pip_run_command(self.reference_value,['rm','-rf',self.reference_value['details']['project_name']])
        pip_run_command(self.reference_value,['django-admin','startproject',self.reference_value['details']['project_name']])#
        generate_requirement(self.reference_value,SUPPORT_LIBRARY_DJANGO_REST_FRAMEWORK)
     
    def package_bottle(self):
        print("package_bottle")
    def package_fastapi(self):
        print("package_fastapi")
    def package_flask(self):
        print("package_flask")
    def package_graphene(self):
        print("package_graphene")
    def package_strawberry(self):
        print("package_strawberry")
    def package_ariadne(self):
        print("package_ariadne")
    def package_tartiflette(self):
        print("package_tartiflette")
    def package_django_graphbox(self):
        print("package_django_graphbox")
    def default_grpc(self):
        print("default_grpc")   
    def default_websocket(self):
        print("default_websocket")                                                                                          