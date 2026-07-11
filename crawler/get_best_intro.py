import pandas as pd

df = pd.read_csv('data/artists.csv', encoding='utf-8-sig')


df['intro_len'] = df['artist_intro'].fillna('').str.len()

# 按 artist_id 分组，保留 intro_len 最大的行
df_unique = df.loc[df.groupby('artist_id')['intro_len'].idxmax()]


df_unique = df_unique.drop(columns=['intro_len'])

df_unique.to_csv('data/artists_unique.csv', index=False, encoding='utf-8-sig')

print(f"去重前：{len(df)} 条")
print(f"去重后：{len(df_unique)} 位歌手")