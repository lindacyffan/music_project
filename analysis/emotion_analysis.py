import csv
from snownlp import SnowNLP
file = open("C:/Users/53125/Desktop/music_project/data/lyrics_data_00后歌单.csv",'r',encoding='utf-8-sig')

reader = csv.DictReader(file)
scores = []
for row in reader:
    lyric = row['lyrics']
    if not lyric or len(lyric)<10:
        scores.append(0.5)
    else:
        score = SnowNLP(lyric).sentiments
        scores.append(score)
avg = sum(scores)/len(scores)
print (avg)
file.close()