import urllib.parse
import base64
import time
import requests
import json
import re
import rsa
import binascii


class WeiBoLogin(object):
    def __init__(self):
        # 同一个session实列中发出的请求之间保存cookies
        self.session = requests.session()
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.146 Safari/537.36',
        }
        self.session.headers.update(self.headers)
        self.su = None
        self.sp = None
        self.servertime = None
        self.nonce = None

    # 登录
    def login(self, username, password):

        self.username = username
        self.password = password

        self.su = self.get_username()
        self.data = self.get_params()
        self.sp = self.get_password()

        post_data = {
            'entry': 'account',
            'gateway': '1',
            'from': 'null',
            'savestate': '30',
            'useticket': '0',
            'vsnf': '1',
            'su': self.su,
            'service': 'account',
            'servertime': self.servertime,
            'nonce': self.nonce,
            'pwencode': 'rsa2',
            'rsakv': self.data['rsakv'],
            'sp': self.sp,
            'sr': '1366*768',
            'encoding': 'UTF-8',
            'cdult': '3',
            'domain': 'sina.com.cn',
            'prelt': '177',
            'returntype': 'TEXT',
        }

        url = 'https://login.sina.com.cn/sso/login.php?client=ssologin.js(v1.4.19)'
        response = self.session.post(url, data=post_data)
        data_1 = json.loads(response.text)
        # 重定向 正在登录...
        ticket = re.match('.*?=(.*?)&.*?', data_1["crossDomainUrlList"][0]).group(1)
        if data_1["retcode"] == '0':
            params = {
                'ticket': urllib.parse.unquote(ticket),
                'ssosavestate': int(time.time()),
                'callback': 'sinaSSOController.doCrossDomainCallBack',
                'scriptId': 'ssoscript0',
                'client': 'ssologin.js(v1.4.19)',
                '_': int(time.time() * 1000),
            }
            response = self.session.get('https://passport.weibo.com/wbsso/login', params=params)
            data_2 = json.loads(re.search('.*?\((.*?)\)', response.text).group(1))
            if data_2['result'] == True:
                user_uniqueid = data_2['userinfo']['uniqueid']
                user_displayname = data_2['userinfo']['displayname']
                print('login weibo success:%s'% user_displayname)
            else:
                print('login weibo failed:%s', data_2)
        else:
            print('login weibo failed:%s', data_1)

    # base64加密用户名
    def get_username(self):
        # 将字符串转化为url编码
        username_quote = urllib.parse.quote(self.username)
        username = base64.b64encode(username_quote.encode('utf-8'))
        # 将bytes对象转为str
        return username.decode('utf-8')

    # 获取服务器返回的nonce,servertime,pubkey等信息
    def get_params(self):
        params = {
            'entry': 'account',
            'callback': 'sinaSSOController.preloginCallBack',
            'su': self.su,
            'rsakt': 'mod',
            'client': 'ssologin.js(v1.4.15)',
            '_': int(time.time() * 1000),
        }
        try:
            response = self.session.get('https://login.sina.com.cn/sso/prelogin.php', params=params)
            data = json.loads(re.search('.*?\((.*?)\)', response.text).group(1))
            return data
        except Exception as e:
            print(e.code)
            return None

    # rsa加密密码
    def get_password(self):
        self.servertime = self.data['servertime']
        self.nonce = self.data['nonce']
        self.pubkey = self.data['pubkey']
        string = (str(self.servertime) + "\t" + str(self.nonce) + "\n" + self.password).encode("utf-8")
        public_key = rsa.PublicKey(int(self.pubkey, 16), int('10001', 16))
        ps_encrypt = rsa.encrypt(string, public_key)
        self.password = binascii.b2a_hex(ps_encrypt)
        return self.password.decode('utf-8')


if __name__ == '__main__':
    weibo = WeiBoLogin()
    weibo.login('username','password')
























