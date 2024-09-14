import os
import subprocess
from http.client import responses

import requests

from plutonkit.config import ARCHITECTURE_DETAILS_FILE
from plutonkit.config.message import ARCHITECTURE_REQUEST_ERROR_MESSAGE

from .ValidateSource import ValidateSource


class ArchitectureRequest:
    def __init__(self, path, dirs) -> None:
        self.path = path
        self.dirs = dirs
        self.validate = ValidateSource(path)
        self.isValidReq = False
        self.getValidReq = None
        self.errorMessage = ARCHITECTURE_REQUEST_ERROR_MESSAGE
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

            except subprocess.CalledProcessError as clone_error:
                output = clone_error.output.decode("utf-8")
                self.errorMessage = output

        if self.validate.arch_type == "local":

            arch_file = self._read_file(ARCHITECTURE_DETAILS_FILE)
            self.isValidReq = arch_file["is_valid"]
            self.errorMessage = arch_file["content"]

        if self.isValidReq is False and self.errorMessage != ARCHITECTURE_REQUEST_ERROR_MESSAGE:
            self.errorMessage = f"No `{ARCHITECTURE_DETAILS_FILE}` was found in local directory"


    def getFiles(self, file):
        if self.validate.arch_type == "request":
            data = self._curl(f"{self.path}/{file}")
            return {
                "is_valid": data.status_code == 200,
                "content": str(data.text)
            }
        if self.validate.arch_type == "git":
            return self._read_file(file)
        if self.validate.arch_type == "local":
            return self._read_file(file)
        return {"is_valid": False}

    def _curl(self, path):
        data = requests.get(path, timeout=25)
        return data

    def _read_file(self, file):
        if self.validate.arch_type == "local":
            path = os.path.join(self.dirs, self.path, file)
        else:
            path = os.path.join(self.dirs, self.validate.repo_name, self.validate.repo_path_dir, file)

        try:
            f_read = open(path, "r", encoding="utf-8")

            data =  {
                "is_valid": True,
                "content": str(f_read.read())
            }
            f_read.close()
            return data
        except Exception as e:
            return {
                "is_valid": False,
                "content": str(e)
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
