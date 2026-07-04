import requests
import csv

playlist_map = {
    "3778678": "热歌榜",
    "3779629": "新歌榜",
    "19723756": "飙升榜",
    "2884035":"原创榜",
    "71385702": "ACG榜",
    "71384707": "古典榜",
    "13372522766": "潮流风向榜",
    "2768609272":"清晨听古典",
    "17666320375":"下班放轻松",
    "8643604201":"晴天自习室",
    "13335483641": "Lofti工作歌单",
    "17539371762": "治愈系下午茶",
    "8851077202":"跑步听华语",
    "8640538202":"旅行听华语",
    "17615719403":"通勤好状态",
    "9158431202":"00后歌单",
    "8159674692":"全球流行趋势",
    "13688797642":"70后歌单",
    "17535769386":"80后歌单",
    "7810805656":"影视原声",
    "8835188200":"欧美热播",
    # 你可以继续添加更多榜单
}
cookies = {
 "os": "pc"
}
playlist_id = "8835188200"
url = f"https://music.163.com/api/playlist/detail?id={playlist_id}"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/116.0",
    "Referer": "https://music.163.com/"
}

response = requests.get(url=url,headers=headers,cookies=cookies)



data = response.json()
playlist_name = playlist_map.get(playlist_id, playlist_id)
filename = f'data/raw_data_{playlist_name}.csv'
file = open(f'{filename}','w',newline='',encoding='utf-8-sig')

writer = csv.writer(file)
writer.writerow(['name', 'id', 'artist_id','artist_name', 'album_picUrl', 'music_Url'])
tracks = data['result']['tracks']
for song in tracks:
    name=song['name']
    id=song['id']
    artist_id = song['artists'][0]['id']
    artist_name=song['artists'][0]['name']
    album_picUrl=song['album']['picUrl']
    music_Url=f"https://music.163.com/#/song?id={id}"

    row = [name,id,artist_id,artist_name,album_picUrl,music_Url]
    writer.writerow(row)

file.close()

