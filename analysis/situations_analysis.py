import pandas
import csv

file = open("C:/Users/53125/Desktop/music_project/data/lyrics_data_跑步听华语.csv",'r',encoding='utf-8-sig')
reader = csv.DictReader(file)
avg_list=[]
for row in reader:
    sentence_list =[]
    lyric = row['lyrics']
    if lyric:
        sentence_list = lyric.split('\n')
        if '' in sentence_list:
            sentence_list.remove('')
        for i in range(len(sentence_list)):
            sentence_list[i]=len(sentence_list[i])
        avg = sum(sentence_list)/len(sentence_list)
        if avg:
            avg_list.append(avg)

    
all_avg = sum(avg_list)/len(avg_list)
print(all_avg)