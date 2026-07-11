import pandas as pd
import json
from datetime import datetime

df = pd.read_csv("C:/Users/53125/Desktop/music_project/data/comments.csv")
data = df.to_dict('records')
dic ={}
for item in data:
    if item['id'] not in dic:
        dic[item['id']]=[]
    time = int(item['time'])
    datetime_time = datetime.fromtimestamp(time/1000).strftime('%Y-%m-%d %H:%M:%S')
    dic[item['id']].append({'id':time,
                                 '内容':item['comments_content'],
                                '时间': datetime_time,
                                'likes':item['comments_likedCount']})
    
file = open("C:/Users/53125/Desktop/music_project/mysite/comments.json",'w',encoding='utf-8-sig')
json.dump(dic,file,ensure_ascii=False,indent=2)
file.close()

