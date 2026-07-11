import matplotlib.pyplot as plt

plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

scenes = ['跑步听华语', '旅行听华语', '通勤好状态']
densities = [0.00675, 0.00689, 0.00123]

plt.figure(figsize=(8, 6))
bars = plt.bar(scenes, densities, color=['#4CAF50', '#2196F3', '#FF5722'])

for bar, val in zip(bars, densities):
    plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.0001, 
             f'{val:.5f}', ha='center', va='bottom', fontsize=12)

plt.title('不同场景歌单语气词密度对比', fontsize=16)
plt.xlabel('场景', fontsize=12)
plt.ylabel('语气词密度（次数/总字数）', fontsize=12)

plt.savefig('C:/Users/53125/Desktop/music_project/analysis/modal_density.png', dpi=300, bbox_inches='tight')
plt.show()