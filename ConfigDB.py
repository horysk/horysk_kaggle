# _*_ coding:utf-8 _*_
__author__ = 'Will'

import redis
from  random import randint
from redis.sentinel import Sentinel
from pymongo import MongoClient,ReadPreference
from datetime import datetime

class MongoDB(object):
    def __init__(self,DBName, CollectionName):

        self.client = MongoClient('mongodb://root:admin@172.20.1.187:27011,172.20.1.187:27018,172.20.1.187:27019,172.20.1.187:27020,172.20.1.187:27021,172.20.1.187:27022', replicaset='mongos', readPreference='secondaryPreferred')
        self.db_name = self.client.get_database(DBName,read_preference=ReadPreference.NEAREST)
        self.mongoDbClient = self.db_name[CollectionName]

    def getID(self,idName):
        inx=self.mongoDbClient.find_and_modify({"_id": idName}, update={"$inc": {'index': 1}}, upsert=True)
        try:
            id=inx["index"]
        except :
            id=0
        return id

    def getInfo(self, arg):
        '''获取一条数据'''
        print(arg)
        resultData=self.mongoDbClient.find_one(arg)
        return resultData

    def insertDict(self,arg):
        self.mongoDbClient.insert(arg)

    def updateDict(self,arg,val):
        self.mongoDbClient.update(arg,val,True)

    def getHigh(self):
        print("starting")
        # find_dic={"High":1}
        # find_dic={"High":1}
        # result=self.mongoDbClient.find(find_dic,{"code":1})
        result=self.mongoDbClient.find({})

        
        # return result
        print(result,"6666")
        if result.count() >0:
            for i in result:
                yield i

class RedisDB(object):
    '''初始化Redis数据库'''
    def __init__(self, db=0):
        self.sentinel = Sentinel([('172.20.1.157', 26379),
                            ('172.20.1.157', 26380),
                            ('172.20.1.157', 26381)
                            ],
                            socket_timeout=0.5)
        self.RedisDb = self.sentinel.master_for('local-master', socket_timeout=0.5, password='redis', db=db)

    def lpush(self, key, coent):
        try:
            self.RedisDb.lpush(key, coent)
        except Exception as e:
            print(e)

    def rpush(self, key, coent):
        try:
            self.RedisDb.rpush(key, coent)
        except Exception as e:
            print(e)

    def get(self, key):
        try:
            
            # result=self.RedisDb.lpop(key,0,-1)
            result=self.RedisDb.lpop(key)
            print(key,result,'&'*10)
            return result
        except Exception as e:
            print(e)
            return False

    def sget(self, key):
        try:
            num=self.RedisDb.llen(key)
            inx=randint(0, num)
            result=self.RedisDb.lindex(key,inx)
            print(key,result,'*'*10)
            return result
        except Exception as e:
            print(e)
            return False

    def GetIP(self):
        IP = self.RedisDb.get("ip")
        ipdata = str(IP).replace("\n", "")
        proxies = {
            'http': 'http://' + ipdata,
            'https': 'https://' + ipdata,
        }
        return proxies



class RedisPool(RedisDB):
    def __init__(self, db=0):
            pool = redis.ConnectionPool(host='172.20.1.157',port='6399',password='admin123',db=db)
            self.RedisDb = redis.Redis(connection_pool=pool)



# ips = RedisDB()