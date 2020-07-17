from requests import get
import requests
import pandas  as  pd
import numpy  as np 
from os import rename
from os import makedirs
from os.path import exists
from json import loads
from contextlib import closing


def getSnowballSymbol():
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36"}
    df_obj=pd.DataFrame(columns={"symbol","name"})
    print(df_obj)
    for i in range(1,18):
        url=R"https://xueqiu.com/service/v5/stock/screener/quote/list?page={}&size=90&order=desc&order_by=amount&exchange=CN&market=CN&type=sha".format(str(i))

        res=get(url,  headers=headers).content.decode("utf8")
        res=loads(res)["data"]["list"]
        temp=[]
        for v in res:
            temp.append([v['symbol'],v['name']])
        temp_obj=pd.DataFrame(temp,columns={"symbol","name"})

        df_obj=pd.concat([df_obj,temp_obj],axis=0)


    df_obj.to_csv("stock.csv")


if  __name__=="__main__":
    getSnowballSymbol()