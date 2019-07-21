from mm.models import *
from mm.my import network
with open("C:\\Users\\jiakang\\Desktop\\离别时的句子.txt", 'r',encoding='utf-8') as f:
  lineList = f.readlines()
for line in lineList:
    s=Sentence()
    s.content=line
    s.save()