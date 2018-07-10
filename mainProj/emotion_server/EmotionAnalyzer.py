import socket
import codecs
from konlpy.tag import Kkma
from konlpy.utils import pprint
from gensim.models import word2vec
from konlpy.tag import Twitter

kkma=Kkma()#Kkma Morpheme Initializing
twitter = Twitter()

def sentiment():
    filename ='./model/wiki.model'
    model = word2vec.Word2Vec.load(filename)
    standard = ['기쁨','슬픔','분노','놀람','혐오','두려움','반성']
    emotion = '돈'
    weight = []
    for s in standard:
        weight.append(model.wv.similarity(s, emotion))
    print(weight)
    print(model.wv.most_similar(emotion))


'''
def csvList():
    global dictList
    dictList=csvArranger()
    return True

def csvArranger():
    data=[]
    csv=csvLoading()
    rows=csv.split('\r\n')
    for row in rows:
        data.append(row.split(','))
    print(data)
    return data

def csvLoading():
    filename='./dict/polarity.csv'
    csv=codecs.open(filename, 'r', 'euc_kr').read()
    print('csvLoaded')
    return csv
'''
#def morphemeParse(data):
def morphemeParse():
    naturalData=['사랑해요','감사해요','미워요','고마워요','싫어요','불행하다']
    parsedData=[]
    for nd in naturalData:
        parsedData.append(twitter.pos(nd))
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
            #parsedSentence=morphemeParse(recevingData)
            parsedSentence=morphemeParse()#First Receive Data, and then morpe the syntex.
            dataSender(connection, parsedSentence)#Data Sending
        except Exception as e:
            print('Error has been occurred at the responding section')
            print(str(e))
        finally:
            connection.close()
            


if __name__ == '__main__':
    #csvList()#Initializing the csv Dict to upload the csv to global var
    listen('localhost', 25443)
    sentiment()