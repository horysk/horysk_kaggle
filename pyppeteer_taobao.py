# -*- coding: utf-8 -*-
# __author__ = "will"  
# Date: 2019-10-6  Python: 3.7

import os
import time
import random
import asyncio
import pyppeteer
from urllib.parse import urlsplit
from exe_js import js1, js3, js4, js5
from  ConfigDB import RedisDB

# from scripts import scripts

# BASE_DIR = os.path.dirname(__file__)


class LoginTaoBao:
    """
    类异步
    """
    pyppeteer.DEBUG = True
    page = None
    redisconn=RedisDB(0)
    cookie=redisconn.get("tbcookie")
    print(cookie,">"*100,type(cookie))
    redisconn.lpush('tbcookie',cookie)
    cookieStr=str(cookie,encoding='utf-8')

    async def _injection_js(self):
        """注入js
        """
        await self.page.evaluateOnNewDocument('() =>{ Object.defineProperties(navigator,'
                                   '{ webdriver:{ get: () => false } }) }')  # 本页刷新后值不变
    

    async def intercept_request(req):
        """请求过滤"""
        
        if req.resourceType in ['image', 'media', 'eventsource', 'websocket']:
            await req.abort()
        else:
            await req.continue_()


    async def intercept_response(res):
        print(res)
        # resourceType = res.request.resourceType
        # if resourceType in ['xhr', 'fetch']:
        #     resp = await res.text()

        #     url = res.url
        #     tokens = urlsplit(url)

        #     folder = BASE_DIR + '/' + 'data/' + tokens.netloc + tokens.path + "/"
        #     if not os.path.exists(folder):
        #         os.makedirs(folder, exist_ok=True)
        #     filename = os.path.join(folder, str(int(time.time())) + '.json')
        #     with open(filename, 'w', encoding='utf-8') as f:
        #         f.write(resp)


    async def _init(self):
        """初始化浏览器
        """
        browser = await pyppeteer.launch({'headless': False,
                                          # 'userDataDir': './userdata',
                                          'args': [
                                              '--window-size={1300},{600}'
                                              '--disable-extensions',
                                              '--hide-scrollbars',
                                              '--disable-bundled-ppapi-flash',
                                              '--mute-audio',
                                              '--no-sandbox',
                                              '--disable-setuid-sandbox',
                                              '--disable-gpu',
                                              '--disable-infobars'
                                          ],
                                          'dumpio': True
                                          })
        self.page = await browser.newPage()
        # await self.page.setRequestInterception(True)
        # self.page.on('request', self.intercept_request)
        # self.page.on('response', self.intercept_response)
        # 设置浏览器头部
        await self.page.setUserAgent('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                                     '(KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36 Edge/16.16299')
        # 设置浏览器大小
        await self.page.setViewport({'width': 1200, 'height': 600})
        await self.page.evaluate(js1)
        await self.page.evaluate(js3)
        await self.page.evaluate(js4)
        await self.page.evaluate(js5)

    async def get_cookie(self):
        cookies_list = await self.page.cookies()
        cookies = ''
        for cookie in cookies_list:
            str_cookie = '{0}={1};'
            str_cookie = str_cookie.format(cookie.get('name'), cookie.get('value'))
            cookies += str_cookie
        print(cookies)
        # return cookies

    async def mouse_slider(self):
        """滑动滑块
        """
        await asyncio.sleep(3)
        try:
            await self.page.hover('#nc_1_n1z')
            # 鼠标按下按钮
            await self.page.mouse.down()
            # 移动鼠标
            await self.page.mouse.move(2000, 0, {'steps': 30})
            # 松开鼠标
            await self.page.mouse.up()
            await asyncio.sleep(2)
        except Exception as e:
            print(e, '      :错误')
            return None
        else:
            await asyncio.sleep(3)
            # 获取元素内容
            slider_again = await self.page.querySelectorEval('#nc_1__scale_text', 'node => node.textContent')
            if slider_again != '验证通过':
                return None
            else:
                print('验证通过')
                return True

    async def main(self, username_, pwd_,url):
        """登陆
        """
        # 初始化浏览器
        await self._init()
        # 注入js
        await self._injection_js()
        # 打开淘宝登陆页面
        # await self.page.goto('https://login.1688.com/member/signin.htm')
        await self.page.goto(url)

        # await self.page.goto('https://www.taobao.com')
        # time.sleep(1000000)
        # 点击密码登陆按钮
        # await self.page.click('div.login-switch')
        time.sleep(random.random() * 2)
        await self.page.setCookie(cookieStr)
        # 输入用户名
        try:
            await self.page.type('#fm-login-id', username_, {'delay': random.randint(100, 151) - 50})
            # 输入密码
            await self.page.type('#fm-login-password', pwd_, {'delay': random.randint(100, 151)})
        except:
            await page.type('#TPL_username_1', username_, {'delay': random.randint(100, 151) - 50})
            await page.type('#TPL_password_1', pwd_, {'delay': random.randint(100, 151)})
            await page.keyboard.press('Enter')
        time.sleep(random.random() * 2)
        # 获取滑块元素
        try:
            slider = await self.page.Jeval('#nocaptcha', 'node => node.style')
            if slider:
                print('有滑块')
                # 移动滑块
                flag = await self.mouse_slider()
                if not flag:    
                    print('滑动滑块失败')
                    return None
                time.sleep(random.random() + 1.5)
        except:
            print("contium")
            # 点击登陆
            print('点击登陆')
            await self.page.click('.password-login')
            await asyncio.sleep(1000)

        print('点击登陆')
        await self.page.keyboard.press('Enter')

        cookies = await self.get_cookie()
        time.sleep(10000)


if __name__ == '__main__':
    username = input('请输入淘宝用户名')
    password = input('密码')
    url="https://login.taobao.com"
    # url="https://login.1688.com/member/signin.htm"
    login = LoginTaoBao()
    loop = asyncio.get_event_loop()
    task = asyncio.ensure_future(login.main(username, password,url))
    loop.run_until_complete(task)