from plutonkit.helper.filesystem import generate_requirement,generate_filesystem
from plutonkit.helper.command import pip_install_requirement,pip_run_command,change_dir_command

from plutonkit.config.framework import SUPPORT_LIBRARY_DJANGO,\
SUPPORT_LIBRARY_DJANGO_REST_FRAMEWORK,\
SUPPORT_LIBRARY_BOTTLE,\
SUPPORT_LIBRARY_FAST_API,\
SUPPORT_LIBRARY_FLASK,\
SUPPORT_LIBRARY_GRAPHENE,\
SUPPORT_LIBRARY_STRAWBERRY,\
SUPPORT_LIBRARY_ARIADNE,\
SUPPORT_LIBRARY_TARTIFLETTE,\
SUPPORT_LIBRARY_DJANGO_GRAPHBOX,\
SUPPORT_LIBRARY_GRPC,\
SUPPORT_LIBRARY_WEB_SOCKET

import os

class FrameworkBluePrint:
    def __init__(self,path,reference_value) -> None:
        self.path = path
        self.reference_value = reference_value

    def package_django(self):
        generate_requirement(self.reference_value,SUPPORT_LIBRARY_DJANGO)
        pip_install_requirement(self.reference_value)
        #change_dir_command(self.reference_value)
        pip_run_command(['rm','-rf',self.reference_value['details']['project_name']])
        pip_run_command(['django-admin','startproject',self.reference_value['details']['project_name']])
        generate_requirement(self.reference_value,SUPPORT_LIBRARY_DJANGO)
        generate_filesystem(self.reference_value,self.reference_value['details']['project_name'])
        #change_dir_command(self.reference_value)
        #pip_run_command(['django-admin','startapp','testapp'])

    def package_django_rest(self):
        generate_requirement(self.reference_value,SUPPORT_LIBRARY_DJANGO_REST_FRAMEWORK)
        pip_install_requirement(self.reference_value)

        pip_run_command(['django-admin','startproject',self.reference_value['details']['project_name']])
        generate_requirement(self.reference_value,SUPPORT_LIBRARY_DJANGO_REST_FRAMEWORK)
        generate_filesystem(self.reference_value)

    def package_bottle(self):
        generate_requirement(self.reference_value,SUPPORT_LIBRARY_BOTTLE)
        pip_install_requirement(self.reference_value)
    def package_fastapi(self):
        generate_requirement(self.reference_value,SUPPORT_LIBRARY_FAST_API)
        pip_install_requirement(self.reference_value)
        generate_filesystem(self.reference_value)
    def package_flask(self):
        generate_requirement(self.reference_value,SUPPORT_LIBRARY_FLASK)
        pip_install_requirement(self.reference_value)
        generate_filesystem(self.reference_value)
    def package_graphene(self):
        generate_requirement(self.reference_value,SUPPORT_LIBRARY_GRAPHENE)
        pip_install_requirement(self.reference_value)
        generate_filesystem(self.reference_value)
    def package_strawberry(self):
        generate_requirement(self.reference_value,SUPPORT_LIBRARY_STRAWBERRY)
        pip_install_requirement(self.reference_value)
        generate_filesystem(self.reference_value)
    def package_ariadne(self):
        generate_requirement(self.reference_value,SUPPORT_LIBRARY_ARIADNE)
        pip_install_requirement(self.reference_value)
        generate_filesystem(self.reference_value)
    def package_tartiflette(self):
        generate_requirement(self.reference_value,SUPPORT_LIBRARY_TARTIFLETTE)
        pip_install_requirement(self.reference_value)
        generate_filesystem(self.reference_value)
    def package_django_graphbox(self):
        generate_requirement(self.reference_value,SUPPORT_LIBRARY_DJANGO_GRAPHBOX)
        pip_install_requirement(self.reference_value)
        generate_filesystem(self.reference_value)
    def package_default_grpc(self):
        generate_requirement(self.reference_value,SUPPORT_LIBRARY_GRPC)
        pip_install_requirement(self.reference_value)
        generate_filesystem(self.reference_value)
    def package_default_websocket(self):
        generate_requirement(self.reference_value,SUPPORT_LIBRARY_WEB_SOCKET)
        pip_install_requirement(self.reference_value)
        generate_filesystem(self.reference_value)
