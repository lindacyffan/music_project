import csv
import jieba.analyse
import matplotlib
import wordcloud
import pandas
from collections import Counter
from wordcloud import WordCloud
stop_words = [
     '那么', '怎么', '什么',  '我们', '自己',
    '因为', '所以', '虽然', '然而', '于是', '因此', '但是', '只是', '不过', '那么',
    '这样', '那样', '怎么', '什么', '现在', '已经', '可以', '没有', '不要', '我要',
    '还是', '如果', '有些', '这些', '那些', '这里', '那里', '哪里', '怎样', '多少',
    '所有', '整个', '一切', '终于', '其实', '果然', '必须', '应该', '能够', '需要',
    '觉得', '知道', '感到', '想到', '不是', '而是',"一个","总是"  ,"就是", "那个" ,"不会", "不能","真的","是否",'为何', '就算', '如何', '这么', '仍然', '不必', '难道', '继续', '不到']

file = open("C:/Users/53125/Desktop/music_project/data/lyrics_data_70后歌单.csv",'r',encoding='utf-8-sig')
words= []
reader = csv.DictReader(file)
for row in reader:
    lyric = row['lyrics']
    keywords = jieba.lcut(lyric)
    for word in keywords:
        if len(word) >1 and word not in stop_words:
            words.append(word)
word_Counts = Counter(words)
high_freq_words = [word for word,count in word_Counts.items() if count>=5]
print(high_freq_words)
top_10 = word_Counts.most_common(10)
print(top_10)
file.close()

wc = WordCloud(
    font_path="C:/Windows/Fonts/msyh.ttc",
    width=800,
    height=600,
    background_color='white'
)

wc.generate_from_frequencies(word_Counts)
wc.to_file('C:/Users/53125/Desktop/music_project/analysis/wordcloud_70s.png')