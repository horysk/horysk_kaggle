from mitmproxy import ctx
import json 

# 所有发出的请求数据包都会被这个方法所处理
# 所谓的处理，我们这里只是打印一下一些项；当然可以修改这些项的值直接给这些项赋值即可
def request(flow):
    # 获取请求对象
    request = flow.request


    # 实例化输出类
    # info = ctx.log.info
    # 打印请求的url
    # info(request.url)
    # 打印请求方法
    # info(request.method)
    # 打印host头
    # info(request.host)
    # 打印请求端口
    # info(str(request.port))
    # 打印所有请求头部
    # info(str(request.headers))
    # 打印cookie头
    # info(str(request.cookies))

# 所有服务器响应的数据包都会被这个方法处理
# 所谓的处理，我们这里只是打印一下一些项
def response(flow):
        
    # with open(r'res.text','a') as f1:
    #     f1.write(flow.response.text)
    if R'/income.json' in flow.request.url:
        response_dict=json.loads(flow.response.text)["data"]
        for r  in   response_dict["list"]:
            #  jing
            if "net_profit" in r.keys():
                print(r["net_profit"],">"*10)
            #  yingye
            if "total_revenue" in r.keys():
                print(r["total_revenue"],">"*10)
            #  yingye
            if "op" in r.keys():
                print(r["op"],">"*10)

        #roe
    if R'/indicator.json' in flow.request.url:
        print(flow.response.text)
        response_dict=json.loads(flow.response.text)["data"]
        for r  in   response_dict["list"]:
            # A  
            if "roe" in r.keys():
                print(r["roe"],">"*10)
            #  $
            if "avg_roe" in r.keys():
                print(r["avg_roe"],">"*10)

    if R'/cash_flow.json' in flow.request.url:
        print(flow.response.text)
        response_dict=json.loads(flow.response.text)["data"]
        for r  in   response_dict["list"]:
            #jinying
            if "ncf_from_oa" in r.keys():
                print(r["ncf_from_oa"][0],">"*10)
            # touzi
            if "ncf_from_ia" in r.keys():
                print(r["ncf_from_ia"],">"*10)
            # chouzi
            if "ncf_from_fa" in r.keys():
                print(r["ncf_from_fa"],">"*10)

    if R'/balance.json' in flow.request.url:
        print(flow.response.text)
        response_dict=json.loads(flow.response.text)["data"]["list"]
        for r in   response_dict:

            if "total_assets" in r.keys():
                print(r["total_assets"],">"*10)
            if "total_liab" in r.keys():
                print(r["total_liab"],">"*10)
            if "asset_liab_ratio" in r.keys():
                print(r["asset_liab_ratio"],">"*10)   # 取同比==前一期
        # print(response_dict,"*"*100,flow.request.url)
        # if 'wareInfo' in response_dict:
        #     for i in response_dict['wareInfo']:
#     # 获取响应对象
#     response = flow.response
#     # 实例化输出类
#     info = ctx.log.info
#     # 打印响应码
#     # info(str(response.status_code))
#     # 打印所有头部
#     info(str(response.headers))
#     # 打印cookie头部
#     # info(str(response.cookies))
#     # 打印响应报文内容
#     info(str(response.text))
#     # if R"/income.json" in str(response.url):
#     #     info(str(response.text))
