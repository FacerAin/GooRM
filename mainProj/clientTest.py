import socket

def run():
  with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect(('localhost', 25443))
    line='나는 행복합니다.'
    s.sendall(line.encode())
    resp = s.recv(10000)

    print(tuple(resp))

if __name__ == '__main__':
  run()