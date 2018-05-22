# selenium模拟登录豆瓣
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from cap.YDMHTTPDemo import capytcha
import requests
import os,sys
from lxml import etree

brower = webdriver.Chrome()
brower.get('https://accounts.douban.com/login')
wait = WebDriverWait(brower,2)

def login():
    # 输入账号,密码
    input=wait.until(EC.presence_of_element_located((By.ID,'email')))
    input.clear()
    input.send_keys('username')
    wait.until(EC.presence_of_element_located((By.ID,'password'))).send_keys('password')

    # 获取验证码url
    captcha_url = brower.find_element_by_id('captcha_image').get_attribute('src')

    # 下载验证码
    response = requests.get(captcha_url)
    path = os.path.join(sys.path[0], 'cap\getimage.jpg')
    with open(path,'wb') as file:
         file.write(response.content)

    # 云打码识别
    result = capytcha(path)
    time.sleep(20)

    # 输入验证码
    brower.find_element_by_id('captcha_field').send_keys(result)

    time.sleep(3)
    # 点击登录
    wait.until(EC.presence_of_element_located((By.CLASS_NAME,'btn-submit'))).click()
    return brower.page_source

def main():
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

    # 验证是否登录成功
    url = 'https://www.douban.com/people/175097287/'
    session = requests.session()
    response  = session.get(url,cookies = cookies)
    selector= etree.HTML(response.text)
    title = selector.xpath('/html/head/title/text()')[0]
    print(title)


if __name__ == "__main__":
    main()
