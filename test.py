from konlpy.tag import Kkma

kkma=Kkma()

def morphemeParse(data):
    naturalData=kkma.sentences(data)
    parsedData=[]
    for nd in naturalData:
        parsedData.append(kkma.pos(nd))
    print(parsedData[1][1][0])
    print(parsedData)

morphemeParse('너는 누구니? 나는 올라프야. 너는 뭐하는 친구니?')