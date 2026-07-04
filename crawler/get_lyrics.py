import csv
import requests
import re
import time
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/116.0",
    "Referer": "https://music.163.com/"
}

fieldnames = ['name', 'id','artist_id', 'artist_name', 'album_picUrl', 'music_Url', 'source','lyrics']

file = open('data/raw_data_all.csv','r',newline='',encoding='utf-8-sig')

reader = csv.DictReader(file)

f = open('data/lyrics_data_all9.csv','w',newline='',encoding='utf-8-sig')

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
        if line.strip():
            new_clean_lyric+=line
            new_clean_lyric+='\n'
    new_row = dict(row)
    
    new_row['lyrics'] = new_clean_lyric.strip('\n')
    writer.writerow(new_row)
    time.sleep(0.5)

file.close()
f.close()

