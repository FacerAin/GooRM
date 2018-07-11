#-*- coding: utf-8 -*-
import socket
import threading
import time
import wave
import pyaudio
import enum
from google.cloud import speech
from google.cloud.speech import enums, types
color=[0,0,0]
def threadFlow(lenth):
    #text=googleSpeechAPI(record(lenth))
    text='나는 정말 행복합니다'
    print(text)
    emotion=tuple(socketConnect(text))#(max, index)
    print(emotion)
    print('finish')
    #ledChanger=Changer(emotion)

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
    print('##########recording')
    #recordStart
    for i in range(0, int(RATE / CHUNK * lenth)):
        data = stream.read(CHUNK, exception_on_overflow=False)
        frames.append(data)
    #recordFinishing
    print('#####recorded!!')
    stream.stop_stream()
    stream.close()
    audio.terminate()
    return frames#audio sound return

def googleSpeechAPI(content):
    print('googleSpeech Enterting')
    client = speech.SpeechClient()
    audio = types.RecognitionAudio(content=b''.join(content))
    config = types.RecognitionConfig(
        encoding=enums.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=16000,
        language_code='ko-KR')
    response = client.recognize(config, audio)
    for result in response.results:
        print(result.alternatives[0].transcript)
        return result.alternatives[0].transcript

def socketConnect(text):
      with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect(('localhost', 25443))
        s.sendall(text.encode())
        resp = s.recv(10000)
        print(resp)
        return resp

def main():
    lenth=10#recording lenth
    while True:
        thf=threading.Thread(target=threadFlow, args=(lenth,))#Thread set
        print('start')
        thf.start()#Thread Starting
        time.sleep(lenth+1)
        print('sleepOver')


if __name__ == '__main__':
    main()
