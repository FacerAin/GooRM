import pyaudio
import wave
import time
def record(outDir, ordd):
    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 16000
    RECORD_SECONDS = 3

    audio = pyaudio.PyAudio()

    stream = audio.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)
    if ordd==2:
        print(a-time.time())
    #recordStarting
    frames = []
    for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        frames.append(data)
    #recordFinishing
    stream.stop_stream()
    stream.close()
    audio.terminate()

    wa = wave.open(outDir, 'wb')
    wa.setnchannels(CHANNELS)
    wa.setsampwidth(audio.get_sample_size(FORMAT))
    wa.setframerate(RATE)
    wa.writeframes(b''.join(frames))
    wa.close()

if __name__ == '__main__':
    

    print('audio1')

    record('1.wav',1)
    a=time.time()
    print('audio2')
    record('2.wav',2)