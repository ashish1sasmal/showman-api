from bs4 import BeautifulSoup
import requests
import json
from datetime import datetime
from .models import *
# Create your views here.

def fetch_soup(url):
    headers = { 'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:72.0) Gecko/20100101 Firefox/72.0' }
    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.content, 'html.parser')
    return soup

def city_events(city):
    soup = fetch_soup("https://in.bookmyshow.com/explore/home/"+city)
    events = soup.find_all(class_="commonStyles__FullWidgetWrapper-sc-1k17atf-4 hOGemf")
    # print(len(e))
    events_list = []
    for i in range(len(events)):
        ev = events[i].find_all(class_="commonStyles__LinkWrapper-sc-1k17atf-11 style__CardContainer-sc-10gjjdh-3 cnsxMV")
        for j in ev:
            genre = None
            try:
                 genre = j.find(class_="style__StyledText-tgsgks-0 kJJQxJ").text
            except:
                 genre = j.find(class_="style__StyledText-tgsgks-0 dJlJfB").text
            d = {
                "id":j['href'].split("/")[-1],
                "city":city,
                "title":j.find(class_="style__StyledText-tgsgks-0 cTkfzX").text,
                "url":j['href'],
                "img_url":j.img['src'],
                "genre":genre
                }
            # e = Events.objects.get_or_create(e_id=d["id"],title=d["title"],e_url=d["url"],img_url=d["img_url"],genre=d["genre"])[0]
            # #print(Cities.objects.get(c_name=city).id)
            # e.city.add(Cities.objects.get(c_name=city).id,)
            events_list.append(d)
            # print(d)
    with open(f'Citywise-data/{city}.json','w') as outfile:
        json.dump({f"{city}":events_list},outfile)






def all_cities():
    file = open('cities.txt','r')
    r = file
    soup = BeautifulSoup(r, 'html.parser')
    r = soup.find_all(class_="sc-gVyKpa joBuHk")
    cities = []
    for i in r:
        cities.append(i.text.replace(" ","-").replace("(","").replace(")","").lower())
    file.close()
    with open('cities.json','w') as outfile:
        json.dump(cities,outfile)
