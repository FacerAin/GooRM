# -*- coding: utf-8 -*- 
import enum
import os
import pickle
import socket
import threading
import time
import wave
import csv

from google.cloud import speech
from google.cloud.speech import enums, types

import control
import pyaudio
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="/home/pi/goorm/mainProj/GooRM-986a31f2c980.json"
ledChanger = control.Changer()
weight=[0, 0, 0, 0, 0, 0, 0, 0]
callTime=0
GPIO.setup(12, GPIO.OUT)#LED
def weightAdder(weightList):
    j=0
    global callTime
    for i in weightList:
        weight[j] += i
        j += 1
    callTime += 1

def weightAvg():
    for i in weight:
        weight[weight.index(i)] /= callTime

def threadFlow(lenth, isFinal):
    GPIO.output(12, True)
    text=googleSpeechAPI(record(lenth))
    GPIO.output(12, False)
    print('recognizedText:{}'.format(text))
    emotionWeight=list(socketConnect(str(text)))#get Weights of emotion
    maxValue = max(emotionWeight)
    index = emotionWeight.index(maxValue)
    weightAdder(emotionWeight)
    if isFinal == 0:
        ledChanger.setEmotion(index)
    elif isFinal == 1:
        weightAvg()
        print(weight)
        maxValue = max(weight)
        index = weight.index(maxValue)
        csvSaver(index)#save today's emotion
        ledChanger.setEmotion(index)#if isFinal=1, input the data which is averaged
        finalQuiz(index)#Quiz starting
    
def finalQuiz(maxIndex):
    time.sleep(3)
    maxIndex += 1
    ledChanger.finalRainbow()
    GPIO.setup(16, GPIO.IN, pull_up_down = GPIO.PUD_UP)
    ledChanger.changeMode(1)
    mode=1
    while True:
        if(GPIO.input(16) == False):
            if(mode > 7):
                mode = 1
            else:
                mode += 1
            ledChanger.changeMode(mode)
            time.sleep(0.05)

        if(GPIO.input(23) == False):
            #선택
            if(mode == maxIndex):
                #합격!
                break
            else:
                ledChanger.wrong()
                time.sleep(0.05)
                continue

def csvSaver(index):
    data = []
    with open('./data.csv', 'r', encoding='utf-8') as f:
        rd = csv.reader(f)
        for line in rd:
            data.append(line)
    with open('./data.csv', 'w', encoding='utf-8', newline='') as f:
        wr = csv.writer(f)
        for line in data:
            wr.writerow(line)
        wr.writerow([index])
        f.close()

def retrospection():
    dataset=[]
    lenth=0
    with open('./data.csv', 'r', encoding='utf-8') as f:
        rd = csv.reader(f)
        for line in rd:
            dataset.append((rd.line_num, line))
        lenth=len(dataset)
        f.close()
    sourceData=[]#데이터 10개로 간추리기
    j = lenth-10
    while j < lenth:
        sourceData.append(dataset[j])
        j += 1
    return sourceData


def record(lenth):
    CHUNK = 512
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 16000
    audio = pyaudio.PyAudio()
    stream = audio.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)
    frames = []
    print('###RECORDING###')
    #recordStart
    for i in range(0, int(RATE / CHUNK * lenth)):
        data = stream.read(CHUNK, exception_on_overflow=False)
        frames.append(data)
    #recordFinishing
    print('###RECOREDE###')
    stream.stop_stream()
    stream.close()
    audio.terminate()
    return frames#sound data return

def googleSpeechAPI(content):
    client = speech.SpeechClient()
    audio = types.RecognitionAudio(content=b''.join(content))
    config = types.RecognitionConfig(
        encoding=enums.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=16000,
        language_code='ko-KR')
    response = client.recognize(config, audio)
    for result in response.results:
        return result.alternatives[0].transcript #return transcript

def socketConnect(text):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect(('localhost', 25437))
        s.sendall(text.encode())
        resp = s.recv(16000)
        receivedData=pickle.loads(resp)
        print(receivedData)
        return receivedData

def btnRecog():
    GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_UP)#button
    GPIO.setup(24, GPIO.IN, pull_up_down=GPIO.PUD_UP)#toggle
    try:
        while True:
            if GPIO.input(23) == False and GPIO.input(24) == False:
                threadsStartup()
                print('mic')
                time.sleep(2400)#4' 0"
            elif GPIO.input(23) == True and GPIO.input(24) == False:
                print('past')
                past = retrospection()
                ledChanger.pastLed(past)
                
    except:
        GPIO.cleanup()

def threadsStartup():
    lenth=15#recording lenth
    iterate=int(180/lenth)
    for i in range(1, iterate):
        if not i == iterate:
            thf=threading.Thread(target=threadFlow, args=(lenth, 0))#Thread set
        else:
            thf = threading.Thread(target=threadFlow, args=(lenth, 1))
        print('start')
        thf.start()#Thread Starting
        time.sleep(lenth+1)
        print('sleepOver')
    print('ProgramFinished')

def main():
    btnRecog()

if __name__ == '__main__':
    main()
