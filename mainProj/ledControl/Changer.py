from enum import Enum
import sys
sys.path.insert(0, './../')
import emotionEnum

emotions=emotionEnum.emotionEnum.emotions
class Changer:
    def __init__(self, emotion):
        self.feeling=emotion[0]
        self.maxValue=emotion[1]

    def change(self):
        b=1

    def sigmoidChanger(self):
        a=1

    