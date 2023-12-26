"""Module providing a function printing python version."""

from yaml import  dump

from plutonkit.framework.package.django_script import DjangoScript

from plutonkit.core.blueprint_architecture import BlueprintArchitecture
from plutonkit.helper.command import pip_install_requirement,pip_run_command
from plutonkit.config.framework import SUPPORT_LIBRARY_DJANGO,\
SUPPORT_LIBRARY_DJANGO_REST_FRAMEWORK,\
SUPPORT_LIBRARY_BOTTLE,\
SUPPORT_LIBRARY_FAST_API,\
SUPPORT_LIBRARY_FLASK,\
SUPPORT_LIBRARY_GRAPHENE,\
SUPPORT_LIBRARY_ARIADNE,\
SUPPORT_LIBRARY_TARTIFLETTE,\
SUPPORT_LIBRARY_DJANGO_GRAPHBOX,\
SUPPORT_LIBRARY_GRPC,\
SUPPORT_LIBRARY_WEB_SOCKET,\
SUPPORT_LIBRARY_WEB3,\
SUPPORT_LIBRARY_GRPC_INTERCEPTOR

class FrameworkBluePrint(BlueprintArchitecture):
    def __init__(self,path,reference_value,framework_name) -> None:
        super().__init__(reference_value)
        self.path = path
        self.parameter_constant = []
        self.parameter_execute_variable = {}
        self.framework_name=framework_name

    def __construct_yml_exeecute(self,name,value):
        if name not in self.parameter_execute_variable:
            self.parameter_execute_variable[name] = {"command":[value]}
        else:
            variable_command = self.parameter_execute_variable[name]['command']
            self.parameter_execute_variable[name]['command'] = variable_command+[value]

    def get_project_script(self):
        return  dump({
            "name":self.getProjectName(),
            "package":self.framework_name.replace("package_","")
        })

    def get_execute_script(self):
        self.parameter_execute_variable["pip_install"] = {"command":["pip install -r requirements.txt"]}

        if 'docker' in self.reference_value['command']:
                if  self.reference_value['command']['docker'] == "default_docker_yes":
                    self.parameter_execute_variable["docker_build"] = {"command":["docker build -t apps ."]}
                    self.parameter_execute_variable["docker_run"] = {"command":["docker run --name apps"]}
        return dump({
            "script":self.parameter_execute_variable
        })

    def get_env_script(self):
        return '''
DB_CONNECTION=
DB_NAME=
DB_USER=
DB_PASSWORD=

'''

    def package_django(self):
        self.generate_requirement(SUPPORT_LIBRARY_DJANGO)
        pip_install_requirement(self.reference_value)

        pip_run_command(['rm','-rf',self.getProjectName()])
        pip_run_command(['django-admin','startproject',self.getProjectName()])
        self.generate_requirement(SUPPORT_LIBRARY_DJANGO)
        self.generate_filesystem(self.getDefaultProjectName())

        django = DjangoScript(argSetting = {
            "value":[self.getProjectName(".apptest")],
            "import":[]
        },
        argUrl = {
            "value":["path('health/', health)"],
            "import":["from "+self.getProjectName(".apptest.views import health")]
        })
        self.modified_project_filesystem({
            "modified_file_content":{
                "settings":django.getSettings,
                "urls":django.getUrl
            }
        })
        self.__construct_yml_exeecute("migrate","python manage.py makemigrations")
        self.__construct_yml_exeecute("migrate","python manage.py migrate")
        self.__construct_yml_exeecute("start","python manage.py runserver")

    def package_django_rest(self):

        self.generate_requirement(SUPPORT_LIBRARY_DJANGO_REST_FRAMEWORK)
        pip_install_requirement(self.reference_value)

        pip_run_command(['rm','-rf',self.getProjectName()])
        pip_run_command(['django-admin','startproject',self.getProjectName()])
        self.generate_requirement(SUPPORT_LIBRARY_DJANGO_REST_FRAMEWORK)
        self.generate_filesystem(self.getDefaultProjectName())

        django = DjangoScript(argSetting = {
            "value":[self.getProjectName(".apptest")],
            "import":[],
            "append":[]#"REST_FRAMEWORK = []"]
        },
        argUrl = {
            "value":["path('', include('"+self.getProjectName(".apptest.url")+"'))"],
            "import":["from django.urls import include"]
        })
        self.modified_project_filesystem({
            "modified_file_content":{
                "settings":django.getSettings,
                "urls":django.getUrl
            }
        })
        self.__construct_yml_exeecute("migrate","python manage.py makemigrations")
        self.__construct_yml_exeecute("migrate","python manage.py migrate")
        self.__construct_yml_exeecute("start","python manage.py runserver")

    def package_bottle(self):
        self.generate_requirement(SUPPORT_LIBRARY_BOTTLE)
        pip_install_requirement(self.reference_value)
        self.generate_filesystem()

    def package_fastapi(self):
        self.generate_requirement(SUPPORT_LIBRARY_FAST_API)
        pip_install_requirement(self.reference_value)
        self.generate_filesystem()
        self.__construct_yml_exeecute("start","uvicorn main:app")

    def package_flask(self):

        self.generate_requirement(SUPPORT_LIBRARY_FLASK)

        pip_install_requirement(self.reference_value)
        self.generate_filesystem()
        self.__construct_yml_exeecute("start","flask --app main run")

    def package_graphene(self):
        self.generate_requirement(SUPPORT_LIBRARY_GRAPHENE)
        pip_install_requirement(self.reference_value)
        self.generate_filesystem()
        self.__construct_yml_exeecute("start","python main.py")

    def package_ariadne(self):
        self.generate_requirement(SUPPORT_LIBRARY_ARIADNE)
        pip_install_requirement(self.reference_value)
        self.generate_filesystem()
        self.__construct_yml_exeecute("start","uvicorn main:app")

    def package_tartiflette(self):
        self.generate_requirement(SUPPORT_LIBRARY_TARTIFLETTE)
        pip_install_requirement(self.reference_value)
        self.generate_filesystem()
        self.__construct_yml_exeecute("start","python main.py")

    def package_django_graphbox(self):
        self.generate_requirement(SUPPORT_LIBRARY_DJANGO_GRAPHBOX)
        pip_install_requirement(self.reference_value)

        pip_run_command(['rm','-rf',self.getProjectName()])
        pip_run_command(['django-admin','startproject',self.getProjectName()])
        self.generate_requirement(SUPPORT_LIBRARY_DJANGO_GRAPHBOX)
        self.generate_filesystem(None,{
            "modified_position":{
                "urls":f"{self.getProjectName()}/"
            }
        })
        django = DjangoScript(argSetting = {
            "value":["graphene_django","graph_schema.myapp","graph_schema.myproject"],
            "import":[]
        },
        argUrl = {
            "value":[
                "path('graphql/', csrf_exempt(FileUploadGraphQLView.as_view(graphiql=True, schema=schema)))"
            ],
            "import":[
                "from graphene_file_upload.django import FileUploadGraphQLView",
                "from django.views.decorators.csrf import csrf_exempt",
                "from graph_schema.myproject.schema import schema",
            ]
        })
        self.modified_project_filesystem({
            "modified_file_content":{
                "settings":django.getSettings,
                "urls":django.getUrl
            }
        })

        self.__construct_yml_exeecute("migrate","python manage.py makemigrations")
        self.__construct_yml_exeecute("migrate","python manage.py migrate")
        self.__construct_yml_exeecute("start","python manage.py runserver")

    def package_default_grpc(self):
        self.generate_requirement(SUPPORT_LIBRARY_GRPC)
        pip_install_requirement(self.reference_value)
        self.generate_filesystem()

        self.__construct_yml_exeecute("proto_generate","python -m grpc_tools.protoc -I./protobufs --python_out=./server/proto   --grpc_python_out=./server/proto ./protobufs/test.proto")

    def package_default_grpc_w_interceptor(self):
        self.generate_requirement(SUPPORT_LIBRARY_GRPC_INTERCEPTOR)
        pip_install_requirement(self.reference_value)
        self.generate_filesystem()

        self.__construct_yml_exeecute("proto_generate","python -m grpc_tools.protoc -I./protobufs --python_out=./server/proto   --grpc_python_out=./server/proto ./protobufs/test.proto")

    def package_default_websocket(self):
        print("This feature is in progress")
        #generate_requirement(self.reference_value,SUPPORT_LIBRARY_WEB_SOCKET)
        #pip_install_requirement(self.reference_value)
        #generate_filesystem(self.reference_value)
        #

    def package_default_web3(self):
        self.generate_requirement(SUPPORT_LIBRARY_WEB3)
        pip_install_requirement(self.reference_value)
        self.generate_filesystem()

    def package_default_packaging(self):
        self.generate_filesystem()
