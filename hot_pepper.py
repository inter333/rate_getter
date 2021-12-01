import requests
import bs4
import time
import re


def get_soup(link):
    ua = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_4) AppleWebKit/600.7.12 (KHTML"," like Gecko) Version/8.0.7 Safari/600.7.12'
    url = link
    resp = requests.get( url , headers = {"User-Agent": ua} )
    resp.encoding = resp.apparent_encoding
    soup = bs4.BeautifulSoup( resp.text, "html.parser" )
    return soup

def get_area_url(soup,area):
    links = [link.get('href') for link in soup.find_all('a') if link.text == area ]
    area_url = 'https://www.hotpepper.jp%s' % (links[0])
    return area_url

def get_content(soup):
    l = []
    shop_name = [n.get_text(strip=True) for n in soup.select('div.shopDetailTop h3.detailShopNameTitle')]
    shop_link = ['https://www.hotpepper.jp%s' % (n.get('href')) for n in soup.select('div.shopDetailTop h3.detailShopNameTitle a')]
    for shop,link in zip(shop_name,shop_link):
        time.sleep(2)
        shop_soup = get_soup(link)
        l.append(get_data(shop_soup,shop))
    return l

#遷移後で取得
def get_data(soup,shop):
    dic = {}
    c = soup.select('span.telNumber')
    call = c[0].text
    s = soup.select('div.topShopInfoWrap dd')
    s = s[1].select('span')
    site = ''.join(s[0].text.split())
    shop = ''.join(shop.split())
    dic.update(店名=shop, 住所=site, 電話番号=call)
    print(dic)
    return dic

def main(area):
    soup = get_soup("https://www.hotpepper.jp/yoyaku/SA11/")
    url = get_area_url(soup,area)
    data_list = []
    flg = 0
    while flg == 0:
        time.sleep(2)
        area_soup = get_soup(url)
        time.sleep(2)
        data_li = get_content(area_soup)
        data_list.append(data_li)
        print(data_list[-1])
        #終了判断
        s = area_soup.select('ul.pageLinkLinear.cFix.fl li')
        if len(s) == 2:
            flg = 1
        else:
            n = area_soup.select('ul.searchResultPageLink.cFix.fr li a')
            url =  'https://www.hotpepper.jp%s' % (n[1].get('href'))
    return data_list

if __name__ ==  '__main__':
    #クォーテーション内に検索したいエリアを入力してください！
    task_list = main("")