import thulac
import jieba

import numpy as np
import mmap as mp
from sklearn import datasets
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import BernoulliNB

from sklearn.naive_bayes import BernoulliNB

from ml.DealContent import getWordSet

clf = BernoulliNB()

def loadFile(filename):
    """
    1.函数说明;加载数据集 包括训练集 测试集
    2.filename：文件路径
    3.return：文件返回词条 邮件的类别分类
    """
    # 分词列表 评论分类列表
    contentList = []
    classVec = []
    file = open(filename, "r", encoding='utf-8')
    # 读取文件中的所有行
    contents = file.readlines()

    for line in contents:
        content = line.strip('\n').split(' ')
        print(line)
        classVec.append(int(content[0]))
        del (content[0])
        while '' in content:
            content.remove('')
        contentList.append(content)
    file.close()
    # print(contentList)
    # print(classVec)
    print("已经将分词后的影评，转换成了词汇列表和对应的词向量")
    return contentList, classVec


def createVocabList(dataSet):
    # 使用set的数据结构 去除重复的词汇
    vocabList = set([])
    for doc in dataSet:
        vocabList = vocabList | set(doc)
        # 以列表的形式返回 不重复词汇的集合
    return list(vocabList)



def Words_to_vec(vocabList, wordSet):
    """
    1.函数说明：根据vocabList词汇表 将每个评价分词后在进行向量化 即出现为1 不出现为0
    2.vocablit: 词汇表
    3.wordSet: 生成的词向量
    return：返回的词向量
    """

    returnVec = [0] * len(vocabList)

    for word in wordSet:
        if word in vocabList:
            # 如果在词汇表中的话 便将其所在位置赋为1
            returnVec[vocabList.index(word)] = 1
        else:
            pass
    return returnVec


def trainNB(trainMat, trainLabel):

    clf.fit(trainMat,trainLabel)

def classifyNB(vec2Classify):
    return clf.predict(vec2Classify)


def getMotion(sentence:str):
    wordSet= getWordSet(sentence)
    doc = np.array(Words_to_vec(vocabList, wordSet))
    doc = [doc]
    if classifyNB(doc):
        return 1
    else:
        return -1

trainList, trainLable = loadFile('ml/影评训练.txt')

# print(trainList)
vocabList = createVocabList(trainList)
def init():

    trainMat = []
    cnt = 0

    for train in trainList:
        trainMat.append(Words_to_vec(vocabList, train))
        cnt += 1
        # print("当前正在处理%s组训练数据"%cnt)

    print("训练集数据处理完毕")
    trainNB(np.array(trainMat, dtype='float16'), np.array(trainLable, dtype='float16'))
    print("生成训练集指标")



init()