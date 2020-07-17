import json
import requests
import re
from ConfigDB import RedisDB
 
redisconn =RedisDB()
 
# 设置 cookie 池 随机发送请求 通过 pyppeteer 获取 cookie
# cookie = 'isg=BKys-daL3vWXZsrEm-guE7BjfYPeZVAPxnuHRwbtuNf6EUwbLnUgn6IjNdCpmYhn;_nk_=willhory;sg=y87;uc4=nk4=0%40Fntvrwa38owlUDj0qAG09%2Baxzw%3D%3D&id4=0%40U2grFnDq4HyLuG1Rvgfe41rKooQOK8AX;skt=3354cf1b0d767286;cookie17=UUphzW%2B74ql9lrR6GQ%3D%3D;csg=57fd54f5;tg=5;_cc_=VFC%2FuZ9ajQ%3D%3D;_tb_token_=3e396e363be3e;uc3=nk2=FPCuyFXlnsg%3D&lg2=W5iHLLyFOGW7aA%3D%3D&id2=UUphzW%2B74ql9lrR6GQ%3D%3D&vt3=F8dBxdAVU%2F4solYUaA8%3D;unb=2207824680408;sgcookie=EtXVNZ%2Bfl1PkqNAnHyAeU;cookie1=AClnw4Ef2XgAiphO27VBZYAdUtU0Q770IRHGuj%2FONoY%3D;tracknick=willhory;cookie2=7ef26c57422fd148a81abfc698121c9f;dnk=willhory;_mw_us_time_=1586139209616;cna=n+oNF4rLlwECAXd7sVUoTyUd;mt=ci=0_1;_samesite_flag_=true;thw=cn;l=dBTRur2RQX8w1VjkBOCanurza77OSIRYYuPzaNbMi_5BA6T_rCQOo1kn3F96VfXftcLBqh6Mygv9-etUZ7Dmndd8E5vyUxDc.;_l_g_=Ug%3D%3D;uc1=cookie16=WqG3DMC9UpAPBHGz5QBErFxlCA%3D%3D&lng=zh_CN&cookie15=UIHiLt3xD8xYTw%3D%3D&existShop=false&cookie14=UoTUPOVYc3Duwg%3D%3D&pas=0&cookie21=Vq8l%2BKCLiYXzG52e&tag=8;tfstk=cC2CBef0rm0axkY-CysZTkxaFGkRZJKjV6g3A5B6G4BAQ4rCixvqo_jQZUB2wc1..;lgc=willhory;existShop=MTU4NjE0MDU3Mg%3D%3D;t=6ee50df8336b319b603283abe507cc9d;'
cookie=redisconn.get("tbcookie")
print(cookie,">"*100,type(cookie))
# redisconn.rpush('tbcookiestr',cookie)

cookieStr=str(cookie,encoding='utf-8')
headers = {
    'cookie': cookieStr,
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36"
}
 
rep = requests.get('https://s.taobao.com/search?q=手机&p4ppushleft=1%2C48&s=0&sort=sale-desc ', headers=headers).content
rep.encoding = 'utf-8'
res = rep.text
with open("taobao.html","w") as f:
    f.write(rep.text)
print(res)
 
r = re.compile(r'g_page_config = (.*?)g_srp_loadCss', re.S)
res = r.findall(res)
 
data = res[0].strip().rstrip(';')
dic_data = json.loads(data)
auctions = dic_data.get('mods')['itemlist']['data']['auctions']
 
# print(auctions,len(auctions))
for item in auctions[1:]:
    print(item)
    break
 