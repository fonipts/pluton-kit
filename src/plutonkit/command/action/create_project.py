"""Module providing a function printing python version."""
import os
from curses import wrapper

from plutonkit.config import PROJECT_COMMAND_FILE,\
PROJECT_DETAILS_FILE,\
PROJECT_ENV_FILE,\
DOCKER_FILE,\
DOCKER_COMPOSE_FILE
from plutonkit.config.system import SERVICE_TYPE
from plutonkit.framework.blueprint import FrameworkBluePrint
from plutonkit.framework.blueprint_docker import  FrameworkBluePrintDocker
from plutonkit.helper.filesystem import generate_project_folder_cwd,generate_default_file
from plutonkit.helper.config import get_config

class CreateProject:
    def __init__(self) -> None:
        pass

    def comment(self):
        return "Start creating your project in our listed framework"
    def execute(self):
        details_command = {
            "details":{},
            "command":[]
        }
        self.callback_execute(details_command,"What is your service type?",SERVICE_TYPE)

    def callback_execute(self,reference_value,name,step):

        try:
            field_type = 'input'
            if len( reference_value["command"])>0:
                field_type = reference_value["command"][len( reference_value["command"])-1]['field_type']
            if field_type == 'multiple_choice':

                enum_action = ['[%s]  %s'%(key+1,val['option_name']) for key,val in enumerate(step)]
                print("\n%s\n%s "%(name,"\n".join(enum_action)))
                answer = input('choose only at [%s]'%(len(step) == 1 and '1' or '1-'+str(len(step)) ))

            else:
                enum_action = ['(%s) %s'%(key+1,val['option_name']) for key,val in enumerate(step)]
                print("\n%s\n%s "%(name,"\n".join(enum_action)))
                answer = input('choose only at [%s]'%(len(step) == 1 and '1' or '1-'+str(len(step)) ))

                int_answer = int(answer)
                available_step = step[int_answer-1]
                reference_value["command"].append({
                    "name":available_step['name'],
                    "type":available_step['type'],
                    'field_type':available_step['field_type']
                })

            if len(available_step['config']) >0:
                self.callback_execute(reference_value,available_step['question'],available_step['config'])
            else:
                self.project_details_execute(reference_value)
        except Exception:
            print("Invalid argument please select in the available command `%s`\n"%(answer))
            self.callback_execute(reference_value,name,step)

    def project_details_execute(self,reference_value):
        project_name = input("Name of folder project?")
        reference_value['details']['project_name'] = project_name
        author_name = input("Name of author?")
        reference_value['details']['author_name'] = author_name
        try:
            self.project_execute(reference_value)
        except Exception as e:
            print(e,"error")
            exit(0)

    def project_execute(self,reference_value):

        directory = os.getcwd()

        enum_action = [f" {val['type']}: {val['name']}" for key,val in enumerate(reference_value['command'])]
        command_value  = get_config(reference_value)
        framework_value = command_value['framework']

        folder_name = 'Project name: %s'%(reference_value['details']['project_name'])
        answer = input("%s\n%s\nDo you want to continue?(y/n) > "%("\n".join(enum_action),folder_name))
        dir_path = os.path.join(directory, reference_value['details']['project_name'])

        if answer == "y":
            if os.path.exists(dir_path):
                raise Exception("The folder name `%s` does exist" %(reference_value['details']['project_name']))

            generate_project_folder_cwd(reference_value )
            framework = FrameworkBluePrint(dir_path, reference_value,framework_value)
            getattr(framework, framework_value)()
            generate_default_file(reference_value,PROJECT_COMMAND_FILE,framework.get_execute_script())
            generate_default_file(reference_value,PROJECT_DETAILS_FILE,framework.get_project_script())
            generate_default_file(reference_value,self.__getEnvFileName(framework_value,PROJECT_ENV_FILE),framework.get_env_script())
            if 'docker' in command_value:
                if  command_value['docker'] == "default_docker_yes":
                    docker_framework = FrameworkBluePrintDocker(reference_value,framework_value)
                    generate_default_file(reference_value,self.__getEnvFileName(framework_value,DOCKER_FILE),docker_framework.getDocker())
                    generate_default_file(reference_value,self.__getEnvFileName(framework_value,DOCKER_COMPOSE_FILE),docker_framework.getDockerFile())
            exit(0)
        else:
            print("Your confirmation say `No`")
            exit(0)

    def __getEnvFileName(self,framework_value,file_name):
        if framework_value in ["package_default_grpc","package_default_grpc_w_interceptor"]:
            return "server/%s"%(file_name)
        return file_name
