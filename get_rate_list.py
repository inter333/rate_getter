import bs4
import requests
import time

def get_soup(link):
    ua = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_4) AppleWebKit/600.7.12 (KHTML"," like Gecko) Version/8.0.7 Safari/600.7.12'
    url = link
    resp = requests.get( url , headers = {"User-Agent": ua} )  # WEBリクエスト
    resp.encoding = resp.apparent_encoding                            # 文字化け防止に文字コード指定
    soup = bs4.BeautifulSoup( resp.text, "html.parser" )              # 結果をsoupに格納
    return soup

def get_page_count(soup):
    page = soup.select('div.pageing ul.pagination li')
    page_count = int(page[-2].text)
    return page_count

def define_link(link,page_count):
    link = link+ "?page=" + str(page_count)
    return link

def get_content(soup):
    div = soup.select('div.smash-row.mb-20')
    content = div[0].select('span.rate_text')
    return content

def rate_calculation(rate_list,rate,content):
    content = reversed(content)
    for i in content:
        if "＋" in i.text:
            rate += int(i.text.replace("＋",""))
            rate_list.append(rate)
        elif "－" in i.text:
            rate -= int(i.text.replace("－",""))
            rate_list.append(rate)
        else:
            pass
    return rate_list,rate


def main(link):
    rate_list = []
    rate = 1500
    soup = get_soup(link)
    time.sleep(3)
    page_count = get_page_count(soup)
    print("レート取得中")
    while  page_count  != 1:
        new_link = define_link(link,page_count)
        new_soup = get_soup(new_link)
        content = get_content(new_soup)
        rate_list,rate = rate_calculation(rate_list,rate,content)
        page_count -= 1

    content = get_content(soup)
    rate_list,rate = rate_calculation(rate_list,rate,content)
    print("レート取得完了")
    for rate in rate_list:
        print(rate)


    return rate_list,rate

if __name__ ==  '__main__':
    #このダブルクォーテーションの中に調べたいプレイヤーのマイページのurlを貼り付けてください！
    task_list = main("")