from plutonkit.helper.filesystem import default_project_name
from plutonkit.helper.filesystem import generate_filesystem,modified_project_filesystem

class BlueprintArchitecture:
    def __init__(self,reference_value) -> None:
        self.reference_value = reference_value
    def getProjectName(self,suffix = "") -> str:

        return default_project_name(self.reference_value['details']['project_name'])+suffix
    def getDefaultProjectName(self,suffix = "") -> str:
        return self.reference_value['details']['project_name']+suffix
    def generate_filesystem(self,sub_folder=None,action_file={},variable={}):
        self.__sql_db(variable)
        generate_filesystem(self.reference_value,sub_folder,action_file,variable)
    def modified_project_filesystem(self,action_file={}):

        return modified_project_filesystem(self.reference_value,action_file)

    def __sql_db(self,variable):
        variable['SQL_ALCH_DB'] ='DB=""'
        variable['DJANGO_TEST_NAME'] =self.getProjectName()

        pass
