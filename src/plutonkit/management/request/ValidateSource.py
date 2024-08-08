import re


class ValidateSource:
    def __init__(self,path) -> None:
        self.path = path

        self.arch_type = None
        self.repo_name = None
        self.repo_path_dir = ""
        self.__validate_for_request()
        self.__validate_for_git()

    def __validate_for_request(self):
        # noqa: raw file github
        match1 = re.search(r"^(http[s]{0,1})\://(raw.githubusercontent.com)", self.path)
        # noqa: raw file gitlab
        match2 = re.search(r"^(http[s]{0,1})\://(gitlab.com).*?(\/\-\/raw\/)", self.path)
        if match1 or match2:
            self.arch_type = "request"
    def __validate_for_git(self):
        match1 = re.search(r"(\/[a-zA-Z0-9\_\-]{2,}\.git[\/]{0,}\b)", self.path)
        if match1:
            self.arch_type = "git"
            self.repo_name = match1[0].replace("/","").split(".")[0]
            split_path = self.path.split(r".git")
            if len(split_path)>1:
                self.path = split_path[0]+".git"
                self.repo_path_dir = "/".join(split_path[1::])
