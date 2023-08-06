# coding : utf-8
import hashlib
import json
import requests
import random



def md5_encode(strings):
    m = hashlib.md5()
    m.update(strings.encode('utf-8'))
    return m.hexdigest()


class Translator:
    def __init__(self, key, pwd):
        self.apiKey = key
        self.pwd = pwd
        self.salt = str(random.randint(1024, 65535))

    def z2e(self, src):
        sign = md5_encode(self.apiKey + src + self.salt + self.pwd)
        src = src.replace(' ', '+')
        get_url = "http://api.fanyi.baidu.com/api/trans/vip/translate?q=" \
                  + src + "&from=zh&to=en&appid=" + self.apiKey + \
                  "&salt=" + self.salt + "&sign=" + sign
        try:
            req = requests.get(url=get_url)
            con = req.content.decode("utf-8")
            res = json.loads(con)['trans_result'][0]['dst']
            return res
        except Exception as e:
            return e
    

    def e2z(self, src):
        sign = md5_encode(self.apiKey + src + self.salt + self.pwd)
        src = src.replace(' ', '+')
        get_url = "http://api.fanyi.baidu.com/api/trans/vip/translate?q=" \
                  + src + "&from=en&to=zh&appid=" + self.apiKey + \
                  "&salt=" + self.salt + "&sign=" + sign
        try:
            req = requests.get(url=get_url)
            con = req.content.decode("utf-8")
            res = json.loads(con)['trans_result'][0]['dst']
            return res
        except Exception as e:
            return e
