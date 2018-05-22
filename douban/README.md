---------------------  selenium模拟登录豆瓣  ---------------
# 输入账号,密码
wait.until(EC.presence_of_element_located((By.ID,'email'))).send_keys('username')
wait.until(EC.presence_of_element_located((By.ID,'password'))).send_keys('password')

# 获取验证码url
captcha_url = brower.find_element_by_id('captcha_image').get_attribute('src')

# 云打码识别
result = capytcha(path)
time.sleep(20)

html = login()
selector = etree.HTML(html)
error = selector.xpath('//*[@id="item-error"]/p/text()')[0]
if error == '验证码不正确':
    login()

# 获得cookies
cookites_list = brower.get_cookies()
cookies = dict()
for item in cookites_list:
    cookies[item['name']]=item['value']
