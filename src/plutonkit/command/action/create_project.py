from plutonkit.config.system import SERVICE_TYPE
import sys
import os
from plutonkit.helper.filesystem import generate_project_folder_cwd
from plutonkit.framework.blueprint import FrameworkBluePrint

class CreateProject:
    def __init__(self) -> None:
        pass

    def comment(self):
        return "Start creating your project in our listed framework"
    def execute(self):
        DETAILS_COMMAND = {
            "details":{},
            "command":[]
        }
        self.callback_execute(DETAILS_COMMAND,"What is your service type?",SERVICE_TYPE)



    def callback_execute(self,reference_value,name,step):

        enum_action = ['(%s) %s'%(key+1,val['option_name']) for key,val in enumerate(step)]
        print("\n%s\n%s "%(name,"\n".join(enum_action)))
        answer = input('choose only at [%s]'%(len(step) == 1 and '1' or '1-'+str(len(step)) ))

        try:
            int_answer = int(answer)
            available_step = step[int_answer-1]

            reference_value["command"].append({
            "name":available_step['name'],
            "type":available_step['type'],
            })
            if len(available_step['config']) >0:
                self.callback_execute(reference_value,available_step['question'],available_step['config'])
            else:
                self.project_details_execute(reference_value)
        except Exception as e:
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
            print(e)

    def project_execute(self,reference_value):
        DIRECTORY = os.getcwd()

        enum_action = [' %s: %s'%(val['type'],val['name']) for key,val in enumerate(reference_value['command'])]
        framework_value = [val['name'] for key,val in enumerate(reference_value['command']) if val['type'] =='framework' ][0]

        folder_name = 'Project name: %s'%(reference_value['details']['project_name'])
        answer = input("%s\n%s\nDo you want to continue?(y/n) > "%("\n".join(enum_action),folder_name))
        DIR_PATH = os.path.join(DIRECTORY, reference_value['details']['project_name'])
        if answer == "y":
            if os.path.exists(DIR_PATH):
                raise Exception("The folder name `%s` does exist" %(reference_value['details']['project_name']))
            generate_project_folder_cwd(reference_value )
            framework = FrameworkBluePrint(DIR_PATH, reference_value)
            getattr(framework, framework_value)()
        else:
            print("Your confirmation say `No`")
            