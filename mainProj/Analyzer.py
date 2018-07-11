#-*- coding: utf-8 -*-
import socket
from gensim.models import word2vec
from konlpy.tag import Twitter
twitter = Twitter()
filename = './models/wiki.model'
print('W2V model Loading')
model = word2vec.Word2Vec.load(filename)
print('model Loaded!!!')

def sentiment(data):
    print(data)    
    standard = ['분노','기대','기쁨','존경','두려움','놀람','슬픔','혐오']
    weight = []
    for i in standard:
        sum = 0
    
        for s in data:
        
            sum += model.wv.similarity(s[0],i)
        if not weight == 0:
            weight.append(sum/len(data))
    
    maximumValue=max(weight)
    index=maximumValue.index(maximumValue)
    print('Sentiment:{}\nweight:{}'.format(standard[index], maximumValue))
    return (maximumValue, index)

def morphemeParse(data):
    parsedData= twitter.pos(data,stem=True,norm=True)
    print(parsedData)
    return parsedData
            
def dataReciver(conn):
    print('Entering Reciver')
    data=conn.recv(10000)
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
        sockt.listen(5)
        connection, addr=sockt.accept()
        print('Requested')
        try:
            receivedData=dataReciver(connection)
            emotion=sentiment(receivedData)#sentiment analyzing
            dataSender(connection, emotion)#sending emotion
        except Exception as e:
            print('Error has been occurred at the responding section')
            print(str(e))
        finally:
            connection.close()



if __name__ == '__main__':
    listen('localhost', 25443)