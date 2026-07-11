import csv
import requests
import time,os
from bs4 import BeautifulSoup

headers= {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/116.0",
    "Referer": "https://music.163.com/"
}

file = open('data/raw_data_all.csv','r',newline='',encoding='utf-8-sig')
reader = csv.DictReader(file)
cookies = {
 'MUSIC_U':"00A6EF088DC28923F322E529ED1C22906E0E60881F005CF7B2CA5BCAC5A0CE8FFEF7100171EA777D1447129E7B593DE3B0A52F34757FEF6A3B9E055CAA1F13E9164664C8C5FBA14A3F839480CE2FB5A63435D0F846ABDD5CA28485DE711B67C6D5A41E2427023216C7810D0E43E4362D614E857F9056580F2F877DD2B0E7E16ED79C92AD4F3293D294676E7326654FCD78AD4AB4E81B11DB090672CF88D040E6253BC465110C09A81851E601D988D825DF8FB9C9A34439CCB29CD07F3D942524D23D03E7747606EBD4161BBDEFB30550A15D91C200681480ADD17BB2F79C555D68762F530454577F7E7284465DB070FB667B0E80AE2D4B24F0C41BD6A816C366ACFCB368B96F514E63303BE7BEE175A5A430A89F970C4152CF03BB1B6AFC38BC6D78C461AE2761C1A6B378A8EEA5E3693A4037960F55AB59DBED3F7FEB7038A04F17352D7B49CA82FAE8A3845A9B91F9771745A52122978F42AB2081FBA460F62669FB0C0FEAE4BD78BEBFBCCBD4FA270AF49F14BDA4FCD683B561C84DC548E81895B7A5B061E7927868F1DE91307E4148E69E3E0F91F0298E95951C5A3E9CC376129EC4812644CA746AEDEB39AD6317A6"
} # 必须要登录的cookies呜呜呜

f = open('data/artists.csv','w',newline='',encoding='utf-8-sig')
fieldnames = ['artist_name','artist_id','artist_pic','artist_intro','artist_url']
writer = csv.DictWriter(f,fieldnames=fieldnames)
writer.writeheader()

for song in reader:
    id = song['artist_id']
    url = f"https://music.163.com/artist?id={id}"
    response = requests.get(url=url,headers=headers,cookies=cookies)
    soup = BeautifulSoup(response.text,'lxml')
    title_var = soup.find('title').string.split('-')
    title = title_var[0]
    image = soup.find('meta',attrs={'property':'og:image'}) # <meta property="og:image">
    if image:
        image_Url = image['content']
    else:
        image_Url =''
    intro_url = f"https://music.163.com/api/artist/introduction?id={id}"
    # 由于api访问不能过于频繁，所以采取双保险策略。有限从api获取数据资料，不行再用soup去抓取网页html的标签
    # 没有直接解析html标签是因为<meta attrs={'name': 'description'}>信息不全，完整信息由js动态加载
    # 1. 优先从 API 取完整简介
    try:
        res = requests.get(intro_url, headers=headers, cookies=cookies, timeout=10)
        data = res.json() # 有别于之前的那个response
        if data.get('code') == 200:
            intro_parts = []
            for item in data.get('introduction', []):
                ti = item.get('ti', '')
                txt = item.get('txt', '')
                intro_parts.append(f"{ti}：{txt}")
            introduction = '\n\n'.join(intro_parts) if intro_parts else data.get('briefDesc', '') # 拼接成字符串并用特定字符连接
            if introduction:
                # API 取到了，直接用
                pass
            else:
                # API 没取到，降级到 meta
                raise Exception("API 返回空")
        else:
            raise Exception("API 返回非 200")
    # 2. 备选：从 meta 标签取摘要
    except:
        soup = BeautifulSoup(response.text, 'html.parser')
        meta_intro = soup.find('meta', attrs={'name': 'description'})
        introduction = meta_intro.get('content', '暂无简介') if meta_intro else '暂无简介'
        
    raw = [song['artist_name'],song['artist_id'],image_Url,introduction,url]
    row = dict(zip(fieldnames,raw))
    writer.writerow(row)
    time.sleep(1)

file.close()
f.close()