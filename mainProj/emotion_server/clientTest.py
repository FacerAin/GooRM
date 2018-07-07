import socket

def run():
  with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect(('localhost', 25443))
    line='안녕하세요. 저는 정의철입니다. 한번 잘 지내봅시다.'
    s.sendall(line.encode())
    resp = s.recv(10000)
    print("fdfdf")
    print(resp)

if __name__ == '__main__':
  run()