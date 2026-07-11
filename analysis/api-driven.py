import csv
from zhipuai import ZhipuAI

# 初始化客户端
client = ZhipuAI(api_key="5a820ed9184b4e58b7bda268d583bf70.QQQQTruheRFpnbs7")

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

# 按点赞数排序
comments_sorted = sorted(comments, key=lambda x: x['liked_count'], reverse=True)
top_100 = comments_sorted[:100]

# 定义分类 Prompt
def classify_comment(comment):
    prompt = f"""
你是一个评论分类助手。请将以下音乐评论分类为以下类别之一：

1. 情感共鸣：表达个人情感、经历、共鸣，让人感同身受（如"想起初恋"、"哭了"、"太感动了"）
2. 幽默调侃：让人发笑、轻松、反转、玩梗（如"笑死"、"搞笑"、"原来如此"）
3. 科普信息：提供知识、背景、数据、版权信息（如"版权"、"原唱"、"数据"）
4. 粉丝支持：表达对歌手/歌曲的喜爱和支持（如"太好听了"、"加油"、"爱了"）
5. 哲理文化：人生感悟、文化思考（如"人生"、"生命"、"意义"）
6. 其他：不属于以上任何类别

评论内容：{comment}

请只回答类别名称，不要解释。
"""
    
    response = client.chat.completions.create(
        model="glm-4-flash",  # 使用快速免费模型
        messages=[
            {"role": "system", "content": "你是一个评论分类助手，只输出类别名称。"},
            {"role": "user", "content": prompt}
        ],
        temperature=0.1,
    )
    
    return response.choices[0].message.content.strip()

# 分类 Top 100 评论
categories = []
for i, c in enumerate(top_100):
    category = classify_comment(c['content'])
    categories.append(category)
    print(f"{i+1}. [{category}] {c['content'][:30]}...")

# 统计各类别数量
from collections import Counter
counter = Counter(categories)
print("\n类别统计：")
for cat, count in counter.items():
    print(f"  {cat}: {count} 条")