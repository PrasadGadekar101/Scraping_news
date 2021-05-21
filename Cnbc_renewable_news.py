# Scraping news posted under Energy category of CNBC new site

import requests
from bs4 import BeautifulSoup
from datetime import datetime

cnbc_url = "https://www.cnbc.com/energy/"

cnbs_raw_data = requests.get(cnbc_url)

cnbc_html_data = cnbs_raw_data.content

cnbc_raw_soup = BeautifulSoup(cnbc_html_data, 'html.parser')

# Grabing all the news presently displayed on the site under Energy category 

cnbc_news_content = cnbc_raw_soup.select(".Card-textContent")

print(len(cnbc_news_content))

news_list = []

# Collecting the news which are posted on the same day

for news in cnbc_news_content:
    cnbc_raw_datetime = news.select('.Card-time')[0].get_text()
    if 'ago' not in cnbc_raw_datetime:                        # Adding only the news which are posted on the site same day
        continue                                              # skiping for the older news
    news_dict = {}
    if 'an hour ago' in cnbc_raw_datetime:
        h_min_ago = 1
    else:
        h_min_ago = cnbc_raw_datetime.split(' ')[0]
    datetime_now = datetime.now()
    date_value = str((datetime_now.strftime("%d/%m/%Y")).replace('/', ''))
    time_value = (str(datetime.now()))[11:16].replace(':', '')
    timedate_value = str(time_value)+str(date_value)
    if 'min ago' in cnbc_raw_datetime:
        to_insert = ((int(timedate_value[0:2]))-1)
    else:
        to_insert = ((int(timedate_value[0:2]))-(int(h_min_ago)))
        if to_insert < 1:
            continue
    cnbc_title = news.find_all('div')[3].get_text()
    news_dict.update({"Title": cnbc_title})
    cbnc_link = news.find('a')['href']
    news_dict.update({"link": cbnc_link})
    sorter = str(to_insert) + timedate_value[2:]
    news_dict.update({"sorter": sorter})
    news_list.append(news_dict)  # to add logic for adding date and time

for i in news_list:
    print(i, end='\n\n')
