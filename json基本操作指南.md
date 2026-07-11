# json格式

## 1. 读取
```bash
with open('comments.json', 'r', encoding='utf-8') as f:
    all_comments = json.load(f)
```
## 2.修改（比如添加一条评论）
```bash
song_id = '1973665667'
if song_id not in all_comments:
    all_comments[song_id] = []

all_comments[song_id].append({
    'text': '这首歌真好听！',
    'time': '2026-07-06 10:30:00'
})
```
## 3.写回
```bash
with open('comments.json','w',encoding = 'utf-8') as f:
json.dump(all_comments,f,ensure_ascii=False,indent=2)
```