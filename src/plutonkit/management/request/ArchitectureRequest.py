import os
import subprocess
from http.client import responses

import requests

from plutonkit.config import ARCHITECTURE_DETAILS_FILE

from .ValidateSource import ValidateSource


class ArchitectureRequest:
    def __init__(self,path, dirs) -> None:
        self.path = path
        self.dirs = dirs
        self.validate = ValidateSource(path)
        self.isValidReq = False
        self.getValidReq = None
        self.errorMessage = None
        self.__init_architecture()

    def __init_architecture(self):
        if self.validate.arch_type == "request":
            data = self._curl(f"{self.path}/{ARCHITECTURE_DETAILS_FILE}")
            if data.status_code == 200:
                self.isValidReq = True
                self.getValidReq = str(data.text)
            else:
                self.errorMessage = responses[data.status_code]
        if self.validate.arch_type == "git":

            try:
                subprocess.check_output(
                    ["git", "clone", self.validate.path],
                    cwd=self.dirs,
                    stderr=subprocess.STDOUT,
                )
                arch_file = self._read_file(ARCHITECTURE_DETAILS_FILE)
                if arch_file["is_valid"]:
                    self.isValidReq = True
                    self.getValidReq = arch_file["content"]
                else:
                    self.errorMessage = "No `"+ARCHITECTURE_DETAILS_FILE+"` was found in repository"
            except subprocess.CalledProcessError as clone_error:
                output = clone_error.output.decode("utf-8")
                self.errorMessage = output

    def getFiles(self,file):
        if self.validate.arch_type == "request":
            data = self._curl(f"{self.path}/{file}")
            return {
                "is_valid": data.status_code == 200,
                "content": str(data.text)
            }
        if self.validate.arch_type == "git":
            return self._read_file(file)
        return {"is_valid": False}

    def _curl(self, path):
        data = requests.get(path, timeout=25)
        return data
    def _read_file(self, file):
        path = os.path.join(self.dirs, self.validate.repo_name,self.validate.repo_path_dir,file)

        try:
            f_read = open(path, "r", encoding="utf-8")
            return {
                "is_valid": True,
                "content": str(f_read.read())
            }
        except:
            return {
                "is_valid": False,
                "content": ""
            }

    def clearRepoFolder(self):
        if self.validate.arch_type == "git":
            self.isValidReq = True
            try:
                subprocess.check_output(
                    ["rm", "-rf", self.validate.repo_name],
                    cwd=self.dirs,
                    stderr=subprocess.STDOUT,
                )
            except subprocess.CalledProcessError as clone_error:
                output = clone_error.output.decode("utf-8")
                print(output)
