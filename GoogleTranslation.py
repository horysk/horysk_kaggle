# coding:utf-8

import json
import requests
import execjs
import sys

if sys.version_info[0] == 2:  # Python 2
    from urllib import quote
else:  # Python 3
    from urllib.parse import quote
import locale

locale.getdefaultlocale()[1]


class Py4Js():
    def __init__(self):
        self.ctx = execjs.compile(""" 
        function TL(a) { 
        var k = ""; 
        var b = 406644; 
        var b1 = 3293161072; 
        var jd = "."; 
        var $b = "+-a^+6"; 
        var Zb = "+-3^+b+-f"; 

        for (var e = [], f = 0, g = 0; g < a.length; g++) { 
            var m = a.charCodeAt(g); 
            128 > m ? e[f++] = m : (2048 > m ? e[f++] = m >> 6 | 192 : (55296 == (m & 64512) && g + 1 < a.length && 56320 == (a.charCodeAt(g + 1) & 64512) ? (m = 65536 + ((m & 1023) << 10) + (a.charCodeAt(++g) & 1023), 
            e[f++] = m >> 18 | 240, 
            e[f++] = m >> 12 & 63 | 128) : e[f++] = m >> 12 | 224, 
            e[f++] = m >> 6 & 63 | 128), 
            e[f++] = m & 63 | 128) 
        } 
        a = b; 
        for (f = 0; f < e.length; f++) a += e[f], 
        a = RL(a, $b); 
        a = RL(a, Zb); 
        a ^= b1 || 0; 
        0 > a && (a = (a & 2147483647) + 2147483648); 
        a %= 1E6; 
        return a.toString() + jd + (a ^ b) 
    }; 

    function RL(a, b) { 
        var t = "a"; 
        var Yb = "+"; 
        for (var c = 0; c < b.length - 2; c += 3) { 
            var d = b.charAt(c + 2), 
            d = d >= t ? d.charCodeAt(0) - 87 : Number(d), 
            d = b.charAt(c + 1) == Yb ? a >>> d: a << d; 
            a = b.charAt(c) == Yb ? a + d & 4294967295 : a ^ d 
        } 
        return a 
    } 
    """)

    def getTk(self, text):
        return self.ctx.call("TL", text)


def split_string(str, cutting_method):
    item = str.split(cutting_method)
    interception_len = len(item) / 2
    interception1 = ".".join(item[:interception_len])
    interception2 = ".".join(item[interception_len:len(item)])
    return interception1, interception2


def get_string(str, cutting_method):
    list = []
    interception1, interception2 = split_string(str, cutting_method)
    if len(interception1) > 5000:
        list1 = get_string(interception1, cutting_method)
        list = list + list1
    else:
        list.append(interception1)
    if len(interception2) > 5000:
        list1 = get_string(interception2, cutting_method)
        list = list + list1
    else:
        list.append(interception2)
    return list



# ~~~~~~~~~~~~~~~~~~~~~~~~~~~华丽的分割线~~~~~~~~~~~~~~~~~~~~~~~~~~~

def translate(content):
    try:
        if len(content) == 0:
            texts = ''
            return texts
        js = Py4Js()
        tk = js.getTk(content)
        content = quote(content)
        url = "https://translate.google.cn/translate_a/single?client=t&sl=auto&tl=en&hl=zh-CN&dt=at&dt=bd&dt=ex&dt=ld&dt=md&dt=qca&dt=rw&dt=rm&dt=ss&dt=t&ie=UTF-8&oe=UTF-8&ssel=3&tsel=0&kc=0&tk=%s&q=%s" % (tk, content)
        response = requests.get(url)
        result = response.content
        item = json.loads(result)
        texts = ""
        for i in range(0, len(item[0])):
            if str(item[0][i][0]) != "None":
                texts += str(item[0][i][0])
        return texts
    except:
        return ""


# 自动检测语言后翻译成英文
def get_translate(context):
    str = "你好"
    if len(context) > 5000:
        list = get_string(context, ".")
        count = 0
        for item in list:
            count += 1
            if count != len(list):
                item = item + "."
            str += translate(item)
    else:
        str = translate(context)
    return str

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~华丽的分割线~~~~~~~~~~~~~~~~~~~~~~~~~~~

# 将英文翻译成中文
def zh(content):
    texts = ""
    try:
        if len(content) == 0:
            return texts
        js = Py4Js()
        tk = js.getTk(content)
        content = quote(content)
        url = "https://translate.google.cn/translate_a/single?client=t&sl=en&tl=zh-CN&hl=zh-CN&dt=at&dt=bd&dt=ex&dt=ld&dt=md&dt=qca&dt=rw&dt=rm&dt=ss&dt=t&ie=UTF-8&oe=UTF-8&pc=1&otf=1&ssel=0&tsel=0&kc=1&tk=%s&q=%s" % (tk, content)  # 英语-->汉语
        #url = "https://translate.google.cn/translate_a/single?client=t&sl=en&tl=ja&hl=zh-CN&dt=at&dt=bd&dt=ex&dt=ld&dt=md&dt=qca&dt=rw&dt=rm&dt=ss&dt=t&ie=UTF-8&oe=UTF-8&ssel=6&tsel=3&kc=0&tk=%s&q=%s" % (tk, content)      # 英语-->日语
        # url = "https://translate.google.cn/translate_a/single?client=t&sl=auto&tl=de&hl=zh-CN&dt=at&dt=bd&dt=ex&dt=ld&dt=md&dt=qca&dt=rw&dt=rm&dt=ss&dt=t&ie=UTF-8&oe=UTF-8&ssel=3&tsel=3&kc=0&tk=%s&q=%s" % (tk, content)   # 英语-->德语
        # url = "https://translate.google.cn/translate_a/single?client=t&sl=auto&tl=fr&hl=zh-CN&dt=at&dt=bd&dt=ex&dt=ld&dt=md&dt=qca&dt=rw&dt=rm&dt=ss&dt=t&ie=UTF-8&oe=UTF-8&source=btn&ssel=3&tsel=4&kc=0&tk=%s&q=%s" % (tk, content)  # 英语-->西班牙语
        # url = "https://translate.google.cn/translate_a/single?client=t&sl=auto&tl=fr&hl=zh-CN&dt=at&dt=bd&dt=ex&dt=ld&dt=md&dt=qca&dt=rw&dt=rm&dt=ss&dt=t&ie=UTF-8&oe=UTF-8&source=btn&ssel=3&tsel=4&kc=0&tk=%s&q=%s" % (tk, content)    # 英语-->法文
        # url = "https://translate.google.cn/translate_a/single?client=t&sl=auto&tl=it&hl=zh-CN&dt=at&dt=bd&dt=ex&dt=ld&dt=md&dt=qca&dt=rw&dt=rm&dt=ss&dt=t&ie=UTF-8&oe=UTF-8&source=btn&ssel=3&tsel=4&kc=0&tk=%s&q=%s" % (tk, content)    # 英语-->意大利语
        
        response = requests.get(url)
        result = response.content
        item = json.loads(result)

        for i in range(0, len(item[0])):
            if str(item[0][i][0]) != "None":
                texts += str(item[0][i][0])
        return texts
    except:
        return ""


# 英文翻译中文
def get_zh(context):
    str = "hello"
    if len(context) > 5000:
        list = get_string(context, ".")
        count = 0
        for item in list:
            count += 1
            if count != len(list):
                item = item + "."
            str += zh(item)
    else:
        str = zh(context)
    return str


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~华丽的分割线~~~~~~~~~~~~~~~~~~~~~~~~~~~


def getAPIUrl(Country):
    apiUrl = ""
    if Country == 'JP':    # 日本
        apiUrl = "https://translate.google.cn/translate_a/single?client=t&sl=en&tl=ja&hl=zh-CN&dt=at&dt=bd&dt=ex&dt=ld&dt=md&dt=qca&dt=rw&dt=rm&dt=ss&dt=t&ie=UTF-8&oe=UTF-8&ssel=6&tsel=3&kc=0"

    elif Country == 'DE':  # 德国
        apiUrl = "https://translate.google.cn/translate_a/single?client=t&sl=auto&tl=de&hl=zh-CN&dt=at&dt=bd&dt=ex&dt=ld&dt=md&dt=qca&dt=rw&dt=rm&dt=ss&dt=t&ie=UTF-8&oe=UTF-8&ssel=3&tsel=3&kc=0"

    elif Country == 'ES':  # 西班牙
        apiUrl = "https://translate.google.cn/translate_a/single?client=t&sl=auto&tl=it&hl=zh-CN&dt=at&dt=bd&dt=ex&dt=ld&dt=md&dt=qca&dt=rw&dt=rm&dt=ss&dt=t&ie=UTF-8&oe=UTF-8&source=btn&ssel=3&tsel=4&kc=0"

    elif Country == 'FR':  # 法国
        apiUrl = "https://translate.google.cn/translate_a/single?client=t&sl=auto&tl=fr&hl=zh-CN&dt=at&dt=bd&dt=ex&dt=ld&dt=md&dt=qca&dt=rw&dt=rm&dt=ss&dt=t&ie=UTF-8&oe=UTF-8&source=btn&ssel=3&tsel=4&kc=0"

    elif Country == 'IT':  # 意大利
        apiUrl = "https://translate.google.cn/translate_a/single?client=t&sl=auto&tl=it&hl=zh-CN&dt=at&dt=bd&dt=ex&dt=ld&dt=md&dt=qca&dt=rw&dt=rm&dt=ss&dt=t&ie=UTF-8&oe=UTF-8&source=btn&ssel=3&tsel=4&kc=0"

    return apiUrl


# 将英文翻译成各国语言
def TranslateOtherLanguagesInEnglish(content, Country):
    texts = ""
    try:
        if len(content) == 0:
            return texts
        js = Py4Js()
        tk = js.getTk(content)
        content = quote(content)

        apiUrl = str(getAPIUrl(Country)) + "&tk=%s&q=%s" % (tk, content)    # 获取翻译语种的接口
        # apiUrl = "https://translate.google.cn/translate_a/single?client=t&sl=en&tl=ja&hl=zh-CN&dt=at&dt=bd&dt=ex&dt=ld&dt=md&dt=qca&dt=rw&dt=rm&dt=ss&dt=t&ie=UTF-8&oe=UTF-8&ssel=6&tsel=3&kc=0&tk=%s&q=%s" % (tk, content)

        response = requests.get(apiUrl)
        result = response.content
        item = json.loads(result)

        for i in range(0, len(item[0])):
            if str(item[0][i][0]) != "None":
                texts += str(item[0][i][0])
        return texts
    except:
        return ""


# 英文翻译各国语言
def get_world(context, Country):
    str = ""
    if len(context) > 5000:
        list = get_string(context, ".")
        count = 0
        for item in list:
            count += 1
            if count != len(list):
                item = item + "."
            str += TranslateOtherLanguagesInEnglish(item, Country)
    else:
        str = TranslateOtherLanguagesInEnglish(context, Country)
    return str


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~华丽的分割线~~~~~~~~~~~~~~~~~~~~~~~~~~~


if __name__ == '__main__':
    # result0 = get_zh("Hello world!")
    result1 = get_world("Hello world!", "JP")
    result2 = get_world("Hello world!", "DE")
    result3 = get_world("Hello world!", "ES")
    result4 = get_world("Hello world!", "FR")
    result5 = get_world("Hello world!", "IT")

    print(result1)
    print(result2)
    print(result3)
    print(result4)
    print(result5)





'''
url = "https://translate.google.cn/translate_a/single?client=t&sl=en&tl=zh-CN&hl=zh-CN&dt=at&dt=bd&dt=ex&dt=ld&dt=md&dt=qca&dt=rw&dt=rm&dt=ss&dt=t&ie=UTF-8&oe=UTF-8&pc=1&otf=1&ssel=0&tsel=0&kc=1&tk=%s&q=%s" % (tk, content)      # 英语-->汉语
url = "https://translate.google.cn/translate_a/single?client=t&sl=en&tl=ja&hl=zh-CN&dt=at&dt=bd&dt=ex&dt=ld&dt=md&dt=qca&dt=rw&dt=rm&dt=ss&dt=t&ie=UTF-8&oe=UTF-8&ssel=6&tsel=3&kc=0&tk=%s&q=%s" % (tk, content)                    # 英语-->日语
url = "https://translate.google.cn/translate_a/single?client=t&sl=auto&tl=de&hl=zh-CN&dt=at&dt=bd&dt=ex&dt=ld&dt=md&dt=qca&dt=rw&dt=rm&dt=ss&dt=t&ie=UTF-8&oe=UTF-8&ssel=3&tsel=3&kc=0&tk=%s&q=%s" % (tk, content)                  # 英语-->德语
url = "https://translate.google.cn/translate_a/single?client=t&sl=auto&tl=it&hl=zh-CN&dt=at&dt=bd&dt=ex&dt=ld&dt=md&dt=qca&dt=rw&dt=rm&dt=ss&dt=t&ie=UTF-8&oe=UTF-8&source=btn&ssel=3&tsel=4&kc=0&kc=0&tk=%s&q=%s" % (tk, content)  # 英语-->西班牙语
url = "https://translate.google.cn/translate_a/single?client=t&sl=auto&tl=fr&hl=zh-CN&dt=at&dt=bd&dt=ex&dt=ld&dt=md&dt=qca&dt=rw&dt=rm&dt=ss&dt=t&ie=UTF-8&oe=UTF-8&source=btn&ssel=3&tsel=4&kc=0&tk=%s&q=%s" % (tk, content)       # 英语-->法文
url = "https://translate.google.cn/translate_a/single?client=t&sl=auto&tl=it&hl=zh-CN&dt=at&dt=bd&dt=ex&dt=ld&dt=md&dt=qca&dt=rw&dt=rm&dt=ss&dt=t&ie=UTF-8&oe=UTF-8&source=btn&ssel=3&tsel=4&kc=0&tk=%s&q=%s" % (tk, content)       # 英语-->意大利语
'''