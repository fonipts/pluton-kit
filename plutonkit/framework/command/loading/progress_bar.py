import sys
#import time
from math import ceil


class ProgressBar:
    def __init__(self,width=50,fill=".",empty=" ",limit_percentage=100,load_message = "Progress"):
        self.width=width
        self.fill=fill
        self.load_message=load_message
        self.empty=empty
        self.limit_percentage=limit_percentage

    def update(self,i:int):
        if i ==0:
            percent = 0
        else:
            percent = i/self.limit_percentage
        filled_length = ceil(self.width * percent)
        bar_print = (self.fill * filled_length) + self.empty * (self.width - filled_length)
        percentage = f"{percent:.1%}"
        sys.stdout.write(f"\r{self.load_message}[{bar_print}]{percentage}")
        sys.stdout.flush()
        if i > self.limit_percentage:
            print()
    def completed(self):
        print()
