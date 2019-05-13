# -*- coding: utf-8 -*- 
from enum import Enum
import sys
import math
import emotionEnum
import time
from neopixel import *
class Changer:
    # LED strip configuration:
    LED_COUNT      = 11      # Number of LED pixels.
    LED_PIN        = 18      # GPIO pin connected to the pixels (18 uses PWM!).
    LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
    LED_DMA        = 10      # DMA channel to use for generating signal (try 10)
    LED_BRIGHTNESS = 255     # Set to 0 for darkest and 255 for brightest
    LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
    LED_CHANNEL    = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53
    strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
    strip.begin()
    feeling=0
    color=[255, 255, 255]
    #['Anger','Expectation','Pleasure','Respect','Fear','Surprised','Sadness','Aversion']
    def __init__(self):
        pass

    def setWhite(self):
        self.sigmoidChangerClean(255, 255, 255)

    def setEmotion(self, emotion):#emotion = (maximum, index)
        emo = emotionEnum.emotionEnum
        if emotion == 0:
            self.feeling = emo.Anger
        elif emotion == 1:
            self.feeling = emo.Expectation
        elif emotion == 2:
            self.feeling = emo.Pleasure
        elif emotion == 3:
            self.feeling = emo.Respect
        elif emotion == 4:
            self.feeling = emo.Fear
        elif emotion == 5:
            self.feeling = emo.Surprised
        elif emotion == 6:
            self.feeling = emo.Sadness
        elif emotion == 7:
            self.feeling = emo.Aversion

        print(self.feeling)
        self.emotionToColor()#according to the mind color wheel
        self.sigmoidChanger()#change the color

    def pastLed(self, past):
        for i in past:
            self.setEmotion(int(i[0]))
            time.sleep(3)
        self.rainbow()
        
    def sigmoidChanger(self):
        nowColor = self.strip.getPixelColor(1)
        binState=bin(nowColor)
        if not nowColor == 0:
            lenth=nowColor.bit_length()
            binState=str(binState[2:])
            diffLen = 24-lenth
            rotate=0
            while rotate < diffLen:
                binState = '0' + binState
                rotate += 1
            aR = int(str(binState[0:8]), 2)
            aG = int(str(binState[8:16]), 2)
            aB = int(str(binState[16:24]), 2)
        else:
            aR = 0
            aG = 0
            aB = 0
        
        bR = self.color[0]
        bG = self.color[1]
        bB = self.color[2]
        print('원래: {} {} {}'.format(aR, aG, aB))
        print('변경: {} {} {}'.format(bR, bG, bB))
        diffR = bR - aR
        diffG = bG - aG
        diffB = bB - aB
        for i in range(-100, 100):
            R = int(aR + self.sig(i * 0.05) * diffR)
            G = int(aG + self.sig(i * 0.05) * diffG)
            B = int(aB + self.sig(i * 0.05) * diffB)
            for j in range(0, 11):
                self.strip.setPixelColorRGB(j, R, G, B)
                self.strip.show()
            time.sleep(0.0025)

    def sig(self, r):
        return 1 / (1 + math.exp((-1)*r))

    def emotionToColor(self):
        emo=emotionEnum.emotionEnum
        if self.feeling == emo.Anger:
            self.color = [255, 0, 0]#Red
        elif self.feeling == emo.Expectation:
            self.color = [255, 127, 0]#Orange
        elif self.feeling == emo.Pleasure:
            self.color = [255, 255, 0]#Yellow
        elif self.feeling == emo.Respect:
            self.color = [127, 255, 0]#MellowGreen
        elif self.feeling == emo.Fear:
            self.color = [0, 255, 0]#Green
        elif self.feeling == emo.Surprised:
            self.color = [0, 127, 255]#MellowBlue
        elif self.feeling == emo.Sadness:
            self.color = [0, 0, 255]#Blue
        elif self.feeling == emo.Aversion:
            self.color = [255, 0, 255]#Violet
    
    def emotionToColorClean(self, mode):
        if mode == 1:
            return [255, 0, 0]#Red
        if mode == 2:
            return [255, 127, 0]#Orange
        if mode == 3:
            return [255, 255, 0]#Yellow
        if mode == 4:
            return [127, 255, 0]#MellowGreen
        if mode == 5:
            return [0, 255, 0]#Green
        if mode == 6:
            return [0, 127, 255]#MellowBlue
        if mode == 7:
            return [0, 0, 255]#Blue
        if mode == 8:
            return [255, 0, 255]#Violet

    def sigmoidChangerClean(self, red, green, blue):
        nowColor = self.strip.getPixelColor(1)
        binState=bin(nowColor)
        if not nowColor == 0:
            lenth=nowColor.bit_length()
            binState=str(binState[2:])
            diffLen = 24-lenth
            rotate=0
            while rotate < diffLen:
                binState = '0' + binState
                rotate += 1
            aR = int(str(binState[0:8]), 2)
            aG = int(str(binState[8:16]), 2)
            aB = int(str(binState[16:24]), 2)
        else:
            aR = 0
            aG = 0
            aB = 0
        
        bR = red
        bG = green
        bB = blue
        print('원래: {} {} {}'.format(aR, aG, aB))
        print('변경: {} {} {}'.format(bR, bG, bB))
        diffR = bR - aR
        diffG = bG - aG
        diffB = bB - aB
        for i in range(-100, 100):
            R = int(aR + self.sig(i * 0.05) * diffR)
            G = int(aG + self.sig(i * 0.05) * diffG)
            B = int(aB + self.sig(i * 0.05) * diffB)
            for j in range(0, 11):
                self.strip.setPixelColorRGB(j, R, G, B)
                self.strip.show()
            time.sleep(0.0025)

    def clear(self):
        self.sigmoidChangerClean(0,0,0)

    def glow(self, mode):
        color = self.emotionToColorClean(mode + 1)
        self.sigmoidChangerClean(0, 0, 0)
        self.sigmoidChangerClean(color[0], color[1], color[2])


    def Color(self, red, green, blue, white = 0):
          return (white << 24) | (red << 16) | (green << 8) | blue

    def wheel(self, pos):
        if pos < 85:
            return self.Color(pos * 3, 255 - pos * 3, 0)
        elif pos < 170:
            pos -= 85
            return self.Color(255 - pos * 3, 0, pos * 3)
        else:
            pos -= 170
            return self.Color(0, pos * 3, 255 - pos * 3)

    def rainbow(self, wait_ms=20, iterations=1):
        bgr=0
        for j in range(256*iterations):
            for i in range(self.strip.numPixels()):
                self.strip.setPixelColor(i, self.wheel((i+j) & 255))
                if(bgr<255):
                    self.strip.setBrightness(bgr)
                    bgr += 1
            self.strip.show()
            time.sleep(wait_ms/1000.0)

    def finalRainbow(self):
        for i in range(0, 256):
            self.strip.setBrightness(255-i)
            self.strip.show()
            time.sleep(0.003)
        self.rainbow(iterations=2)

    def wrong(self, mode):
        color = self.emotionToColorClean(mode)
        for i in range(0, 11):
            self.strip.setPixelColorRGB(i, 0, 0, 0)
            self.strip.show()
        time.sleep(0.2)
        for i in range(0, 11):
            self.strip.setPixelColorRGB(i, color[0], color[1], color[2])
            self.strip.show()
        time.sleep(0.2)
        for i in range(0, 11):
            self.strip.setPixelColorRGB(i, 0, 0, 0)
            self.strip.show()
        time.sleep(0.2)
        for i in range(0, 11):
            self.strip.setPixelColorRGB(i, color[0], color[1], color[2])
            self.strip.show()
        

    def changeMode(self, mode):
        color = self.emotionToColorClean(mode)
        self.sigmoidChangerClean(color[0], color[1], color[2])#모드 변경시 색 변경