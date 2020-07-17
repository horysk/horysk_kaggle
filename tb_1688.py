import asyncio
import time
import json
from pyppeteer.launcher import launch
from alifunc import mouse_slide, input_time_random
from exe_js import js1, js3, js4, js5
import tkinter
from  ConfigDB import RedisDB
 
 
def screen_size():
    """使用tkinter获取屏幕大小"""
    tk = tkinter.Tk()
    width = tk.winfo_screenwidth()
    height = tk.winfo_screenheight()
    tk.quit()
    return width, height
 
 
async def main(username, pwd, url):
    browser = await launch({'headless': False, 'args': ['--no-sandbox'], }, userDataDir='./userdata',
                           args=[
                               '--window-size=1366,768',
                               '--disable-setuid-sandbox',
                                '--disable-gpu',
                                '--disable-infobars'
                               ])
    page = await browser.newPage()
    width, height = screen_size()
    await page.setViewport(viewport={"width": width, "height": height,"isMobile":True})
    await page.setUserAgent(
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36 Edge/16.16299')
 
    await page.goto(url)
    await page.evaluate(js1)
    await page.evaluate(js3)
    await page.evaluate(js4)
    await page.evaluate(js5)
    
    # pwd_login = await page.querySelector('.J_Quick2Static')
    # print(await (await pwd_login.getProperty('textContent')).jsonValue())
    # await pwd_login.click()
    # try:
    await page.type('#fm-login-id', username, {'delay': input_time_random() - 50})
    await page.type('#fm-login-password', pwd, {'delay': input_time_random()})
    # except:
    #     await page.type('#TPL_username_1', username, {'delay': input_time_random() - 50})
    #     await page.type('#TPL_password_1', pwd, {'delay': input_time_random()})
    await page.keyboard.press('Enter')
    time.sleep(3)
    await  page.goto('https://m.1688.com/page/ali.html')
    await page.screenshot({'path': './headless-test-result.png'})
    await get_cookie(page)
    time.sleep(2000)
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
 
 
async def page_close(browser):
    for _page in await browser.pages():
        await _page.close()
    await browser.close()
 
 
async def get_search(page):
    # https://s.taobao.com/search?q={查询的条件}&p4ppushleft=1%2C48&s={每页 44 条 第一页 0 第二页 44}&sort=sale-desc
    await page.goto("https://s.taobao.com/search?q=气球")
 
    await asyncio.sleep(5)
    # print(await page.content())
 
 
# 获取登录后cookie  
async def get_cookie(page):
    redisconn=RedisDB()
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
    redisconn.lpush("ali1688cookie",json.dumps(cookies_list))
    
    
    # return cookies
 
 
if __name__ == '__main__':
    username = input('TBusername: ')
    pwd = input('PWD: ')
    # url = "https://login.taobao.com/member/login.jhtml"
    url = "https://havanalogin.taobao.com/mini_login.htm?lang=zh_CN&appName=wap1688&appEntrance=h5&isMobile=true"
 
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main(username, pwd, url))
 