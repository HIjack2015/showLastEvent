import random
import time
from threading import Thread

from ml.MainLIb import getMotion
from mm.models import *
from mm.my import network

# 这个类是程序的入口，输入一首歌的id，爬所有的热评账户的听歌记录，并记录所有的音乐id，对所有的


#  暂时不要管这个方法了。songid先爬那2000个用户的听歌记录。或者喜欢的音乐
from mm.my.network import replyNegetiveSentenceList, replyPositiveSentenceList


def getMoreSongId():
    return
def getMoreUserId():
    userId=findFollowerUserIdSet.pop()
    userIdSet.update(network.getFollowerIdList(userId))
    if len(userIdSet)==0:
        getMoreList()

# 根据userId找到所有他喜欢的歌和在听的歌。
def addSongIdByUser(userId):
    likeMusic= network.getLikeMusic(userId)
    mostListenMusic= network.getMostListenMusic(userId)

    return  likeMusic.append(mostListenMusic)
#判断数据库是否包含这首歌
def dbContainSong(songId):
    size = len(Song.objects.all().filter(id=songId))
    if size<=0:
        return False
    else:
        return True

def dbContainUser(userId):
    size = len(User.objects.all().filter(id=userId))
    if size<=0:
        return False
    else:
        return True
def addUserToDb(user):
    user.save()
    return


def getCanceledComment(songId):
    comments= network.getCanceldComment(songId)

    return comments





def checkLastEventAndForwardThenComment(userId):
    lastEvent=network.getLastEvent(userId)
    if lastEvent is None:
        return -1
    network.forwardEvent(lastEvent)
    network.commentEvent(lastEvent)
    lastEvent.save()
    return 0


# 这个函数有点问题。现在接口里边没有转发评论这个。先记在数据库里边吧。

def forwardComment(comment):
    comment.save()

    return

songIdSet=set()
listIdSet=set() #2814440999,977452696,976381514,882086412,2347480105,948471242,2422787988,743558697,2467948595
userIdSet=set()
findFollowerUserIdSet=list()
network.loginByPhone('15102279873',"wyjk2015") # 总是要先登录


def addSongToDb(songId):
    song =Song()
    song.id=songId
    song.save()
    pass

def addBySong(songId):
    if dbContainSong(songId):
        return
    canceldCommentSet = getCanceledComment(songId)

    for comment in canceldCommentSet:
        userId = comment.userId
        if dbContainUser(userId):
            continue
        result = checkLastEventAndForwardThenComment(userId)
        emotion = getMotion(comment.content)
        sentence = replyNegetiveSentenceList[random.randint(0, len(replyNegetiveSentenceList) - 1)]
        if emotion == 1:
            sentence = replyPositiveSentenceList[random.randint(0, len(replyPositiveSentenceList) - 1)]

        network.replyComment(songId,comment.id,sentence.content)
        comment.canceld=True
        comment.musicId=songId
        forwardComment(comment)
        user= User()
        addUserToDb(user.getUserByComment(comment))
    addSongToDb(songId)
    if songId in songIdSet:
        songIdSet.remove(songId)
    return
#  不成功返回-1
def addByUser(userId):
    if dbContainUser(userId):
        return
    result = checkLastEventAndForwardThenComment(userId)

    #if userId in userIdSet:
    #    userIdSet.remove(userId)
    user=User()
    user.id= userId

    addUserToDb(user)
    return result



# while True:
#     if len(userIdSet) == 0:
#         getMoreUserId()
#     userId=userIdSet.pop()
#     addByUser(userId)

def getMoreList():
    lists= network.getMoreList()
    for list in lists:
         if len(List.objects.filter(id=list.id))==0:
             listIdSet.add(list.id)
    if len(listIdSet)==0:
        getMoreList()
def addSongIdByList():
    if len(listIdSet)==0:
        getMoreList()
    listId= listIdSet.pop()
    songIdSet.update(network.getSongIdInList(listId))
    songList= List();
    songList.id=listId;
    songList.save()


# 要想使用这个东西 先在控制台 执行python manage.py shell 然后在新的窗口执行  import mm.my.main
# while True:
#     if len(songIdSet) == 0:
#         addSongIdByList()
#     songId=songIdSet.pop()
#     addBySong(songId)

allFollower= network.getAllFollower(1482537933)
for follwer in allFollower:
    findFollowerUserIdSet.append(follwer.id)
while True:
    getMoreUserId()
    while len(userIdSet)!=0:
        addByUser(userIdSet.pop())
        time.sleep(10)

# result=network.getFollower(341731701)
# userIdList=[]
# for user in result:
#     userIdList.append(user.id)
# print(userIdList)
