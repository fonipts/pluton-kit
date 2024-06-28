
class InquiryTerminal:
    def __init__(self, choices=[]) -> None:
        self.ref_answer = {}
        self.choices = choices
        self.is_continue = True
        self.is_terminate = False

    def execute(self):
        if len(self.choices)>0:
            self._selection(self.choices)
        else:
            self.is_terminate = True

    def getAnswer(self):
        return self.ref_answer

    def isContinue(self):
        return self.is_continue

    def isTerminate(self):
        return self.is_terminate

    def _selection(self,choices):
        choice = choices[0]

        name = choice.get("name","")
        question = choice.get("question","")
        type = choice.get("type","")
        default = choice.get("default","")

        if type == "input":
            question = input(f"{question}?:")
            if question =="":
                question = default
            self.ref_answer[name] = question
            choices.pop(0)
        if type == "single_choice":
            option = choice.get("option",[])

            enum_action = [ f"[{key+1}] {val}" for key,val in enumerate(option)]
            print("\n%s\n%s "%(question,"\n".join(enum_action)))
            try:
                answer = input("choose only at [%s]"%(len(option) == 1 and "1" or "1-"+str(len(option)) ))

                available_step = option[int(answer)-1]
                self.ref_answer[name] = available_step
                choices.pop(0)
            except:
                print("Invalid option, try again")
                self._selection(choices)

        if type == "multiple_choice":
            option = choice.get("option",[])

            enum_action = [ f"[{key+1}] {val}" for key,val in enumerate(option)]
            print("\n%s\n%s (use comma `,` for multiple selection)"%(question,"\n".join(enum_action)))
            try:
                answer = input("choose only at [%s]"%(len(option) == 1 and "1" or "1-"+str(len(option)) ))

                self.ref_answer[name] = ""
                answer_split = answer.split(",")
                for kk in answer_split:
                    available_step = option[int(kk)-1]

                self.ref_answer[name] = answer
                choices.pop(0)
            except:
                print("Invalid option, try again")
                self._selection(choices)


        if len(choices)>0:
            self._selection(choices)
        else:
            self.is_terminate = True
