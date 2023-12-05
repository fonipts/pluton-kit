from plutonkit.helper.filesystem import default_project_name,generate_requirement,generate_filesystem,modified_project_filesystem
from plutonkit.helper.config import get_config
from plutonkit.framework.package.database_script import DatabaseScript

class BlueprintArchitecture:
    def __init__(self,reference_value) -> None:
        self.reference_value = reference_value
        self.config= get_config(self.reference_value)
        self.database_script = DatabaseScript( self.config['framework'], self.config['db_package'] , self.config['db_type'] )

    def getProjectName(self,suffix = "") -> str:

        return default_project_name(self.reference_value['details']['project_name'])+suffix
    def getDefaultProjectName(self,suffix = "") -> str:
        return self.reference_value['details']['project_name']+suffix
    def generate_filesystem(self,sub_folder=None,action_file={},variable={}):
        self.__sql_db(variable)
        generate_filesystem(self.reference_value,sub_folder,action_file,variable)
    def modified_project_filesystem(self,action_file={}):

        return modified_project_filesystem(self.reference_value,action_file)
    def generate_requirement(self,library=[]):

        library += self.database_script.getRequirement()
        return generate_requirement(self.reference_value,library)

    def __sql_db(self,variable):
        variable['SQL_ALCH_DB_CONTENT'] =self.database_script.getContent()
        variable['SQL_ALCH_IMPORT'] = self.database_script.getImport()
        variable['DJANGO_TEST_NAME'] =self.getProjectName()
