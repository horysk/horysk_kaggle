# -*- encoding=utf8 -*-
__author__ = "shenxixiang"

from airtest.core.api import *
from airtest.cli.parser import cli_setup
import pandas as pd
import numpy as np


if not cli_setup():
    auto_setup(__file__, logdir=True, devices=[
            "Android://172.20.1.13:5037/172.20.1.13:7555",
    ])


# script content
print("start...")


# generate html report
# from airtest.report.report import simple_report
# simple_report(__file__, logpath=True)


from poco.drivers.android.uiautomation import AndroidUiautomationPoco
poco = AndroidUiautomationPoco(use_airtest_input=True, screenshot_each_action=False)


def init():
    poco(text="雪球股票").click()
    sleep(5)
    poco(name="com.xueqiu.android:id/stock_name_one").click()
    sleep(1)
    poco.swipe([0.5, 0.8], [0.5, 0.2])
    sleep(5)
    poco(name="com.xueqiu.android:id/action_search").click()
    sleep(2)

def getStockDetail(symbol):
    # poco(name="com.xueqiu.android:id/action_delete_text").click()
    try:
        poco(name="com.xueqiu.android:id/action_search").click()
        sleep(2)
        poco(name="com.xueqiu.android:id/search_input_text").set_text(symbol)
    except:
        poco(name="com.xueqiu.android:id/search_input_text").set_text(symbol)
    sleep(2)
    poco(name='com.xueqiu.android:id/code').click()
    sleep(2)
    poco(name="com.xueqiu.android:id/stockCode",textMatches=symbol).click()
    sleep(2)
    poco.swipe([0.5, 0.8], [0.5, 0.2])
    poco(name="com.xueqiu.android:id/text",textMatches='财务').click()
    sleep(1)
    poco.swipe([0.5, 0.8], [0.5, 0.2])

if __name__=="__main__":
    
    # init()
    df=pd.read_csv("stock.csv")
    for r in df['symbol']:
        getStockDetail(r)




