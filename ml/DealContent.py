import jieba


tycF=open("ml/tyc.txt", "r", encoding='utf-8')
likeF=open("ml/like.txt", "r", encoding='utf-8')

tycs=tycF.readlines()
likes=likeF.readlines()

tycSet=set()


def getWordSet(content:str):
    wordSet=set()
    seg_list = jieba.cut(content, cut_all=False)
    filter_list = []
    for word in seg_list:
        if word not in tycSet:
            filter_list.append(word)
            wordSet.add(word)
    return  wordSet