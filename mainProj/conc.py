import os
import wave
al = os.path.join(
        os.path.dirname(__file__),'1.wav')
be = os.path.join(os.path.dirname(__file__),'2.wav')
CHUNK = 1024
FORMAT = 8
CHANNELS = 1
RATE = 16000
RECORD_SECONDS = 3

wa = wave.open('3.wav', 'wb')
wa.setnchannels(CHANNELS)
wa.setsampwidth(8)
wa.setframerate(RATE)
wa.writeframes(b''.join(al+be))
wa.close()