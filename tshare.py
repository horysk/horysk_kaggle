import akshare as ak
import numpy as np
import pandas  as pd
import tushare  as ts 
import requests as rq
import time
import json
from ConfigDB import  MongoDB,RedisPool
db = MongoDB('Stock','Increate')
red_=RedisPool(db=1)


def stock_ak(code,):
    # dataF=stock_financial_abstract_df = ak.stock_financial_abstract(stock="600004")
    # dataF=stock_em_yjyg_df = ak.stock_em_yjyg(date="2019-03-31")
    # for i in code:
    data={}
    data["code"]=code
    data['id']=db.getID("stock")
    try:
        df=stock_financial_analysis_indicator_df = ak.stock_financial_analysis_indicator(stock=code)
        for item,row in df.iteritems():
            r=np.array(row).tolist()
            data[item]=r
            # print(r[:12])
            if item=="净资产增长率(%)":
                r=[i if i !="--" else "0" for i in r  ]
                num=np.sum(list(map(lambda x: float(x) >= 20, r[:15])))
                
                if num > 12 :
                    data['High']=1
    except Exception as e:
        print(e)
        
    # increate=np.array(df["净资产增长率(%)"]).tolist()
    # print(data)
    
    db.insertDict(data)
    # write = pd.ExcelWriter("stock_ak_increate.xlsx")
    # df=pd.read_excel("stock_ak.xlsx",index_col=0,)
    # for i in df.index:
    # print(df["净资产增长率(%)"])

        # if df.
    # dataF.to_excel(r"stock_ak.xlsx",)
    # excel_header="financial"
    # with pd.ExcelWriter('stock_ak.xlsx') as writer:  # doctest: +SKIP
    # df["净资产增长率(%)"].to_excel(write, sheet_name='Sheet_name_1',header=excel_header,index=False)

        # df2.to_excel(writer, sheet_name='Sheet_name_2')
    # print(df)
    # print(stock_financial_abstract_df)
    # write.save()

def  read_code():
    code=pd.read_excel("tshare.xlsx",index_col=0,)
    dt=np.array(code.ts_code)
    dt=dt.tolist()
    res=[]
    for i in dt:
        i=i.split(".")[::-1]
        i="".join(i)
        res.append(i)
        # print(i)
    return res
    

def stock_tu():

    pro = ts.pro_api("3bffe33c882b7cf4c90d49b32bd476515271003520a9b77232685195")
    data = pro.stock_basic(exchange='', list_status='L', fields='ts_code,symbol,name,area,industry,list_date')
    # ts.set_token('your token here')
    # with open("tushare.txt",'w',encoding='utf-8') as f:
    #     f.write(ts.get_industry_classified())
    # print(type(data))
    # print(data.ts_code)
    data.to_excel(r"tshare.xlsx",)
    dt=np.array(data.ts_code)
    dt=dt.tolist()



def snowball():
    user_agent = "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36"
    cookie="device_id=24700f9f1986800ab4fcc880530dd0ed; s=cx11ywwoko; xq_a_token=083cb48f59c4e464135799326ae6b063cbe71b9a; xqat=083cb48f59c4e464135799326ae6b063cbe71b9a; xq_r_token=5ca3ac1644c5df08523173779a080773967ff6db; xq_id_token=eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJ1aWQiOjU0OTY5NzYyOTQsImlzcyI6InVjIiwiZXhwIjoxNTk1MjkxMzU5LCJjdG0iOjE1OTM2ODk4OTYyMjksImNpZCI6ImQ5ZDBuNEFadXAifQ.fVSs6LDfY-wTqxk6Gs8bzkF3RolAyrPdCsCNp6lddScjseNUn9sQg6Y_tKQn81huBuFpgh7MmkzbGKUvdW8tfVzlmzhZ_GQ5kOQ-GbxZy311kf7ywWh-U8hyRpdT2Fnu1G5dt_9f2cdM5knllx_Un6I0GxR-7TiNIUPGayL3jf7sRu4vkONHU4lLtsFw2b7AFqPaylFtmcQDx_NPQdHT20l-i-TWo9oxpJ8XzHlbsO-py_t2kpvmjj2_sZmkioIVendhqIG3m7NlPYFv9oaoPwo-d9vptZ9kRGeORRDJx9MUU6ChiNQCUz2Wh3Tk4eImXSucbMT6eThJUtX6Y2xTZg; xq_is_login=1; u=5496976294; bid=f244c8f52388bb444c5461130c3ddc9a_kc4rhk37; Hm_lvt_1db88642e346389874251b5a1eded6e3=1593692705,1593693631,1593693945,1593758896; Hm_lpvt_1db88642e346389874251b5a1eded6e3=1593764284"
    headers = {
    'cookie': cookie,
    "user-agent": user_agent
}
    # for i in dt:
    #     i=i.split(".")[::-1]
    #     i="".join(i)
    # for i in range(1,18):
    #     #  stock_list
    #     url=R"https://xueqiu.com/service/v5/stock/screener/quote/list?page={}&size=90&order=desc&order_by=amount&exchange=CN&market=CN&type=sha".format(str(i))
    #     # stock finance
    #     print(i)

    i="SZ000858"
    url=R"https://stock.xueqiu.com/v5/stock/finance/cn/income.json?symbol={}&type=all&is_detail=true".format(str(i))
    res=rq.get(url, headers=headers).content.decode("utf8")

    d_list=json.loads(res)["data"]["list"]
    for i in d_list:
        # s=i["net_profit_atsopc_yoy"]
        for k in i.keys():
            # k
            print(k,"\r\n")


if __name__=="__main__":
    # stock_tu()
    # stock_ak()
    code=read_code()
    # # # print(code)
    for i in code:
        print(i)
        if i:
            red_.lpush("code",i)
            # stock_ak(i[2:])
    # while True:
    #     red_.get("code")
    #     stock_ak(str(red_.get("code"),encoding="utf-8")[2:])
    #     time.sleep(5)
    # ts=db.getHigh()
    # for t in ts:
    #     # print("*"*10,)
    #     try:
    #         data=t.pop("净资产报酬率(%)")
    #         r=[i if i !="--" else "0" for i in data] 
    #         k=1
    #         inc_list=[]
    #         for i in range(1,5):
    #             start =(k-1)*1
    #             end=4*k
    #             r[start:end]
    #             temp=0
    #             for i in r[:4]:
    #                 temp += float(i)
    #             inc=temp/4
    #             if inc>20:
    #                 inc_list.append(inc) 
    #             k+=1
    #         num=np.sum(list(map(lambda x: float(x) >= 20, inc_list)))
        
    #         if num == 4 :
    #             print(t["code"],inc_list)
    #     except:
    #         pass
    # for i in ts:
    #     print(i)
    # code="000858"
    # stock_ak(code)
    
    # snowball()
    