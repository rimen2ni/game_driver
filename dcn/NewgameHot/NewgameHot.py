import requests
import time
import smtplib
from email.mime.text import MIMEText
from selenium import webdriver
from lxml import etree


url = 'http://ng.d.cn/channel/ranklist.html'
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
    return re.text


def parse_taday(link):#解析排名
    etr = etree.HTML(link)
    tables = etr.xpath('//ul[@id="con_rank_1"]//li') #排名
    print(tables)
    new_game = {}
    file = open('dcn_taday.txt', 'w', encoding='utf-8')
    for table in tables:
        ranking = table.xpath('./div[1]/em/text()')
        game_name = table.xpath('./div[1]/a/text()')
        game_type = table.xpath('./div[1]/span/text()')
        print(ranking,game_name,game_type)

        if len(ranking) != 0 and len(game_name) != 0 and len(game_type) != 0:
            file.write('ranking：%s,game_name：%s,game_type：%s' % (
                ranking[0], game_name[0], game_type[0] + '\n'))

def parse_week(link):
    etr = etree.HTML(link)
    tables = etr.xpath('//ul[@id="con_rank_2"]//li')  # 排名
    print(tables)
    new_game = {}
    file = open('dcn_week.txt', 'w', encoding='utf-8')
    for table in tables:
        ranking = table.xpath('./div[1]/em/text()')
        game_name = table.xpath('./div[1]/a/text()')
        game_type = table.xpath('./div[1]/span/text()')
        print(ranking, game_name, game_type)

        if len(ranking) != 0 and len(game_name) != 0 and len(game_type) != 0:
            file.write('ranking：%s,game_name：%s,game_type：%s' % (
                ranking[0], game_name[0], game_type[0] + '\n'))


def parse_expect(link):
    etr = etree.HTML(link)
    tables = etr.xpath('//div[@id="wrap"]/div[3]/ul//li')  # 排名

    file = open('dcn_expect.txt', 'w', encoding='utf-8')
    for table in tables:
        ranking = table.xpath('./div[1]/em/text()')
        game_name = table.xpath('./div[1]/a/text()')
        game_type = table.xpath('./div[1]/span/text()')
        print(ranking, game_name, game_type)

        if len(ranking) != 0 and len(game_name) != 0 and len(game_type) != 0:
            file.write('ranking：%s,game_name：%s,game_type：%s' % (
                ranking[0], game_name[0], game_type[0] + '\n'))

if __name__ == '__main__':
    parse_taday(driver())
    parse_week(driver())
    parse_expect(driver())