import matplotlib.pyplot as plt

plt.rcParams['font.sans-serif']=['SimHei']
plt.rcParams['axes.unicode_minus']=False

labels = ['70后','80后','00后']
scores = [0.807,0.950,0.900]

plt.figure(figsize=(8,6))

plt.plot(
    labels,
    scores,
    marker='o',
    linestyle='-',
    linewidth=2,
    markersize =10,
    color ='#2196F3'
)

for i,score in enumerate(scores):
    plt.text(i,score,f'{score:.3f}',ha='center',va='bottom',fontsize=12)
plt.title('三个年代歌单情感得分变化趋势',fontsize=16)
plt.xlabel('年代', fontsize=12)
plt.ylabel('平均情感得分', fontsize=12)
plt.ylim(0.7,1.0)
plt.savefig('C:/Users/53125/Desktop/music_project/analysis/emotion_trend.png',dpi=300,bbox_inches='tight')