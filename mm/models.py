from django.db import models


# Create your models here.
class Song(models.Model):
    id = models.BigIntegerField
    hotCommentCount = models.IntegerField(blank=True, null=True)
    closedCommentCount = models.IntegerField(blank=True, null=True)
    insertDate = models.DateTimeField(blank=True, null=True)
    updateDate = models.DateTimeField(blank=True, null=True)
    name = models.TextField(blank=True, null=True)
    looked = models.BooleanField(blank=True, null=True)

class Sentence(models.Model):

    content= models.TextField(blank=True, null=True)
    emotion=models.IntegerField(blank=True,null=True)
class Count(models.Model):
    id=models.IntegerField
class User(models.Model):
    id = models.IntegerField
    province = models.IntegerField(blank=True, null=True)
    signature = models.TextField(blank=True, null=True)  # 签名
    nickName = models.TextField(blank=True, null=True)

    follows = models.IntegerField(blank=True, null=True)
    followeds = models.IntegerField(blank=True, null=True)
    eventCount = models.IntegerField(blank=True, null=True)
    playlistCount = models.IntegerField(blank=True, null=True)
    vipType = models.IntegerField(blank=True, null=True)  # 0 表示不是vip

    looked = models.BooleanField(blank=True, null=True)

    def getUserByComment(self, comment):
        a = User()

        a.id = comment.userId
        a.province = comment.province
        a.nickName = comment.nickName
        a.signature = comment.signature

        return a


class Comment(models.Model):
    id = models.BigIntegerField
    musicId=models.TextField(blank=True, null=True)
    userId = models.IntegerField(blank=True, null=True)
    province = models.IntegerField(blank=True, null=True)
    nickName = models.TextField(blank=True, null=True)
    signature = models.TextField(blank=True, null=True)  # 签名

    content = models.TextField(blank=True, null=True)
    likedCount = models.IntegerField(blank=True, null=True)
    commentTime = models.DateTimeField(blank=True, null=True)
    insertDate = models.DateTimeField(blank=True, null=True)
    updateDate = models.DateTimeField(blank=True, null=True)
    canceld=models.BooleanField(blank=True, null=True)

class List(models.Model):
    id = models.BigIntegerField
class Event(models.Model):
    id = models.IntegerField
    threadId = models.TextField(blank=True, null=True)
    userId = models.IntegerField(blank=True, null=True)
    province = models.IntegerField(blank=True, null=True)
    signature = models.TextField(blank=True, null=True)  # 签名
    nickName = models.TextField(blank=True, null=True)

    json = models.TextField(blank=True, null=True)  # 这个里边是动态的内容需要解析
    eventTime = models.DateTimeField(blank=True, null=True)
    insertDate = models.DateTimeField(blank=True, null=True)
    updateDate = models.DateTimeField(blank=True, null=True)
