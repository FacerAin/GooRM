import socket
import pickle
def socketConnect(text):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect(('localhost', 25438))
        s.sendall(text.encode())
        resp = s.recv(16000)
        receivedData=pickle.loads(resp)
        print(receivedData)
        return receivedData

while True:
    socketConnect(input())
