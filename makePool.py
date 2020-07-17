
from threading import Timer
import psutil
import time
import datetime
from ConfigDB import RedisDB,RedisPool
import requests
from user_agents import  agents
# redisconn=RedisDB(db=0)
# for i in agents:
#     redisconn.lpush("user-agent",i)
# url="http://tpv.daxiangdaili.com/ip/?tid=556754546957144&num=1000&category=2&protocol=https"

URL="http://tpv.daxiangdaili.com/ip/?tid=556754546957144&num=1000&delay=3&category=2&ports=80"

def getIP(url,interval=60):
    ips=requests.get(url).content.decode("utf8").split("\r\n")
    if 'ERROR' in ips[0]:
        return
    print(ips)
    r = RedisPool(db=0)
    for i in ips:
        r.lpush("daxiangIP",i)
    Timer(interval, getIP,(url,)).start()

def getUA(interval=60):
    print("start UA...")
    r = RedisPool(db=0)
    for i in agents:
        r.lpush("user-agent",i)
    Timer(interval, getUA).start()    



if __name__ == "__main__":
    area=["香港","澳门","广州","深圳","北京","上海",'杭州','河北','山西','辽宁','吉林','黑龙江','江苏','浙江','安徽','福建','江西',
    '山东','河南','湖北','湖南','广东','海南','四川','贵州','云南','陕西','甘肃','青岛','台湾']
    # for i in area:
        # url=URL.format(i)
    getIP(URL,60)
    getUA(60)

