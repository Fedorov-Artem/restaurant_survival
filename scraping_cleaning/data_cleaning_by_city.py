import numpy as np
import pandas as pd

#df1 = pd.read_csv('NI_by_city_0_1.csv')
#df2 = pd.read_csv('NI_by_city_2_5.csv')
#df3 = pd.read_csv('NI_by_city_5_20.csv')
#df4 = pd.read_csv('NI_by_city_20_40.csv')
#df5 = pd.read_csv('NI_by_city_40_155.csv')
#df1 = pd.read_csv('SK_by_city_0_10.csv')
#df2 = pd.read_csv('SK_by_city_10_30.csv')
#df3 = pd.read_csv('SK_by_city_30_100.csv')
#df4 = pd.read_csv('SK_by_city_100_250.csv')
#df5 = pd.read_csv('SK_by_city_250_428.csv')
df1 = pd.read_csv('BG_by_city_0_10.csv')
df2 = pd.read_csv('BG_by_city_10_50.csv')
df3 = pd.read_csv('BG_by_city_10_plus.csv')
df = pd.concat([df1, df2, df3])

df = df.drop_duplicates()
df = df.reset_index(drop=True)

# Clean restaurant name field
df['rest_name'] = df['rest_name'].str.split('.', n=1).str.get(-1)

# Extract restaurant ID from the URL
df['id'] = df['rest_url'].str.extract('Restaurant_Review-(.+?)-Reviews')

# Clean rating field
df['rating'] = df['rating'].str.split(' ', n=1).str.get(0)

# Clean number of reviews field
df['n_reviews'] = df['n_reviews'].str.split(' ', n=1).str.get(0)
df['n_reviews'] = df['n_reviews'].str.replace(',', '')
df['n_reviews'] = df['n_reviews'].fillna(0).astype(np.int16)

# Extract information for menu field
df['menu'] = 0
df.loc[df['top_tags_price'].str.contains('Menu', na=False), 'menu'] = 1
df['top_tags_price'] =  df['top_tags_price'].str.removesuffix('Menu')

# Extract information for price range
df['price_range'] = np.NaN
df.loc[df['top_tags_price'].str.endswith('$$$$', na=False), 'price_range'] = '$$$$'
df['top_tags_price'] =  df['top_tags_price'].str.removesuffix('$$$$')
df.loc[df['top_tags_price'].str.endswith('$$ - $$$', na=False), 'price_range'] = '$$ - $$$'
df['top_tags_price'] =  df['top_tags_price'].str.removesuffix('$$ - $$$')
df.loc[df['top_tags_price'].str.endswith('$', na=False), 'price_range'] = '$'
df['top_tags_price'] =  df['top_tags_price'].str.rstrip('$')

# Clean information for michelin stars
df['michelin'] = df['michelin'].str.replace('MICHELIN', '1')
df['michelin'] = df['michelin'].fillna(0).astype(np.int8)

# Clean information for travellers choice badge
df.loc[df['travellers_choice'] > 0, 'travellers_choice'] = 1
df['travellers_choice'] = df['travellers_choice'].fillna(0).astype(np.int8)

# Clean information for online order availability
df['order_online'] = df['order_online'].apply(lambda x: 1 if x == 'Order online' else 0).astype(np.int8)

# Check if a restaurant is present in 2021 list of restaurants from the same country
df_old = pd.read_csv('tripadvisor_european_restaurants.csv')
df_old = df_old.loc[df_old['country'] == 'Bulgaria']
df_old = df_old[['restaurant_link']]
df = df.merge(df_old, how='left', left_on='id', right_on='restaurant_link')
df['is_new'] = df['restaurant_link'].isnull()
del df['restaurant_link']

# Rename some columns for more clarity
df = df.rename(columns = {'top_tags_price': 'top_tags', 'is_new': 'present_in_2021_dataset'})

# Save the final file
df.to_csv('by_city_clean.cav', index=False)