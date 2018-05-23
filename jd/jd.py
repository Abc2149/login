import requests
from lxml import etree
import json
import time


class Jd(object):

    def __init__(self,usernmae,password):
        self.username = usernmae
        self.password = password
        self.session = requests.session()
        self.headers = {
            'Host': 'passport.jd.com',
            'Pragma': 'no-cache',
            'Referer': 'https://passport.jd.com/uc/login?ltype=logout',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.146 Safari/537.36',
        }

    def get_data(self):
        url = 'https://passport.jd.com/uc/login?ltype=logout'
        response = self.session.get(url,headers = self.headers)
        # print(response.text)
        selector = etree.HTML(response.text)
        sa_token = selector.xpath('//*[@id="sa_token"]/@value')[0]
        uuid = selector.xpath('//*[@id="uuid"]/@value')[0]
        eid = selector.xpath('//*[@id="eid"]/@value')[0]
        fp = selector.xpath('//*[@id="sessionId"]/@value')[0]
        _t = selector.xpath('//*[@id="token"]/@value')[0]
        pubkey = selector.xpath('//*[@id="pubKey"]/@value')[0]

        self.headers['Host'] = 'authcode.jd.com'    # 验证码的头部
        # 判断是否需要输入验证码
        cap_url ='https://authcode.jd.com/verify/image?a=1&acid={acid}&uid={uid}&yys={yys}'
        cap_url = cap_url.format(acid=uuid,uid=uuid,yys=str(int(time.time()*1000)))
        image = self.session.get(cap_url,headers=self.headers)
        with open('image.jpg','wb') as f:
            f.write(image.content)
        authcode = input('请输入验证码:')

        data = {
            'uuid':uuid,
            'eid':eid,
            'fp':fp,
            '_t':_t,
            'loginType':'c',
            'loginname':self.username,
            'nloginpwd':self.password,
            'authcode':authcode,
            'pubKey':pubkey,
            'sa_token':sa_token,
        }
        return data,uuid

    def login(self):
        formdata,uuid = self.get_data()
        # 登录头部
        self.headers['Host'] ='passport.jd.com'
        self.headers['Origin'] = 'https://passport.jd.com'

        url = 'https://passport.jd.com/uc/loginService?uuid={uuid}&ltype={ltype}&r={r}&version=2015'.format(uuid=uuid,ltype='logout',r=0.386014980619763)
        response = self.session.post(url,data=formdata,headers=self.headers)
        print(response.text)

if __name__ == '__main__':
    jb = Jd('username','password')
    jb.login()










