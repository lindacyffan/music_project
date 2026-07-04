import pandas as pd
import glob
import os

# 读取所有 raw_data_*.csv 文件
files = glob.glob('data/raw_data_*.csv')
print(f"找到 {len(files)} 个歌单文件")

df_list = []
for file in files:
    # 从文件名提取歌单名称
    # 例如：data/raw_data_热歌榜.csv → 热歌榜
    
    filename = os.path.basename(file)  # raw_data_热歌榜.csv
    source = filename.replace('raw_data_', '').replace('.csv', '')  # 热歌榜
    if filename == 'raw_data_all.csv':
        print(f"  ⏭ 跳过 {filename}（汇总文件）")
        continue
    df = pd.read_csv(file, encoding='utf-8-sig')
    df['source'] = source  # 添加 source 列
    print(f"  ✓ 读取 {filename}：{len(df)} 首 → 来源：{source}")
    df_list.append(df)

# 合并所有数据
df_all = pd.concat(df_list, ignore_index=True)
print(f"\n合并后总数据：{len(df_all)} 行")

# 按 id 去重（去重时会保留第一次出现的 source）
df_unique = df_all.drop_duplicates(subset=['id'], keep='first')
print(f"去重后保留：{len(df_unique)} 首独立歌曲")

# 保存
df_unique.to_csv('data/raw_data_all.csv', index=False, encoding='utf-8-sig')
print("\n✅ 汇总完成！保存为 data/raw_data_all.csv")
print(f"   包含 source 列，共有 {df_unique['source'].nunique()} 个不同来源")