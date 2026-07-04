import pandas as pd

df = pd.read_csv('data/artist.csv',encoding='utf-8-sig')

unique = df.drop_duplicates(subset=['artist_id'], keep = 'first')

unique.to_csv('data/artists_unique.csv', index=False, encoding = 'utf-8-sig')

print(f"去重前：{len(df)} 行")
print(f"去重后：{len(unique)} 行")