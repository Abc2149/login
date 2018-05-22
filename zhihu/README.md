-----------模拟登录知乎--------
-处理知乎的倒立汉字验证码
请求知乎的地址:https://www.zhihu.com
分析：js、验证码、登录表单提交的数据

https://static.zhihu.com/heifetz/main.app.4bbf07772464fb28d4c5.js
{var n=Date.now(),r=new a.a("SHA-1","TEXT");return r.setHMACKey("d1b964811afb40118a12068ff74a12f4","TEXT"),r.update(e),r.update(u),r.update("com.zhihu.web"),r.update(String(n)),s({clientId:u,grantType:e,timestamp:n,source:"com.zhihu.web",signature:r.getHMAC("HEX")},t)}
字段signature
h = hmac.new(self.setHMACKey, None, sha1)  # 通过Hmac算法加密
h.update(self.grant_type.encode('utf-8'))  # 加密变量的顺序
h.update(self.client_id.encode('utf-8'))
h.update(self.source.encode('utf-8'))
h.update(str(int(time.time() * 1000)).encode('utf-8'))
signature = h.hexdigest()

https://static.zhihu.com/heifetz/main.app.4bbf07772464fb28d4c5.js
{headers:{"X-API-Version":"3.0.91","X-App-Za":"OS=Web",authorization:"oauth c3cef7c66a1843f8b3a9e6a1e3160e20"}}
字段client_id: oauth c3cef7c66a1843f8b3a9e6a1e3160e20 在未登录的情况下，爬取知乎的内容，一定要加此字段


验证码有三次请求分别是:get put post 同一个url地址
https://www.zhihu.com/api/v3/oauth/captcha?lang=en
lang = cn 为倒立汉字验证码，lang = en 为字母验证码，这里解决倒立汉字验证码的处理
第一次get
response:{show_captcha: False} 不需要验证码
response:{show_captcha: True} 需要验证码
response.cookies中携带put请求的验证码票据capsion_ticket

第二次put
# 提交put请求，需要在cookie中设置验证码票据
self.cookies['capsion_ticket'] = response.cookies['capsion_ticket']
# 验证码图片通过base64加密处理
img_base64":" base64码

第三次post
# 将图片保存到本地
# 获取所有汉字的坐标
{"img_size":[200,44],"input_points":[[.........]]
# 查看倒立汉字，输入序号
nums = str(input('输入序号从1开始,以空格为分隔符:')).split(' ')  # 以空格为分隔符
for num in nums:
    self.input_text.append(input_points[int(num) - 1])
# 验证是否输入正确

知乎破解汉字倒立验证码，登录成功