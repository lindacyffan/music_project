import pandas as pd
import os
import glob
files = glob.glob('data/raw_data_*.csv')
print(f"找到 {len(files)} 个歌单文件")

df_list = []
for file in files:
    df = pd.read_csv(file,encoding='utf-8-sig')
    df_list.append(df)

df_all = pd.concat(df_list, ignore_index=True)
print(f"\n合并后总数据：{len(df_all)} 行")

unique = df_all.drop_duplicates(subset=['id'],keep = 'first')
print(f"去重后保留：{len(unique)} 首独立歌曲")


unique.to_csv('data/raw_data_all.csv', index=False, encoding='utf-8-sig')