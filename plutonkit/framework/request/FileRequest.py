import os
from http.client import responses
from typing import Optional

import requests

from plutonkit.config import (
    ARCHITECTURE_REQUEST_ERROR_MESSAGE,
)
from plutonkit.helper.filesystem import create_temp_file

from .ValidateSource import ValidateSource


class FileRequest:
    def __init__(self, path, dirs,filename):
        self.path = path
        self.dirs = dirs
        self.validate = ValidateSource(path)
        self.isValidReq = False
        self.get_dir:Optional[str] = None
        self.errorMessage:str = ARCHITECTURE_REQUEST_ERROR_MESSAGE
        self.filename = filename
        self.ref_local_dest_filename:Optional[str] = None
        self.__init_request()

    def __init_request(self):
        if self.validate.arch_type == "request":
            data = self._curl(f"{self.path}/{self.filename}")

            if data.status_code == 200:
                self.isValidReq = True
                self.ref_local_dest_filename = os.path.join(self.dirs, self.filename)
                self.get_dir = self.dirs
                create_temp_file(self.ref_local_dest_filename, data.text+"\n")
            else:
                self.errorMessage = responses[data.status_code]
        if self.validate.arch_type == "git":

            self.isValidReq = True
            self.get_dir = self.dirs
            self.ref_local_dest_filename = os.path.join(self.dirs, str(self.validate.repo_name), self.filename)

        if self.validate.arch_type == "local":
            self.isValidReq = True
            self.ref_local_dest_filename = os.path.join(self.path, self.filename)
            self.get_dir = self.path

        if self.isValidReq is False and self.errorMessage != ARCHITECTURE_REQUEST_ERROR_MESSAGE:
            self.errorMessage = f"No `{self.filename}` was found in local directory"

    def _curl(self, path):
        data = requests.get(path, timeout=25)
        return data

    def IsValidReq(self):
        return self.isValidReq

    def getFilename(self):
        return self.ref_local_dest_filename

    def getDir(self):
        return self.get_dir

    def deleteFile(self):
        if self.ref_local_dest_filename is not None:
            os.remove(self.ref_local_dest_filename)
