---------------------  weibo模拟登录  ---------------
tools:chrome fiddler 
url:https://weibo.com/
输入账号，密码，验证码登录一遍，fiddler抓包工具分析有三个重要的url地址。

https://login.sina.com.cn/sso/prelogin.php
该url地址，get服务器返回的json格式的数据，servertime,nonce，publickey

https://login.sina.com.cn/sso/login.php
观察post表单中的内容，如su,sp等信息，可以判断这就是登录请求，构建自己的表单信息，发送请求即可。

https://i.sso.sina.com.cn/js/ssologin.js
查看js源码，su为username,sp为possword,并相应的进行了加密处理。

重定向正在登录
https://passport.weibo.com/wbsso/login

get，post的关键字：su,sp,servertime,nonce,pubkey,ticket...


username=sinaSSOEncoder.base64.encode(urlencode(username))
RSAKey.setPublic(me.rsaPubkey,"10001");password=RSAKey.encrypt([me.servertime,me.nonce].join("\t")+"\n"+password)

su用base64解码
import base64
print(base64.b64decode('YmFubWFraiU0MDEyNi5jb20='))
输出结果为：b'banmakj%40126.com'            


sp用rsa进行加密
import rsa
import binascii
string = (str(servertime) + "\t" + str(nonce) + "\n" + str(password)).encode("utf-8")
public_key = rsa.PublicKey(int(pubkey,16),int('10001',16))
ps_encrypt = rsa.encrypt(string,public_key)
password = binascii.b2a_hex(ps_encrypt)








