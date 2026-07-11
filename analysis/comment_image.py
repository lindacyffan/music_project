import matplotlib.pyplot as plt
import numpy as np

plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

categories = ['情感共鸣', '幽默调侃', '哲理文化', '粉丝支持', '科普信息', '其他']
high_like = [48, 21, 16, 11, 3, 1]
random_like = [37, 31, 9, 12, 7, 4]

x = np.arange(len(categories))
width = 0.35

plt.figure(figsize=(10, 6))
bars1 = plt.bar(x - width/2, high_like, width, label='高赞组', color='#4CAF50')
bars2 = plt.bar(x + width/2, random_like, width, label='随机组', color='#FF9800')

for bar, val in zip(bars1, high_like):
    plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1, f'{val}%', ha='center', va='bottom', fontsize=10)
for bar, val in zip(bars2, random_like):
    plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1, f'{val}%', ha='center', va='bottom', fontsize=10)

plt.title('高赞组 vs 随机组评论类型对比', fontsize=16)
plt.xlabel('评论类型', fontsize=12)
plt.ylabel('占比（%）', fontsize=12)
plt.xticks(x, categories)
plt.legend()
plt.savefig('C:/Users/53125/Desktop/music_project/analysis/comment_type_comparison.png', dpi=300, bbox_inches='tight')
plt.show()