from plutonkit.framework.analysis.word_distance import WordDistance

VALID_MASTER_BLUEPRINT_KEY = ["name","bootscript","settings","choices", "dependencies","script","files"]
class ReviewBlueprint:
    def __init__(self, blueprint_content) -> None:
        self.blueprint_content = blueprint_content

    def verify_blueprint(self):
        validate_data = { 
            "error_message": [], 
        }
        
        self.__check_invalid_value(validate_data,True,True,self.blueprint_content,VALID_MASTER_BLUEPRINT_KEY)

        if len(validate_data["error_message"])==0:
            if "name" not in self.blueprint_content:
                validate_data["error_message"].append(
                    f"`name` is missing in architecture.yaml, please provide"
                )
            if "settings" not in self.blueprint_content:
                validate_data["error_message"].append(
                    f"`settings` is missing in architecture.yaml, please provide"
                )
            else:
                if "install_type" not in self.blueprint_content['settings']:
                    validate_data["error_message"].append(
                    f"`settings -> install_type` is missing in architecture.yaml, please provide"
                )
            if "files" not in self.blueprint_content:
                validate_data["error_message"].append(
                    f"`files` is missing in architecture.yaml, please provide"
                )
            else:
                self.__check_invalid_value(validate_data,True,True,self.blueprint_content["files"],["default", "optional"],"files -> ")
                if "optional" in self.blueprint_content["files"]:
                    for val in self.blueprint_content["files"]["optional"]:
                        self.__check_invalid_value(validate_data,True,True,val,["condition", "dependent"],"files ->optional -> ")
            if "choices" in self.blueprint_content:
                for val in self.blueprint_content["choices"]:
                    self.__check_invalid_value(validate_data,True,True,val,["name", "question", "type", "option"],"choices[] -> ") 
            if "dependencies" in self.blueprint_content:
                self.__check_invalid_value(validate_data,True,True,self.blueprint_content["dependencies"],["default", "optional"],"dependencies -> ")

                if "optional" in self.blueprint_content["dependencies"]:
                    for val in self.blueprint_content["dependencies"]["optional"]:
                        self.__check_invalid_value(validate_data,True,True,val,["condition", "dependent"],"dependencies ->optional -> ")
            if "script" in self.blueprint_content:
                for _,val in self.blueprint_content["script"].items():
                    self.__check_invalid_value(validate_data,True,True,val,["command", "description"],"script[] -> ") 
            if "bootscript" in self.blueprint_content:
                for val in self.blueprint_content["bootscript"]:
                    self.__check_invalid_value(validate_data,True,True,val,["command", "exec_position"],"bootscript[] -> ") 
                    if "exec_position" in val:
                        if val["exec_position"] != "start" and val["exec_position"] != "end":
                                validate_data["error_message"].append(
                        f"the `bootscript[] -> exec_position` is invalid, choose either start or end"
                )
        return validate_data

    def __check_invalid_value(self,validate_data,is_type_key,is_type_item,values,trained,main_key=""):
        words_distance = WordDistance(trained)
        for key, value in is_type_item and values.items() or enumerate(values):
            distances = words_distance.get_ave_distance(is_type_key and key or value)
            max_distance = max(distances)
            if max_distance != 1.0:
                validate_data["error_message"].append(
                    f"the `{main_key}{key}` is invalid,  I assume you are using this command `{main_key}{trained[distances.index(max_distance)]}`"
                )
