import pandas
import csv
import jieba.analyse
from collections import Counter
modal_words = [
    '啊', '哦', '喔', '嗯', '啦', '吧', '吗', '呢', '呀', '哇',
    '嘿', '哈', '呵', '唉', '哎', '噢', '哼', '唔', '咦', '呗',
    '咯', '哟', '喽', '嘛', '耶'
]
file = open("C:/Users/53125/Desktop/music_project/data/lyrics_data_通勤好状态.csv",'r',encoding='utf-8-sig')
reader = csv.DictReader(file)
avg_list=[]
word_of_modal = []
sum =0 
totol_lyrics = 0
for row in reader:
    lyric = row['lyrics']
    keywords = jieba.lcut(lyric)
    for word in keywords:
        totol_lyrics+=len(word)
        if word in modal_words:
            word_of_modal.append(word)
            sum+=1
word_counter = Counter(word_of_modal)
word_fre = [{word:count} for word,count in word_counter.items()]

print(word_fre)
print(sum/totol_lyrics)
file.close()