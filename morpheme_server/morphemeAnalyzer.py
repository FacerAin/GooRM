import socket
from konlpy.tag import Kkma
from konlpy.utils import pprint

kkma=Kkma()#Kkma Morpheme Initializing

def morphemeParse(data):
    naturalData=kkma.sentences(data)
    parsedData=[]
    for nd in naturalData:
        parsedData.append(kkma.pos(nd))
    print(parsedData)
    return parsedData
            
def dataReciver(conn):
    print('Entering Reciver')
    data=conn.recv(10240)
    data=str(data.decode('utf-8'))
    print('received Data is┐\n>{}'.format(data))
    return data

def dataSender(conn, data):
    conn.sendall(data)
    return

def listen(host, port):
    sockt=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    address=(host, port)
    try:
        print('server Starting...')
        sockt.bind(address)
    except:
        print('server Error. Please retry')
        exit()
    while True:
        print('ready to responde')
        connection, addr=sockt.accept()
        print('Req has been dected')
        try:
            recevingData=dataReciver(connection)
            parsedSentence=morphemeParse(recevingData)#First Receive Data, and then morpe the syntex.
            dataSender(connection, parsedSentence)#Data Sending
        except Exception as e:
            print('Errer has been occurred at the responding section')
            print(str(e))
        finally:
            connection.close()
            


if __name__ == '__main__':
    listen('localhost', 25443)