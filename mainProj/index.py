# -*- coding: utf-8 -*- 
import enum
import os
import pickle
import socket
import threading
import time
import wave
import csv
import control
import pyaudio
import RPi.GPIO as GPIO

from google.cloud import speech
from google.cloud.speech import enums, types
abcdefg = pyaudio.PyAudio()#Warning Message Avoding
GPIO.setmode(GPIO.BCM)
os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="/home/pi/goorm/mainProj/GooRM-986a31f2c980.json"
ledChanger = control.Changer()
weight=[0, 0, 0, 0, 0, 0, 0, 0]
callTime = 0
index = 0
isFirst= 0 
GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_UP)#toggle
GPIO.setup(24, GPIO.IN, pull_up_down=GPIO.PUD_UP)#button
GPIO.setup(16, GPIO.IN, pull_up_down = GPIO.PUD_UP)#select
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
        try:
            weight[weight.index(i)] /= callTime
        except ZeroDivisionError:
            weight[weight.index(i)] = 0

def threadFlow(lenth, isFinal):
    text=googleSpeechAPI(record(lenth))
    global index
    global isFirst
    error = False
    try:
        print('recognizedText:' + text)
        emotionWeight = list(socketConnect(str(text)))#get Weights of emotion
        emotionWeight
        maxValue = max(emotionWeight)
        index = emotionWeight.index(maxValue)
        weightAdder(emotionWeight)
    except Exception as e:
        print(e)
        error = True

    if isFinal == 0:
        if not error:
            ledChanger.setEmotion(index)
        elif isFirst == 0:
            ledChanger.setWhite()
            isFirst += 1
        else:
            ledChanger.setEmotion(index)
    elif isFinal == 1:
        print('Final Seq')
        ledChanger.setEmotion(index)
        weightAvg()
        print('weight:' + str(weight))
        maxValue = max(weight)
        time.sleep(3)
        index = weight.index(maxValue)
        csvSaver(index)#save today's emotion
        print('setting Final emotion')
        #ledChanger.setEmotion(index)#if isFinal=1, input the data which is averaged
        time.sleep(2)
        print('Glow Starting----')
        ledChanger.glow(index)
        time.sleep(2)
        finalQuiz(index)#Quiz starting
    
def finalQuiz(maxIndex):
    time.sleep(3)
    maxIndex += 1
    ledChanger.finalRainbow()
    ledChanger.changeMode(1)
    mode=1
    while True:
        if(GPIO.input(16) == False):
            print('change mode')
            if(mode > 7):
                mode = 1
            else:
                mode += 1
            ledChanger.changeMode(mode)
            time.sleep(0.05)

        if(GPIO.input(24) == False):
            #choosing
            print('selection')
            if(mode == maxIndex):
                print('---correct answer')
                ledChanger.finalRainbow()
                GPIO.output(12, False)
                break
            else:
                print('---wrong answer')
                ledChanger.wrong(mode)
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
            dataset.append(line)
        lenth=len(dataset)
        f.close()
    sourceData=[]#데이터 10개로 간추리기
    j = lenth-10
    while j < lenth:
        sourceData.append(dataset[j])
        j += 1
    print(sourceData)
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
        encoding = enums.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz = 16000,
        language_code = 'ko-KR')
    response = client.recognize(config, audio)
    for result in response.results:
        return result.alternatives[0].transcript #return transcript

def socketConnect(text):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect(('localhost', 25438))
        s.sendall(text.encode())
        resp = s.recv(16000)
        receivedData=pickle.loads(resp)
        threadFlow.__base__.mro(any).extend(int)
        return receivedData

def threadsStartup():
    iterate = 12
    #iterate = 2 <- 시연용
    thf = None
    for i in range(1, iterate+1):
        if not i == iterate:
            thf=threading.Thread(target=threadFlow, args=(15, 0))#Thread set
            thf.start()#Thread Starting
            time.sleep(16)
        else:
            thf = threading.Thread(target=threadFlow, args=(15, 1))
            thf.start()#Thread Starting
            break
    thf.join()
    print('Emotion Analyzing Finished')

def btnRecog():
    print("____Ready to Function")
    try:
        while True:
            if GPIO.input(23) == False and GPIO.input(24) == False:
                GPIO.output(12, True)
                print('    Emotion Analyzing Start')
                threadsStartup()
                GPIO.output(12, False)
            elif GPIO.input(23) == True and GPIO.input(24) == False:
                print('    Retrospection Start')
                GPIO.output(12, True)
                past = retrospection()
                ledChanger.pastLed(past)
                GPIO.output(12, False)       
    except:
        GPIO.output(12, False)
        GPIO.cleanup()

def main():    
    GPIO.output(12, False)
    print('Eunnarae Start')
    btnRecog()

if __name__ == '__main__':
    main()
