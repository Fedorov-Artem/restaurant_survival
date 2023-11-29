import numpy as np
import pandas as pd
import gc

df_new = pd.read_csv("NI_by_id_clean.csv")
df_old = pd.read_csv('tripadvisor_european_restaurants.csv')
df_old = df_old.loc[df_old['country'] == 'Northern Ireland']
gc.collect()

df_join = df_new[['id', 'status', 'is_claimed', 'rating', 'last_review', 'n_reviews']]
df_old = df_old.merge(df_join, left_on='restaurant_link', right_on='id', how='outer')
df_old['province'] = df_old['province'].fillna(df_old['region'])
del df_old['region'], df_old['id'], df_join
df_old.loc[df_old['province'] == 'Dunmurry', 'province'] = 'Belfast'
df_old = df_old.loc[df_old ['status'] != 'duplicate']

df_old['last_review_year'] = df_old['last_review'].apply(lambda x: str(x)[-4:] if str(x)!='nan' else 0).astype(np.int16)
#df_old['claimed'] = df_old['claimed'].map({'Claimed':1, 'Unclaimed':0}).fillna(-1).astype(np.int8)
#df_old['claimed_2023'] = df_old['is_claimed'].map({' Claimed':1, ' Unclaimed':0}).fillna(-1).astype(np.int8)
df_old['claimed_2023'] = df_old['is_claimed'].str.strip()
del df_old['is_claimed']
df_old['claimed'] = df_old['claimed'].fillna(df_old['claimed_2023'])

#df['is_active'] = 'active'
#df.loc[df['last_review_year'] < 2021, 'is_active'] = 'recently_inactive'
#df.loc[(df['last_review_year'] < 2019), 'is_active'] = 'long_inactive'
#df.loc[df['status'] == 'redirect', 'is_active'] = 'recently_inactive'
#df.loc[(df['last_review_year']>2020) & (df['status'] == 'closed'), 'is_active'] = 'recently_inactive'
#df_old['is_active'] = df_old['is_active'].map({'long_inactive':0, 'recently_inactive':1, 'active':2}).fillna(-1).astype(np.int8)

#df_old['price_level'] = df_old['price_level'].map({'€':0, '€€-€€€':1, '€€€€':2}).fillna(-1).astype(np.int8)
df_old['price_level'] = df_old['price_level'].fillna('No data')

df_old['total_reviews_count'] = df_old['total_reviews_count'].fillna(df_old['reviews_count_in_default_language'])
df_old['total_reviews_count'] = df_old['total_reviews_count'].fillna(0)

df_old.to_csv('NI_joined.csv', index=False)

df['inc_number'] = df['restaurant_link'].apply(lambda x: x.split('-d')[1]).astype(np.int32)
df_inc = df.groupby('last_review_year').agg({'inc_number':np.max}).reset_index()
df_inc = df_inc.loc[df_inc['last_review_year'] > 2000]
df_inc = df_inc.loc[df_inc['last_review_year'] < 2021]
df_inc = df_inc.sort_values('last_review_year', ascending=False)
df_inc = df_inc.reset_index(drop=True)
df['est_report_year'] = 2021

for i in range(len(df_inc)):
    df.loc[df['inc_number'] < df_inc['inc_number'].iloc[i], 'est_report_year'] = df_inc['last_review_year'].iloc[i]

df['last_activity_year'] = df[["last_review_year", "est_report_year"]].max(axis=1)
df['is_active'] = 'active'
df.loc[df['last_activity_year'] < 2021, 'is_active'] = 'recently_inactive'
df.loc[(df['last_activity_year'] < 2019), 'is_active'] = 'long_inactive'
df.loc[df['status'] == 'redirect', 'is_active'] = 'recently_inactive'
df.loc[(df['last_activity_year']>2020) & (df['status'] == 'closed'), 'is_active'] = 'recently_inactive'
#df_old['is_active'] = df_old['is_active'].map({'long_inactive':0, 'recently_inactive':1, 'active':2}).fillna(-1).astype(np.int8)

df_ni = df.loc[df['country'] == 'Northern Ireland']
df_ni.to_csv('NI_joined.csv', index=False)

df_sk = df.loc[df['country'] == 'Slovakia']
df_sk.to_csv('SK_joined.csv', index=False)

df_bg = df.loc[df['country'] == 'Bulgaria']
df_bg.to_csv('BG_joined.csv', index=False)

df_fi = df.loc[df['country'] == 'Finland']
df_fi.to_csv('FI_joined.csv', index=False)