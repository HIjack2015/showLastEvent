from datetime import datetime
import time
import requests
import random
from  mm.my.util import  Util
delay=2
from mm.models import Comment, Event, User, Sentence, Count, List

server = "http://127.0.0.1:3000/"
headers = {
'Upgrade-Insecure-Requests': "1",
'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.80 Safari/537.36',
'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
'Accept-Encoding': 'gzip, deflate, br',
'Accept-Language': 'en,zh-CN;q=0.9,zh;q=0.8',

}

s = requests.Session()
s.headers.update(headers)


def loginByPhone(phoneNo, password):
    r = s.post(server + "login/cellphone", json={"phone": phoneNo, "password": password})
    if r.status_code != 200:
        print("error network")
        return False
    json = r.json()
    time.sleep(delay)
    if json.get("code") != 200:
        return False
    return True
def replyComment(musicId,commentId,content):
    r=s.post(server + "comment/comment?musicId="+str(musicId)+"&commentId="+str(commentId)+"&content="+content)
    time.sleep(delay)
    return
def existSong(songId):
    time.sleep(3)
    r = requests.post(server + "comment/hot?id=" + str(songId) + "&type=0")
    json = r.json()
    total= json.get("total")
    if total==0:
        return False
    else:
        return True
def getCanceldComment(songId):
    r =  s.post(server + "comment/hot?id=" + str(songId) + "&type=0")

    json = r.json()
    time.sleep(delay)
    hotComments = json.get("hotComments")
    canceldComments = []
    comments = []
    if hotComments is None:
        return  canceldComments
    for hotComment in hotComments:
        comment = Comment()
        comment.id = hotComment.get("commentId")
        user = hotComment.get("user")

        comment.userId = user.get("userId")
        comment.nickName = user.get("nickname")

        comment.insertDate = datetime.now()
        comment.updateDate = datetime.now()

        comment.content = hotComment.get("content")
        comment.likedCount = hotComment.get("likedCount")
        comments.append(comment)

    for comment in comments:
        if comment.nickName != "帐号已注销" and comment.nickName != "账号已注销":
            comment.save()
        else:
            canceldComments.append(comment)
    return canceldComments


def getLastEvent(userId):
    r = s.get(server + "user/event?uid=" + str(userId))

    json = r.json()
    time.sleep(delay)

    if json is None:
        return None
    if len(json.get("events")) == 0:
        return None
    lastEvent = json.get("events")[0]
    event = Event()
    user = lastEvent.get("user")

    event.id = lastEvent.get("id")

    event.userId = user.get("userId")
    event.province = user.get("province")
    event.nickName = user.get("nickname")
    event.signature = user.get("signature")

    event.json = lastEvent.get("json")
  #  event.eventTime = lastEvent.get("eventTime")
    event.insertDate = datetime.now()
    event.updateDate = datetime.now()
    event.threadId=lastEvent.get("info").get("threadId")
    return event
dbCount=Count.objects.all()[0]
count= dbCount.id;
def forwardEvent(lastEvent=Event):
    global  count

    cnCount=Util.num2cn(count+1)
    r = s.get(server + "event/forward?evId=" + str(lastEvent.id) + "&uid=" + str(lastEvent.userId) + "&forwards="+cnCount)
    if(r.status_code==200):
        dbCount.delete()
        count=count+1
        dbCount.id=count
        dbCount.save()
    print(r)
    json = r.json()
    time.sleep(delay)
    return
sentenceList= list(Sentence.objects.all())
sentenceLen=len(sentenceList)
def commentEvent(lastEvent:Event):
    sentence= sentenceList[random.randint(0, sentenceLen - 1)]
    content=sentence.content
    r = s.get(server + "comment?threadId=" + str(lastEvent.threadId) + "&content="+content+"&type=6&t=1")
    json = r.json()
    time.sleep(delay)
    return
def getRandomSentence():
    return     sentenceList[random.randint(0, sentenceLen - 1)].content
# 返回 listOf User object
def getFollower(userId):
    r = s.get(server+"user/follows?limit=2000&uid="+str(userId))
    json = r.json()
    time.sleep(delay)
    userList=[]
    for userJson in json.get("follow"):
        accountStatus=userJson.get("accountStatus")
        if accountStatus!=30: # 已经注销
            continue
        user=User()
        user.id=userJson.get("userId")

        user.nickName= userJson.get("nickname")
        user.signature = userJson.get("signature")
        user.looked=False
        user.follows = userJson.get("follows")
        user.followeds = userJson.get("followed")
        user.eventCount=userJson.get("eventCount")
        user.playlistCount = userJson.get("playlistCount")
        user.vipType=userJson.get("vipType")

        userList.append(user)
    return userList
def getFollowerIdList(userId):
    userList=getFollower(userId)
    userIdSet=set()
    for user in userList:
        userIdSet.add(user.id)
    return userIdSet




def delEvent(eventId):
    s.get(server + "event/del?evId=" + str(eventId))

def delAllEvent(userId):
    json = s.get(server+"user/event?uid="+ str(userId)+"&random="+str(random.randint(1,155225555))).json()
    eventDict=json.get("events")
    for event in  json.get("events"):
        eventId=   event.get("id")
        delEvent(eventId)
    if len(eventDict)>1:
        delAllEvent(userId)

def getLikeMusic(userId):
    return []


def getMostListenMusic(userId):
    return []
def getSongIdInList(listId):
    r = s.get(server+"playlist/detail?id="+str(listId))
    json = r.json()
    time.sleep(delay)
    songIdList=set()
    for songJson in json.get("playlist").get("tracks"):
        songIdList.add(songJson.get("id"))
    return songIdList
def getUserIdByName():
    userIdList = set()

    offset=0
    while offset<600:
        r = s.get(server + "search?keywords=账号已注销&type=1002&limit=100&offset="+str(offset))
        json = r.json()
        for userJson in json.get("result").get("userprofiles"):
            if userJson.get("nickname")=="账号已注销" and  userJson.get("accountStatus")==30:
              userIdList.add(userJson.get("userId"))
        offset=offset+100
    return userIdList

tags=["电子", "校园", "性感", "韩语", "午休",
      "游戏",  "舞曲", "粤语", "小语种", "下午茶", "70后", "说唱",
      "治愈", "轻音乐", "80后", "放松", "地铁", "爵士", "90后", "驾车",
      "孤独", "感动", "运动", "网络歌曲", "乡村", "兴奋", "KTV", "旅行",
      "R&B/Soul", "古典", "快乐", "散步", "经典", "翻唱", "安静", "民族",
      "酒吧", "思念", "吉他", "英伦", "金属", "钢琴", "朋克", "器乐", "榜单",
      "蓝调", "雷鬼", "00后", "世界音乐", "拉丁", "另类/独立", "New Age", "古风", "后摇", "Bossa Nova"]
currentTag=0
def getMoreList():
    global  currentTag
    r = s.get(server + "top/playlist?limit=1000&cat="+tags[currentTag])
    print(tags[currentTag]+"tag")
    playlists= r.json().get("playlists")
    listSet= set()
    for playlist in playlists:
        list=List()
        list.id=playlist.get("id")
        listSet.add(list)

    currentTag=currentTag+1
    return listSet