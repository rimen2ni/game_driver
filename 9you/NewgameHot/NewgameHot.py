import requests
import time
import smtplib
from email.mime.text import MIMEText
from selenium import webdriver
from lxml import etree


url = 'http://www.9game.cn/xyrb/'
headers = {
    'Host': 'www.9game.cn',
    'Connection': 'keep-alive',
    'Cache-Control': 'max-age=0',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.16 Safari/537.36',
    'Referer': 'http://www.9game.cn/',
}


def driver():
    re = requests.get(url, headers=headers, verify=False)
    etr = etree.HTML(re.text)
    tables = etr.xpath('//div[@class="box-text"]/table/tr')
    return tables


def parse_hot(tables):#解析排名
    new_game = {}
    file = open('9youHot.txt', 'w', encoding='utf-8')
    for table in tables:
        ranking = table.xpath('./td[1]//text()')  # 排名
        game_name = table.xpath('./td[2]//text()')  # 游戏名称
        game_type = table.xpath('./td[3]//text()')  # 游戏类型
        open_state = table.xpath('./td[4]//text()')  # 开档状态
        game_hot = table.xpath('./td[5]//text()')  # 游戏热度
        if len(ranking) != 0:  # 排名
            new_game['ranking'] = ranking[0]
        if len(game_name) != 0:  # 游戏名称
            new_game['game_name'] = game_name[1]
        if len(game_type) != 0:  # 游戏类型
            new_game['game_type'] = game_type[0]
        if len(game_hot) != 0:  # 游戏热度
            new_game['game_hot'] = game_hot[0]
        print(new_game)
        if len(ranking) != 0 and len(game_hot) != 0 and len(game_type) != 0 and len(game_hot) != 0:
            file.write('ranking：%s,game_name：%s,game_type：%s,game_hot：%s' % (
                ranking[0], game_name[1], game_type[0], game_hot[0] + '\n'))

def parse_url(tables):#解析排名游戏的详情url
    url_list = []
    for link in tables:
        url = link.xpath('./td[2]//a/@href')
        if len(url) != 0:
            new_urls = 'http://www.9game.cn' + url[0]
            url_list.append(new_urls)
    print(url_list)
    return url_list

def parse_connect(url_list):
    driver = webdriver.Firefox()
    file1 = open('9you1Connect.txt', 'w', encoding='utf-8')
    for new_url in url_list:
        driver.get(new_url)
        # re = requests.get(new_url,headers=headers)
        time.sleep(2)

        for i in range(3):#点击加载更多评论
            time.sleep(2)
            driver.find_element_by_link_text('点击查看更多加载').click()
            # driver.find_element_by_xpath('//div[@id="page_reload"]/a').click()
        etr = etree.HTML(driver.page_source)
        li_list = etr.xpath('//ul[@id="comment_list"]//li')
        game_talk = []
        name = etr.xpath('//div[@class="title"]/h1/a/text()')  # 游戏名
        if len(name) != 0:
             name = name[0]
        else:
            name = etr.xpath('//a[@class="name"]/text()')[0]

        for li in li_list:
            game_user = li.xpath('./div[2]/p[1]/span[1]/text()')[0]  # 用户
            game_time = li.xpath('./div[2]/p[1]/span[2]/text()')[0]  # 评论时间
            game_connect = li.xpath('./div[2]/p[2]/text()')[0]  # 评论
            file1.write('name：{}||game_user：{}||game_time：{},\n,game_connect：{}'.format(name, game_user, game_time,
                                                                                            game_connect) + '\n\n')
    time.sleep(10)
    driver.close()

def emil():
    mimetxt = MIMEText('爬虫结束')
    mimetxt['subject'] = '爬虫结束'
    mimetxt['from'] = 'rimen_luo@163.com'
    mimetxt['to'] = 'rimen_luo@163.com'

    myemil = smtplib.SMTP('stmp.163.com',25)
    myemil.login(user='rimen_luo',password='xxxxxxx')
    myemil.sendmail('rimen_luo@163.com','rimen_luo@163.com',mimetxt.as_string())
    myemil.close()

if __name__ == '__main__':
    parse_hot(driver())  # 解析排名数据
    url_list = parse_url(driver())  # 解析url返回new_url
    parse_connect(url_list)
    # emil()