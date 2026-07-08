import csv
import requests
import time
from bs4 import BeautifulSoup
headers= {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/116.0",
    "Referer": "https://music.163.com/"
}
fieldnames = ['artist_name','artist_id','artist_pic','artist_intro','artist_url']
file = open('data/raw_data_all.csv','r',newline='',encoding='utf-8-sig')

reader = csv.DictReader(file)
cookies = {
 'MUSIC_U':"00601544845246694E79D934D042DF28DB6446648BA415623540229F4DAC161659C0AC8780B13BF4274D3E95621F0BD6D63167BAD2213D46D7A7DC5496F043787341AAAB1679952515C260A806A5C5385EB31EA82A666C9149976BC2C2C90F657FD2C9EB4D62744910A89D382F0955CD7A7B6F99694238714E2ED19524F3AEBCC9907D05474C907663416022A3876E2A19F46C431B3D87EE258A6FEC4A929245448E9239DA806E4B19230FF7748FC37900F71625304B8807C771B60997C640A4B7A68ACC19D935AAC4A088DB3BD29567C3EFCB6546A42C8FCF34F37911BA5948E6BAEF454053378CEFA4C88CA9977FE13C32DC12E295F7A9E773E3502A32842301B4CF4A73F42B540DEF202DC4F6BC6A7FA980130C2215F917493D931A78FC4D716124E0CB167BFB86DBA6753471B2BD051E37AEA2B81CA0A104A5277FB3FBBA19E4B938016D9638156F14B89683B3EF66A2608DE6F0962D51D4C67AC1E8A5A8457AA7A2B4121F0D34703A3B67286C2762AF547DBE9B8B3806726E6A59206CE33B0C5A9752F65D0F7827844E285337A7569BB3EB3D2FD18563098C54AEF2D92FB8E63B463CA675D84B826557602F095DC1"
}

f = open('data/artists.csv','w',newline='',encoding='utf-8-sig')
writer = csv.DictWriter(f,fieldnames=fieldnames)
writer.writeheader()

for song in reader:
    id=song['artist_id']
    url = f"https://music.163.com/artist?id={id}"
    response = requests.get(url=url,headers=headers,cookies=cookies)
    soup = BeautifulSoup(response.text,'lxml')
    title_var = soup.find('title').string.split('-')
    title = title_var[0]
    image = soup.find('meta',attrs={'property':'og:image'})
    if image:
        image_Url = image['content']
    else:
        image_Url =''
    intro = soup.find('meta',attrs={'name':'description'})
    if intro:
        introduction = intro['content']
    else:
        introduction='暂无简介'
    raw = [song['artist_name'],song['artist_id'],image_Url,introduction,url]
    row = dict(zip(fieldnames,raw))
    writer.writerow(row)
    time.sleep(0.5)
file.close()
f.close()