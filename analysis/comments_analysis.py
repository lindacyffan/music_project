import csv
file = open("C:/Users/53125/Desktop/music_project/data/comments.csv",'r',encoding='utf-8-sig')

reader = csv.DictReader(file)


comments = []
for row in reader:
    comments.append({
        'content': row['comments_content'],
        'liked_count': int(row['comments_likedCount']),
        'song_id': row['id'],
    })

comments_sorted = sorted(comments, key=lambda x:x['liked_count'],reverse=True)
top_10 = comments_sorted[:10]
for i, c in enumerate(top_10):
    print(f"{i}. 点赞数：{c['liked_count']}")
    print(f"   歌曲ID：{c['song_id']}")
    print(f"   评论：{c['content']}")
file.close()