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

from flask import Flask, request, render_template, send_from_directory, jsonify


app = Flask(__name__)




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
    # if Country == 'JP':    # 英语-->日本
    #     apiUrl = "https://translate.google.cn/translate_a/single?client=t&sl=auto&tl=ja&hl=zh-CN&dt=at&dt=bd&dt=ex&dt=ld&dt=md&dt=qca&dt=rw&dt=rm&dt=ss&dt=t&ie=UTF-8&oe=UTF-8&ssel=6&tsel=3&kc=0"
    #
    # elif Country == 'DE':  # 英语-->德国
    #     apiUrl = "https://translate.google.cn/translate_a/single?client=t&sl=auto&tl=de&hl=zh-CN&dt=at&dt=bd&dt=ex&dt=ld&dt=md&dt=qca&dt=rw&dt=rm&dt=ss&dt=t&ie=UTF-8&oe=UTF-8&ssel=3&tsel=3&kc=0"
    #
    # elif Country == 'ES':  # 英语-->西班牙
    #     apiUrl = "https://translate.google.cn/translate_a/single?client=t&sl=auto&tl=it&hl=zh-CN&dt=at&dt=bd&dt=ex&dt=ld&dt=md&dt=qca&dt=rw&dt=rm&dt=ss&dt=t&ie=UTF-8&oe=UTF-8&source=btn&ssel=3&tsel=4&kc=0"
    #
    # elif Country == 'FR':  # 英语-->法国
    #     apiUrl = "https://translate.google.cn/translate_a/single?client=t&sl=auto&tl=fr&hl=zh-CN&dt=at&dt=bd&dt=ex&dt=ld&dt=md&dt=qca&dt=rw&dt=rm&dt=ss&dt=t&ie=UTF-8&oe=UTF-8&source=btn&ssel=3&tsel=4&kc=0"
    #
    # elif Country == 'IT':  # 英语-->意大利
    #     apiUrl = "https://translate.google.cn/translate_a/single?client=t&sl=auto&tl=it&hl=zh-CN&dt=at&dt=bd&dt=ex&dt=ld&dt=md&dt=qca&dt=rw&dt=rm&dt=ss&dt=t&ie=UTF-8&oe=UTF-8&source=btn&ssel=3&tsel=4&kc=0"
    #
    if Country in ["DE", "ES", "FR", "IT", "JP", "IN", "UK", "CN"]:

        ApiUrlDict = {
            # 德语
            "DE":"https://translate.google.cn/translate_a/single?client=t&sl=auto&tl=de&hl=zh-CN&dt=at&dt=bd&dt=ex&dt=ld&dt=md&dt=qca&dt=rw&dt=rm&dt=ss&dt=t&ie=UTF-8&oe=UTF-8&ssel=3&tsel=3&kc=0",

            # 西班牙语
            "ES":"https://translate.google.cn/translate_a/single?client=t&sl=auto&tl=it&hl=zh-CN&dt=at&dt=bd&dt=ex&dt=ld&dt=md&dt=qca&dt=rw&dt=rm&dt=ss&dt=t&ie=UTF-8&oe=UTF-8&source=btn&ssel=3&tsel=4&kc=0",

            # 法语
            "FR":"https://translate.google.cn/translate_a/single?client=t&sl=auto&tl=fr&hl=zh-CN&dt=at&dt=bd&dt=ex&dt=ld&dt=md&dt=qca&dt=rw&dt=rm&dt=ss&dt=t&ie=UTF-8&oe=UTF-8&source=btn&ssel=3&tsel=4&kc=0",

            # 意大利语
            "IT":"https://translate.google.cn/translate_a/single?client=t&sl=auto&tl=it&hl=zh-CN&dt=at&dt=bd&dt=ex&dt=ld&dt=md&dt=qca&dt=rw&dt=rm&dt=ss&dt=t&ie=UTF-8&oe=UTF-8&source=btn&ssel=3&tsel=4&kc=0",

            # 日语
            "JP":"https://translate.google.cn/translate_a/single?client=t&sl=auto&tl=ja&hl=zh-CN&dt=at&dt=bd&dt=ex&dt=ld&dt=md&dt=qca&dt=rw&dt=rm&dt=ss&dt=t&ie=UTF-8&oe=UTF-8&ssel=6&tsel=3&kc=0",

            # 印度语
            "IN":"https://translate.google.cn/translate_a/single?client=t&sl=auto&tl=hi&hl=zh-CN&dt=at&dt=bd&dt=ex&dt=ld&dt=md&dt=qca&dt=rw&dt=rm&dt=ss&dt=t&ie=UTF-8&oe=UTF-8&ssel=0&tsel=4&kc=0",

            # 英语
            "UK":"https://translate.google.cn/translate_a/single?client=t&sl=auto&tl=en&hl=zh-CN&dt=at&dt=bd&dt=ex&dt=ld&dt=md&dt=qca&dt=rw&dt=rm&dt=ss&dt=t&ie=UTF-8&oe=UTF-8&ssel=0&tsel=4&kc=0",

            # 中国话
            "CN":"https://translate.google.cn/translate_a/single?client=t&sl=auto&tl=zh-CN&hl=zh-CN&dt=at&dt=bd&dt=ex&dt=ld&dt=md&dt=qca&dt=rw&dt=rm&dt=ss&dt=t&ie=UTF-8&oe=UTF-8&ssel=0&tsel=4&kc=0"
        }

        return ApiUrlDict[Country]
    else:
        print('翻译的语种不存在')
        return None


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



@app.route("/GoogleTranslation", methods=["POST"])
def google_translation():
    # result0 = get_zh("Hello world!")

    requestJson = request.get_json()
    TranslationContent = requestJson["Content"]

    TargetLanguage = requestJson["TargetLanguage"]


    # TranslationContentData = {
    #     "productEnName": get_world(TranslationContent["productEnName"], TargetLanguage),
    #     "seoTitle": get_world(TranslationContent["seoTitle"], TargetLanguage),
    #     "seoKeywords": get_world(TranslationContent["seoKeywords"], TargetLanguage),
    #     "searchKeywords": get_world(TranslationContent["searchKeywords"], TargetLanguage),
    #     "seoDescr": get_world(TranslationContent["seoDescr"], TargetLanguage),
    #     "productDescr": get_world(TranslationContent["productDescr"], TargetLanguage),
    #     "featureList": get_world(TranslationContent["featureList"], TargetLanguage),
    #     "packingList": get_world(TranslationContent["packingList"], TargetLanguage)
    # }

    for k, v in TranslationContent.items():
        print(k, v)

    # print(TranslationContentData)


    # CountryList = ["DE", "ES", "FR", "IT", "JP", "IN", "UK", "CN"]
    # for Country in CountryList:
    #
    #     UK = get_world("こんにちは世界！", Country)
    #     print(Country, "+++++", UK)



    return jsonify({"Req":"ok"})
    # return jsonify({"Req":TranslationContentData})

if __name__ == '__main__':
    app.run(debug=True, threaded=True, host='0.0.0.0', port=6006)





'''

"Code": 0,
"德语": "Hallo Welt!",
"意大利语": "Ciao mondo!",
"日语:": "こんにちは世界！",
"法语": "Bonjour le monde!",
"西班牙语": "Ciao mondo!"

DE +++++ Hallo Welt!
ES +++++ Ciao mondo!
FR +++++ Bonjour le monde!
IT +++++ Ciao mondo!
JP +++++ こんにちは世界！
IN +++++ नमस्ते दुनिया!
UK +++++ Hello world!
CN +++++ 你好，世界！


url = "https://translate.google.cn/translate_a/single?client=t&sl=en&tl=zh-CN&hl=zh-CN&dt=at&dt=bd&dt=ex&dt=ld&dt=md&dt=qca&dt=rw&dt=rm&dt=ss&dt=t&ie=UTF-8&oe=UTF-8&pc=1&otf=1&ssel=0&tsel=0&kc=1&tk=%s&q=%s" % (tk, content)      # 英语-->汉语
url = "https://translate.google.cn/translate_a/single?client=t&sl=en&tl=ja&hl=zh-CN&dt=at&dt=bd&dt=ex&dt=ld&dt=md&dt=qca&dt=rw&dt=rm&dt=ss&dt=t&ie=UTF-8&oe=UTF-8&ssel=6&tsel=3&kc=0&tk=%s&q=%s" % (tk, content)                    # 英语-->日语
url = "https://translate.google.cn/translate_a/single?client=t&sl=auto&tl=de&hl=zh-CN&dt=at&dt=bd&dt=ex&dt=ld&dt=md&dt=qca&dt=rw&dt=rm&dt=ss&dt=t&ie=UTF-8&oe=UTF-8&ssel=3&tsel=3&kc=0&tk=%s&q=%s" % (tk, content)                  # 英语-->德语
url = "https://translate.google.cn/translate_a/single?client=t&sl=auto&tl=it&hl=zh-CN&dt=at&dt=bd&dt=ex&dt=ld&dt=md&dt=qca&dt=rw&dt=rm&dt=ss&dt=t&ie=UTF-8&oe=UTF-8&source=btn&ssel=3&tsel=4&kc=0&kc=0&tk=%s&q=%s" % (tk, content)  # 英语-->西班牙语
url = "https://translate.google.cn/translate_a/single?client=t&sl=auto&tl=fr&hl=zh-CN&dt=at&dt=bd&dt=ex&dt=ld&dt=md&dt=qca&dt=rw&dt=rm&dt=ss&dt=t&ie=UTF-8&oe=UTF-8&source=btn&ssel=3&tsel=4&kc=0&tk=%s&q=%s" % (tk, content)       # 英语-->法文
url = "https://translate.google.cn/translate_a/single?client=t&sl=auto&tl=it&hl=zh-CN&dt=at&dt=bd&dt=ex&dt=ld&dt=md&dt=qca&dt=rw&dt=rm&dt=ss&dt=t&ie=UTF-8&oe=UTF-8&source=btn&ssel=3&tsel=4&kc=0&tk=%s&q=%s" % (tk, content)       # 英语-->意大利语
'''

'''
18 - 8 - 27
https://translate.google.cn/translate_a/single?client=t&sl=auto&tl=it&hl=zh-CN&dt=at&dt=bd&dt=ex&dt=ld&dt=md&dt=qca&dt=rw&dt=rm&dt=ss&dt=t&ie=UTF-8&oe=UTF-8&otf=1&ssel=0&tsel=0&kc=2&tk=638777.999116&q=%E4%BD%A0%E5%A5%BD
https://translate.google.cn/translate_a/single?client=t&sl=auto&tl=it&hl=zh-CN&dt=at&dt=bd&dt=ex&dt=ld&dt=md&dt=qca&dt=rw&dt=rm&dt=ss&dt=t&ie=UTF-8&oe=UTF-8&otf=1&ssel=0&tsel=0&kc=1&tk=967808.542069&q=hello






# 中文-->日文
https://translate.google.cn/translate_a/single?client=t&sl=auto&tl=ja&hl=zh-CN&dt=at&dt=bd&dt=ex&dt=ld&dt=md&dt=qca&dt=rw&dt=rm&dt=ss&dt=t&ie=UTF-8&oe=UTF-8&source=btn&ssel=0&tsel=0&kc=0&tk=767641.865470&q=%E4%BD%A0%E5%A5%BD%EF%BC%8C%E4%B8%96%E7%95%8C%EF%BC%81
https://translate.google.cn/translate_a/single?client=t&sl=en  &tl=ja&hl=zh-CN&dt=at&dt=bd&dt=ex&dt=ld&dt=md&dt=qca&dt=rw&dt=rm&dt=ss&dt=t&ie=UTF-8&oe=UTF-8&ssel=6&tsel=3&kc=0
# 中文-->德文
https://translate.google.cn/translate_a/single?client=t&sl=auto&tl=de&hl=zh-CN&dt=at&dt=bd&dt=ex&dt=ld&dt=md&dt=qca&dt=rw&dt=rm&dt=ss&dt=t&ie=UTF-8&oe=UTF-8&ssel=0&tsel=4&kc=0&tk=767641.865470&q=%E4%BD%A0%E5%A5%BD%EF%BC%8C%E4%B8%96%E7%95%8C%EF%BC%81
# 中文-->西班牙
https://translate.google.cn/translate_a/single?client=t&sl=auto&tl=es&hl=zh-CN&dt=at&dt=bd&dt=ex&dt=ld&dt=md&dt=qca&dt=rw&dt=rm&dt=ss&dt=t&ie=UTF-8&oe=UTF-8&ssel=0&tsel=4&kc=0&tk=767641.865470&q=%E4%BD%A0%E5%A5%BD%EF%BC%8C%E4%B8%96%E7%95%8C%EF%BC%81
# 中文-->法文
https://translate.google.cn/translate_a/single?client=t&sl=auto&tl=fr&hl=zh-CN&dt=at&dt=bd&dt=ex&dt=ld&dt=md&dt=qca&dt=rw&dt=rm&dt=ss&dt=t&ie=UTF-8&oe=UTF-8&ssel=0&tsel=4&kc=0&tk=767641.865470&q=%E4%BD%A0%E5%A5%BD%EF%BC%8C%E4%B8%96%E7%95%8C%EF%BC%81
# 中文-->意大利
https://translate.google.cn/translate_a/single?client=t&sl=auto&tl=it&hl=zh-CN&dt=at&dt=bd&dt=ex&dt=ld&dt=md&dt=qca&dt=rw&dt=rm&dt=ss&dt=t&ie=UTF-8&oe=UTF-8&ssel=0&tsel=4&kc=0&tk=767641.865470&q=%E4%BD%A0%E5%A5%BD%EF%BC%8C%E4%B8%96%E7%95%8C%EF%BC%81


# 中文-->印度
https://translate.google.cn/translate_a/single?client=t&sl=auto&tl=hi&hl=zh-CN&dt=at&dt=bd&dt=ex&dt=ld&dt=md&dt=qca&dt=rw&dt=rm&dt=ss&dt=t&ie=UTF-8&oe=UTF-8&ssel=0&tsel=4&kc=0&tk=767641.865470&q=%E4%BD%A0%E5%A5%BD%EF%BC%8C%E4%B8%96%E7%95%8C%EF%BC%81

https://translate.google.cn/translate_a/single?client=t&sl=auto&tl=de&hl=zh-CN&dt=at&dt=bd&dt=ex&dt=ld&dt=md&dt=qca&dt=rw&dt=rm&dt=ss&dt=t&ie=UTF-8&oe=UTF-8           &ssel=3&tsel=3&kc=0"
https://translate.google.cn/translate_a/single?client=t&sl=auto&tl=hi&hl=zh-CN&dt=at&dt=bd&dt=ex&dt=ld&dt=md&dt=qca&dt=rw&dt=rm&dt=ss&dt=t&ie=UTF-8&oe=UTF-8&ssel=0&tsel=4&kc=0
https://translate.google.cn/translate_a/single?client=t&sl=auto&tl=en&hl=zh-CN&dt=at&dt=bd&dt=ex&dt=ld&dt=md&dt=qca&dt=rw&dt=rm&dt=ss&dt=t&ie=UTF-8&oe=UTF-8&ssel=0&tsel=4&kc=0
https://translate.google.cn/translate_a/single?client=t&sl=auto&tl=zh-CN&hl=zh-CN&dt=at&dt=bd&dt=ex&dt=ld&dt=md&dt=qca&dt=rw&dt=rm&dt=ss&dt=t&ie=UTF-8&oe=UTF-8&ssel=0&tsel=4&kc=0
https://translate.google.cn/translate_a/single?client=t&sl=auto&tl=it&hl=zh-CN&dt=at&dt=bd&dt=ex&dt=ld&dt=md&dt=qca&dt=rw&dt=rm&dt=ss&dt=t&ie=UTF-8&oe=UTF-8&source=btn&ssel=3&tsel=4&kc=0

# 中文-->英文
https://translate.google.cn/translate_a/single?client=t&sl=auto&tl=en&hl=zh-CN&dt=at&dt=bd&dt=ex&dt=ld&dt=md&dt=qca&dt=rw&dt=rm&dt=ss&dt=t&ie=UTF-8&oe=UTF-8&ssel=0&tsel=4&kc=0&tk=767641.865470&q=%E4%BD%A0%E5%A5%BD%EF%BC%8C%E4%B8%96%E7%95%8C%EF%BC%81
'''