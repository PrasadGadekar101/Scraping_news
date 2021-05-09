# scraping news posted same day after 12:00:00am/00:00:00

import requests
from bs4 import BeautifulSoup
from datetime import datetime

url = 'https://economictimes.indiatimes.com/industry/energy/power' 

raw_data = requests.get(url)

html_content = raw_data.content

# 2. html parser
raw_soup = BeautifulSoup(html_content,'html.parser')

# 3. html tree traverser

raw_news_content = raw_soup.select('.eachStory')    # Each "eachStory" class contain all the stories present on that page.

raw_news_list = []

# Collecting the raw data for each story/news

for news in raw_news_content:
    dictionary_news = {}
    for_title = news.find_all("meta")
    if len(for_title)>1:
        title = for_title[1].get('content')
    else:
        raw_title = news.find_all('img')
        title = raw_title[0].get('alt')
    dictionary_news.update({'Title':title})
    raw_link = news.find("a")["href"]
    link = "https://economictimes.indiatimes.com" + raw_link
    dictionary_news.update({'Link':link})
    desc = news.find("p").get_text()
    dictionary_news.update({'Desciption':desc})
    raw_date_time =( news.find("time").get_text()).split(',')
    date_time_str = ' '.join(raw_date_time)
    dictionary_news.update({'date_time':date_time_str})
    raw_news_list.append(dictionary_news)


# print(raw_news_content[0].prettify)

def con_to_num(month_news):											# Converting the month from word to number
	if month_news=='Jan':
		return 1
	if month_news=='Feb':
		return 2
	if month_news=='Mar':
		return 3
	if month_news=='Apr':
		return 4
	if month_news=='May':
		return 5
	if month_news=='Jun':
		return 6
	if month_news=='Jul':
		return 7
	if month_news=='Aug':
		return 8
	if month_news=='Sep':
		return 9
	if month_news=='Oct':
		return 10
	if month_news=='Nov':
		return 11
	if month_news=='Dec':
		return 12

def remove_unwanted_return_date_time(date_time):
	month = con_to_num(date_time[0])
	if len(str(month))==1:
		date_value = str(date_time[1])+str('0')+str(month)+str(date_time[3]) # the month and date are suffuled so it will become easy to 
	else:
		date_value = str(date_time[1])+str(month)+str(date_time[3])
	for element in date_time:												# Converting the 12hrs timing to the 24 hrs timing
		if ':' in element:
			if date_time[-2]=='AM':
				if (element[:2])=='12':
					time = str('00'+ element[2:])  # convert to 24 hours clock
				else:
					time = element
			else:
				if element[:2]=='12':
					time = element
				else:
					time = str(int(element[:2])+12) + element[2:] 
	time_value = str(time.replace(':',''))
	return (date_value,time_value)


list_news_sort = []

for news in raw_news_list:															# Main loop through the list of the news short from eachstory class with the 'sortTitle_link_date_dis' fun
	date_time_news = (news['date_time']).split(' ')								# Converting the news date to integer to sort on the basis of date time
	Date_Value, Time_Value = remove_unwanted_return_date_time(date_time_news)  	# Calling the function to remove the unwanted char in the time
	today = datetime.today()													# Taking the time and date of current day
	date_required_formate = str((today.strftime("%d/%m/%Y")).replace('/',''))
	time_required = (str(datetime.now()))[11:16]								# grabbing current time
	if (int(date_required_formate)-int(Date_Value)) ==1000000 and int(Time_Value)>900:    # filter to get news which are 1 day older and only which are after 9 am 
		list_news_sort.append(news)
	if (int(date_required_formate)-int(Date_Value)) == 0:
		list_news_sort.append(news)


# After cleaning and grabing the needed details of the stories/news "list_news_sort" is the list that stores all the stories/news
for story in list_news_sort:
    print(story,end="\n\n")

# Next processes to connect to db and uploading it is done but not included in this....