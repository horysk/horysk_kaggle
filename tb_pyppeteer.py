import asyncio
import time
import json
from pyppeteer.launcher import launch
from alifunc import mouse_slide, input_time_random
from exe_js import js1, js3, js4, js5
import tkinter
from  ConfigDB import RedisDB
redisconn=RedisDB(db=0)

 
 
def screen_size():
    """使用tkinter获取屏幕大小"""
    tk = tkinter.Tk()
    width = tk.winfo_screenwidth()
    height = tk.winfo_screenheight()
    tk.quit()
    return width, height
 
def _patch_pyppeteer():
    from typing import Any
    from pyppeteer import connection, launcher
    import websockets.client

    class PatchedConnection(connection.Connection):  # type: ignore
        def __init__(self, *args: Any, **kwargs: Any) -> None:
            super().__init__(*args, **kwargs)
            # the _ws argument is not yet connected, can simply be replaced with another
            # with better defaults.
            self._ws = websockets.client.connect(
                self._url,
                loop=self._loop,
                # the following parameters are all passed to WebSocketCommonProtocol
                # which markes all three as Optional, but connect() doesn't, hence the liberal
                # use of type: ignore on these lines.
                # fixed upstream but not yet released, see aaugustin/websockets#93ad88
                max_size=None,  # type: ignore
                ping_interval=None,  # type: ignore
                ping_timeout=None,  # type: ignore
            )

    connection.Connection = PatchedConnection
    # also imported as a  global in pyppeteer.launcher
    launcher.Connection = PatchedConnection

class  Browser():
    def __init__(self):
        super().__init__()
        loop = asyncio.get_event_loop()
        task = asyncio.ensure_future(self.getbrowser())
        loop.run_until_complete(task)

    async def getbrowser(self):
        ua=redisconn.get("user-agent")
        redisconn.rpush('user-agent',ua)
        self.browser = await launch({'headless': False,'timeout':0, 'args': ['--no-sandbox'], 'dumpio': True}, userDataDir='./userdata',
                            args=[
                                '--window-size=1366,768',
                                '--disable-extensions',
                                '--hide-scrollbars',
                                '--disable-bundled-ppapi-flash',
                                '--mute-audio',
                                '--disable-setuid-sandbox',
                                '--disable-gpu',
                                '--disable-infobars'
                                ])
        self.page = await self.browser.newPage()
        width, height = screen_size()
        await self.page.setViewport(viewport={"width": width, "height": height})
        await self.page.setUserAgent(str(ua,encoding='utf-8'))
    
        await self.page.evaluate(js1)
        await self.page.evaluate(js3)
        await self.page.evaluate(js4)
        await self.page.evaluate(js5)
        return self.page
        # pwd_login = await page.querySelector('.J_Quick2Static')
        # print(await (await pwd_login.getProperty('textContent')).jsonValue())
        # await pwd_login.click()

    async def go_url(self,username,pwd,url):
        await self.page.goto(url,{'timeout':0})
        try:
            await self.page.type('#fm-login-id', username, {'delay': input_time_random() - 50})
            await self.page.type('#fm-login-password', pwd, {'delay': input_time_random()})
        except:
            await self.page.type('#TPL_username_1', username, {'delay': input_time_random() - 50})
            await self.page.type('#TPL_password_1', pwd, {'delay': input_time_random()})
        await self.page.keyboard.press('Enter')
        time.sleep(5)
    
        await self.page.screenshot({'path': './headless-test-result.png'})
        await self.get_cookie(self.page)
        time.sleep(2)
        # try:
        #     slider = await page.Jeval('#nocaptcha', 'node => node.style')  # 是否有滑块
        #     if slider:
        #         print('出现滑块情况判定')
        #         await page.screenshot({'path': './headless-login-slide.png'})
        #         flag = await mouse_slide(page=page)
        #         if flag:
        #             print(page.url)
        #             await page.keyboard.press('Enter')
        
        #             await get_cookie(page)
        # except:
        #     await page.keyboard.press('Enter')
        #     await page.waitFor(20)
        #     await page.waitForNavigation()
        #     try:
        #         global error
        #         error = await page.Jeval('.error', 'node => node.textContent')
        #     except Exception as e:
        #         error = None
        #         print(e, "错啦")
        #     finally:
        #         if error:
        #             print('确保账户安全重新入输入')
        #         else:
        #             print(page.url)
        #             # 可继续网页跳转 已经携带 cookie
        #             # await get_search(page)
        #             await get_cookie(page)

        # await page_close(browser)
    
    
    async def page_close(self,browser):
        for _page in await browser.pages():
            await _page.close()
        await browser.close()
    
    
    async def get_search(self,page):
        # https://s.taobao.com/search?q={查询的条件}&p4ppushleft=1%2C48&s={每页 44 条 第一页 0 第二页 44}&sort=sale-desc
        await page.goto("https://s.taobao.com/search?q=气球",{'timeout':0})
    
        await asyncio.sleep(5)
        # print(await page.content())
    
    
    # 获取登录后cookie  
    async def get_cookie(self,page):
        res = await page.content()
        cookies_list = await page.cookies()
        cookies = ''
        for cookie in cookies_list:
            str_cookie = '{0}={1};'
            str_cookie = str_cookie.format(cookie.get('name'), cookie.get('value'))
            cookies += str_cookie
        print(cookies,"get....cookies.............")

        # 将cookie 放入 cookie 池 以便多次请求 封账号 利用cookie 对搜索内容进行爬取
        # redisconn.lpush("tbcookiestr",json.dumps(cookies))
        redisconn.lpush("tbcookie",json.dumps(cookies_list))
        
        
        return True
    
    
if __name__ == '__main__':
    # username = input('TBusername: ')
    # pwd = input('PWD: ')
    url = "https://login.taobao.com/member/login.jhtml"
    _patch_pyppeteer()
    browser=Browser()
    with open('account.json','r',encoding='utf-8') as f:
        _obj=json.loads(f.read())
        print(_obj)
        for i in _obj['account']:
            print(i,type(i))
            username=i["user"]
            pwd=i["pwd"]
            loop = asyncio.get_event_loop()
            task = asyncio.ensure_future(browser.go_url(username,pwd,url))
            loop.run_until_complete(task)
            time.sleep(15)

 