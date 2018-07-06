import codecs
from bs4 import BeautifulSoup
from konlpy.tag import Twitter
from gensim.models import word2vec

readFp = codecs.open("wiki.txt","r",encoding="utf-8")
outputFp = "wikiout.txt"
writeFp = open(outputFp, "w",encoding="utf-8")

twitter = Twitter()
i = 0
while True:
    line = readFp.readline()
    if not line:
        break
    if i % 10000 == 0:
        print(str(i))
    i +=1
    malist = twitter.pos(line,norm=True,stem=True)
    r = []
    for word in malist:
        if not word[1] in ["Josa","Eomi","Punctuation"]:
            writeFp.write(word[0]+ " ")
writeFp.close()

data = word2vec.Text8Corpus("wikiout.txt")
model = word2vec.Word2Vec(data , size=100)
model.save("wiki.model")
print("done.")
