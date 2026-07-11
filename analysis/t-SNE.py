import csv
import jieba
import random
from zhipuai import ZhipuAI
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.manifold import TSNE
import matplotlib.pyplot as plt
import numpy as np

# 初始化智谱客户端
client = ZhipuAI(api_key="你的API_KEY")

# 读取评论
file = open("C:/Users/53125/Desktop/music_project/data/comments.csv", 'r', encoding='utf-8-sig')
reader = csv.DictReader(file)

comments = []
for row in reader:
    comments.append({
        'content': row['comments_content'],
        'liked_count': int(row['comments_likedCount']),
        'song_id': row['id'],
    })
file.close()

# 按点赞数排序，取前 200 条高赞评论
comments_sorted = sorted(comments, key=lambda x: x['liked_count'], reverse=True)
top_200 = comments_sorted[:200]

# 定义分类函数
def classify_comment(comment):
    prompt = f"""
你是一个评论分类助手。请将以下音乐评论分类为以下类别之一：

1. 情感共鸣：表达个人情感、经历、共鸣，让人感同身受
2. 幽默调侃：让人发笑、轻松、反转、玩梗
3. 科普信息：提供知识、背景、数据、版权信息
4. 粉丝支持：表达对歌手/歌曲的喜爱和支持
5. 哲理文化：人生感悟、文化思考
6. 其他：不属于以上任何类别

评论内容：{comment}

请只回答类别名称，不要解释。
"""
    
    response = client.chat.completions.create(
        model="glm-4-flash",
        messages=[
            {"role": "system", "content": "你是一个评论分类助手，只输出类别名称。"},
            {"role": "user", "content": prompt}
        ],
        temperature=0.1,
    )
    
    return response.choices[0].message.content.strip()

# 分类前 200 条评论
categories = []
contents = []
for i, c in enumerate(top_200):
    category = classify_comment(c['content'])
    categories.append(category)
    contents.append(c['content'])
    print(f"{i+1}/200: {category}")

# 统计类别分布
from collections import Counter
counter = Counter(categories)
print("\n类别统计：")
for cat, count in counter.items():
    print(f"  {cat}: {count} 条")

# 用 jieba 分词，用于向量化（中文分词）
def chinese_tokenizer(text):
    return ' '.join(jieba.lcut(text))

# 向量化
vectorizer = TfidfVectorizer(
    tokenizer=chinese_tokenizer,
    max_features=500,
    lowercase=False
)
vectors = vectorizer.fit_transform(contents).toarray()

# t-SNE 降维
print("\n正在进行 t-SNE 降维...")
tsne = TSNE(n_components=2, random_state=42, perplexity=30)
coords = tsne.fit_transform(vectors)

# 颜色映射
color_map = {
    '情感共鸣': '#FF6B6B',   # 红
    '幽默调侃': '#4ECDC4',   # 青
    '科普信息': '#45B7D1',   # 蓝
    '粉丝支持': '#FFA94D',   # 橙
    '哲理文化': '#A66CFF',   # 紫
    '其他': '#95A5A6'        # 灰
}

colors = [color_map.get(cat, '#95A5A6') for cat in categories]

# 画图
plt.figure(figsize=(12, 10))
scatter = plt.scatter(coords[:, 0], coords[:, 1], c=colors, s=30, alpha=0.7)

# 创建图例
legend_elements = []
for cat, color in color_map.items():
    if cat in counter:
        legend_elements.append(plt.Line2D([0], [0], marker='o', color='w', 
                                          markerfacecolor=color, markersize=10, label=f'{cat} ({counter[cat]}条)'))
plt.legend(handles=legend_elements, loc='upper right')

plt.title('高赞评论 t-SNE 可视化（按类别着色）', fontsize=16)
plt.xlabel('t-SNE 维度 1')
plt.ylabel('t-SNE 维度 2')
plt.savefig('tsne_comments.png', dpi=300, bbox_inches='tight')
plt.show()