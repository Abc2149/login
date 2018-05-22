import requests
import hmac
from hashlib import sha1
import time
import json
import base64


class ZhihuLogin(object):
    def __init__(self):
        # Hamc算法加密用的字段,提交登录的表单中取得
        self.client_id = 'c3cef7c66a1843f8b3a9e6a1e3160e20'
        self.grant_type = 'password'
        self.source = 'com.zhihu.web'
        # js源码中取得key
        self.setHMACKey = b'd1b964811afb40118a12068ff74a12f4'
        # 验证码地址
        self.url = 'https://www.zhihu.com/api/v3/oauth/captcha?lang=cn'
        # 倒立汉字的坐标点
        self.input_text = []
        self.cookies = {}
        self.session = requests.session()
        self.headers = {
            'Connection': 'keep-alive',
            'Host': 'www.zhihu.com',
            'Referer': 'https://www.zhihu.com/signup\?next=%2F',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.146 Safari/537.36',
            'authorization': 'oauth c3cef7c66a1843f8b3a9e6a1e3160e20',
        }

    def get_signature(self):
        h = hmac.new(self.setHMACKey, None, sha1)  # 通过Hmac算法加密
        h.update(self.grant_type.encode('utf-8'))  # 加密变量的顺序
        h.update(self.client_id.encode('utf-8'))
        h.update(self.source.encode('utf-8'))
        h.update(str(int(time.time() * 1000)).encode('utf-8'))
        signature = h.hexdigest()
        # print(signature)
        return signature

    def get_captcha_image(self):
        # lang = cn 为倒立汉字验证码，lang = en 为字母验证码，这里解决倒立汉字验证码的处理

        # 验证码有三次请求分别是:get put post
        response = self.session.get(self.url, headers=self.headers)
        show_captcha = json.loads(response.text)
        if show_captcha:
            # 提交put请求，需要在cookie中设置验证码票据
            self.cookies['capsion_ticket'] = response.cookies['capsion_ticket']
            # 携带cookies,发送put请求
            response = self.session.put(self.url, headers=self.headers, cookies=self.cookies)
            # 验证码图片通过base64加密处理
            img = json.loads(response.text)['img_base64'].encode('utf-8')  # str to bytes
            # 解码，保存本地目录
            image = base64.b64decode(img)
            with open('captcha.jpg', 'wb') as f:
                f.write(image)
            return True
        else:
            return False

    def deal_captcha(self):
        try:
            if self.get_captcha_image():
                # 点击汉字，获得坐标点
                input_points = [[18.5, 24.1875],[45.5, 23.1875],[65.5, 23.1875],[88.5, 25.1875],
                                [112.5, 24.1875],[135.5, 24.1875],[158.5, 24.1875],]

                # 输入倒立汉字的顺序
                nums = str(input('输入序号从1开始,以空格为分隔符:')).split(' ')  # 以空格为分隔符
                for num in nums:
                    self.input_text.append(input_points[int(num) - 1])
                # 发送坐标信息
                input_text = {
                    "img_size": [200, 44],
                    "input_points": self.input_text,
                    }
                formdata = {
                    'input_text':json.dumps(input_text)
                    }
                response = self.session.post(self.url, headers=self.headers, data=formdata)
                success = json.loads(response.text)['success']
                print(response.text)
                return True
        except:
            print('ERR_SESSION_NEED_CAPTCHA')
            return False

    def login(self, username, password):
        try:
            # 验证码提交验证成功
            if self.get_captcha():
                captcha = {
                    "img_size": [200, 44],
                    "input_points": self.input_text,
                }
                formdata = {
                    'client_id': self.client_id,
                    'grant_type': self.grant_type,
                    'timestamp': int(time.time() * 1000),
                    'source': self.source,
                    'signature': self.get_signature(),
                    'username': username,
                    'password': password,
                    'captcha': json.dumps(captcha),
                    'lang': 'cn',
                    'ref_source': 'homepage',
                    'utm_source': '',
                }
                url = 'https://www.zhihu.com/api/v3/oauth/sign_in'
                response = self.session.post(url, headers=self.headers, data=formdata)
                cookie = json.loads(response.text)["cookie"]
                print(cookie)
        except:
            print('client_logion_failed')


if __name__ == '__main__':
    zhihu = ZhihuLogin()
    zhihu.login('+86phone number', 'password')
















