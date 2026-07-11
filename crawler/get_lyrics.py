import csv
import requests
import re
import time

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/116.0",
    "Referer": "https://music.163.com/"
}
file = open('data/raw_data_治愈系下午茶.csv','r',newline='',encoding='utf-8-sig')
reader = csv.DictReader(file)
fieldnames = ['name', 'id','artist_id', 'artist_name', 'album_picUrl', 'music_Url', 'source','lyrics']
f = open('data/lyrics_data_治愈系下午茶.csv','w',newline='',encoding='utf-8-sig') # 治愈系下午茶只是一个例子，可以换成其他歌单名字
writer = csv.DictWriter(f,fieldnames= fieldnames)
writer.writeheader()

for row in reader:
    id = row['id']
    url = f"https://music.163.com/api/song/lyric?id={id}&lv=1&kv=1&tv=-1"
    response = requests.get(url=url,headers=headers,cookies=None)
    data = response.json()
    temp = data['lrc']['lyric']
    pattern = r'\[\d{2}:\d{2}.\d{2,3}\]'
    clean_lyric = re.sub(pattern,"",temp)
    pattern2 = r'.*[:：].*'
    clean_lyric = re.sub(pattern2,"",clean_lyric)
    lines = clean_lyric.split('\n')
    new_clean_lyric= ""
    for line in lines:
        if line.strip(): # 判断空行，看看去除首尾空格后是否还有其他内容
            new_clean_lyric+=line
            new_clean_lyric+='\n'
    new_row = dict(row)
    
    new_row['lyrics'] = new_clean_lyric.strip('\n') #末尾会多一个换行符
    writer.writerow(new_row)
    time.sleep(0.5)

file.close()
f.close()

# 我的代码里有两种读写csv的方式，第一种是直接读写，格式为write(row)，那么row在这里是列表，第二种是Dictwriter，以字典的形式写进去，需要使用fieldnames