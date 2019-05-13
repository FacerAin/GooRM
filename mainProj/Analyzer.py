# -*- coding: utf-8 -*- 
import socket
import pickle
from gensim.models import word2vec
from konlpy.tag import Twitter
import math

twitter = Twitter()
print('W2V model Loading')
filename = './models/sentiment.model'

model = word2vec.Word2Vec.load(filename)
print('model Loaded!!!')
print('poserLoading')
twitter.pos('poserLoaded')

def sigmoid(x):
    return 1 / (1 + math.exp(3-10*x))
#데이터의 양극화를 위해서 SIGMOID함수를 이용.

def sentiment(data):
    print('sentiment analyze')   
    standard = ['분노','기대','기쁨','존경','두려움','놀람','슬픔','혐오']
    weight = []
    
    for i in standard:
        sum = 0
        z = 0
        for s in data:
            try:
                if(s[0]!='나' and s[0]!='저'):
                
                    if(s[1]=='Adjective'):
                        sum += sigmoid(model.wv.similarity(s[0],i)*2)
                
                    elif(sigmoid(model.wv.similarity(s[0],i))<0.25):
                        sum += 0
                        z += 1
                
                    else:
                        sum += math.tanh(model.wv.similarity(s[0],i))
            except:
                pass

        if not len(data) == z:
            weight.append(sum/(len(data)))
        else:
            weight.append(0)
    zeroSum = 0
    for i in weight:
        zeroSum += i
    
    #if zeroSum=0, weight is Null
    if zeroSum == 0:
        print('data is Null')
        raise Exception
    maximumValue=max(weight)
    index=weight.index(maximumValue)
    print('Sentiment:{}\nweight:{}'.format(standard[index], maximumValue))
    return weight

def morphemeParse(data):
    parsedData= twitter.pos(data,stem=True,norm=True)
    extractedData =[]
    for i in parsedData:
        if i[1] in ['Noun','Adjective','Verb','Exclamation']:
            extractedData.append(i)
    print(extractedData)
    return extractedData
            
def dataReciver(conn):
    print('Entering Reciver')
    data=conn.recv(10000)
    data=str(data.decode())
    print('received Data is┐\n>{}'.format(data))
    return data

def dataSender(conn, data):
    conn.sendall(pickle.dumps(data))
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
        print('ready to response')
        print('\n')
        try:
            sockt.listen(5)
            connection, addr = sockt.accept()
            print('Requested')
            receivedData = dataReciver(connection)
            parsedData = morphemeParse(receivedData)
            emotion = sentiment(parsedData)#sentiment analyzing
            dataSender(connection, emotion)#sending emotion
        except Exception as e:
            print('Error has been occurred at the responding section')
            print(str(e))
        finally:
            connection.close()

if __name__ == '__main__':
    listen('localhost', 25438)
