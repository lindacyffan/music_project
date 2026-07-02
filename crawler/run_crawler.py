import requests
from bs4 import BeautifulSoup
import csv

url = "https://music.163.com/api/playlist/detail?id=3778678"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/116.0",
    "Referer": "https://music.163.com/"
}

response = requests.get(url=url,headers=headers,cookies=None)


soup = BeautifulSoup(response.text, 'lxml')

data = response.json()

file = open('data/raw_data.csv','a',newline='',encoding='utf-8-sig')

writer = csv.writer(file)

tracks = data['result']['tracks']
for song in tracks:
    name=song['name']
    id=song['id']
    artist_name=song['artists'][0]['name']
    album_picUrl=song['album']['picUrl']
    music_Url=f"https://music.163.com/#/song?id={id}"

    row = [name,id,artist_name,album_picUrl,music_Url]
    writer.writerow(row)

file.close()

