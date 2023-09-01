import re
import time
import requests
import pytesseract
from selenium import webdriver
singer = input('请输入歌手名称:')
phone_num = input('请输入手机号码:')
password = input('请输入密码:')
driver = webdriver.Chrome()
driver.get('https://music.facode.cn/index.php/Home/Index/login.html')
phone_tag = driver.find_element_by_name('phone')
phone_tag.send_keys(phone_num)
password_tag = driver.find_element_by_name('pass')
password_tag.send_keys(password)
img_tag = driver.find_element_by_id('graph_img')
png_path = 'E:\python\Python爬虫\爬取的信息\图片\验证码/code.png'
with open(png_path,'wb')as f:
    f.write(img_tag.screenshot_as_png)
code = pytesseract.image_to_string(png_path)
code = code.strip()
code_tag = driver.find_element_by_name('verify')
code_tag.send_keys(code)
login_tag = driver.find_element_by_class_name('login-btn')
login_tag.click()
cookies = ''
cookie_list = driver.get_cookies()
for cookie in cookie_list:
    cookies += '{}={};'.format(cookie['name'],cookie['value'])
header = {'Cookie':cookies}
time.sleep(3)
driver.quit()
search_url = 'https://music.facode.cn/index.php/Home/Index/search_list.html'
data = {
    'value':singer,
    'info':'1',
    'page':1
}
search_res = requests.post(search_url,data=data,headers=header)
search_json = search_res.json()
result_num = int(search_json['totalnum'])
page_num = result_num // 12
if result_num % 12 != 0:
    page_num += 1
for page in range(1,page_num):
    data['page'] = page
    print('开始爬取第{}页...'.format(page))
    search_res = requests.post(search_url,data=data,headers=header)
    search_json = search_res.json()
    for song in search_json['voice']:
        try:
            filename = '{}-{}'.format(song['name'],song['author'].replace('/',''))
        except:
            print('歌曲没有作者')
        else:
            lyrics_res = requests.post('https://music.facode.cn/index.php/Home/Index/lyrics.html',data={'id':song['id']},headers=header)
            lyrics_json = lyrics_res.json()
            if lyrics_json['data'] == None:
                print('暂无歌词')
                continue
            match_result = re.sub('\[.*?]','',lyrics_json['data'])
            with open('E:\python\Python爬虫\爬取的信息\Txt\林俊杰/'+filename+'.txt','w')as f:
                f.write(match_result)
            print('{}歌词的提取写入已完成...'.format(filename))