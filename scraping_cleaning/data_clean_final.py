# Final data cleaning after check_websites.py

import numpy as np
import pandas as pd
import re

df = pd.read_csv('FI_webscan_all_columns_raw.csv')

# Cleans the data for Facebook sites
# Last update field
df.loc[df['last_update'].str.len() == 2, 'last_update'] = 'October, 2023'
df.loc[df['last_update'].str.len() == 3, 'last_update'] = 'October, 2023'
df.loc[df['last_update'].str.contains("Yesterday", na=False), 'last_update'] = 'October, 2023'
df.loc[df['last_update'].str.contains('lokakuu', na=False), 'last_update'] = 'October, 2023'
df.loc[df['last_update'].str.contains('kuu', na=False), 'last_update'] = '18 July, 2021'
df.loc[df['last_update'].str.contains(' pv,', na=False), 'last_update'] = 'October, 2023'

df['last_update'] = df['last_update'].apply(lambda x: str(x).split('at')[ 0 ] if 'at' in str(x) else x)
df['last_update'] = df['last_update'].astype(str)
df.loc[(df['last_update'] != 'nan') & (df['last_update'] != 'no_posts') & (
    ~df['last_update'].str.contains('\,')), 'last_update'] = df['last_update'] + ', 2023'
df.loc[df['last_update'] == 'no_posts', 'last_update'] = np.NaN
df.loc[df['last_update'] == ', 2023', 'last_update'] = np.NaN

df['fb_last_update_year'] = df['last_update'].apply(lambda x: str(x).split(', ')[1] if ", " in str(x) else 0)
df['fb_last_update_year'] = df['fb_last_update_year'].astype(np.int16)

# Change status for restaurants that are marked as permanently closed on their Facebook page.
df.loc[(df['status'] == 'in rating') & (df['description'].str.contains('Permanently Closed', na=False)), 'status'] = 'fb_closed'

# Facebook rating and Facebook reviews fields
df['fb_rating'] = df['description'].apply(lambda x: str(x).split(' · ')[-1] if str(x).endswith('Reviews)') else np.NaN)
df['fb_reviews'] = df['fb_rating'].apply(lambda x: str(x).split('(')[-1] if str(x).endswith('Reviews)') else np.NaN)
df['fb_rating'] = df['fb_rating'].apply(lambda x: str(x).split(' ')[0] if str(x).endswith('Reviews)') else np.NaN)
df['fb_reviews'] = df['fb_reviews'].apply(lambda x: str(x).split(' ')[0] if str(x).endswith('Reviews)') else np.NaN)
df.loc[df['fb_rating'].str.len() > 3, 'fb_rating'] = np.NaN

# Facebook followers
df['fb_followers'] = 0
df['fb_followers'] = df.apply(lambda x: re.findall('(.*) followers', str(x['subscribers']))[0] if 'followers' in str(x['subscribers']) else x['fb_followers'],
                     axis=1)
df['fb_followers'] = df.apply(lambda x: re.findall('(.*) seuraajaa', str(x['subscribers']))[0] if 'seuraajaa' in str(x['subscribers']) else x['fb_followers'],
                     axis=1)
df['fb_followers'] = df.apply(lambda x: str(x['subscribers']).split('sledovatelia: ')[-1] if 'sledovatelia' in str(x['subscribers']) else x['fb_followers'],
                     axis=1)
df['fb_followers'] = df.apply(lambda x: str(x['subscribers']).split('последователи: ')[-1] if 'последователи' in str(x['subscribers']) else x['fb_followers'],
                     axis=1)
df['fb_followers'] = df['fb_followers'].apply(lambda x: str(x).split(' • ')[1] if ' • ' in str(x) else x)

df['fb_followers'] = df['fb_followers'].apply(lambda x: str(x).replace('K', '') + '00' if ('.' in str(x)) & ('K' in str(x)) else x)
df['fb_followers'] = df['fb_followers'].apply(lambda x: str(x).replace('tis.', '') + '00' if (',' in str(x)) & ('tis.' in str(x)) else x)
df['fb_followers'] = df['fb_followers'].apply(lambda x: str(x).replace('t', '') + '00' if (',' in str(x)) & ('t' in str(x)) else x)
df['fb_followers'] = df['fb_followers'].apply(lambda x: str(x).replace('K', '000'))
df['fb_followers'] = df['fb_followers'].apply(lambda x: str(x).replace('t', '000'))
df['fb_followers'] = df['fb_followers'].str.replace('.', '').str.replace(',', '').str.replace(' ', '')
df['fb_followers'] = df['fb_followers'].str.replace('nan', '0').fillna(0)
df['fb_followers'] = df['fb_followers'].str.replace('последователи', '')
df.loc[df['fb_followers'] == '', 'fb_followers'] = 0
df['fb_followers'] = df['fb_followers'].astype(np.int16)

# Removing e-mails
def replace_email(x):
    return re.sub(r'([a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)', 'some@email.com', str(x))

df['description'] = df['description'].apply(lambda x: replace_email(x))

# Website type field
df['website_type'] = 'non-facebook'
df.loc[df['website'].isnull(), 'website_type'] = 'no_website'
df.loc[df['website'].str.contains('\.facebook\.', na=False), 'website_type'] = 'facebook'
df.loc[df['website'].str.contains('/facebook\.', na=False), 'website_type'] = 'facebook'

# Website status field
df['website_status'] = 'no_website'
df.loc[df['is_available'].isin(['account_deleted', 'account_not_found', 'account_doesnt_exist']), 'website_status'] = 'unavailable'
df.loc[df['is_available'] == 'account_exists', 'website_status'] = 'online'

df['is_available1'] = True
df.loc[(df['website_type'] =='non-facebook') & (df['is_available'].isnull()), 'is_available1'] = False
df.loc[(df['website_type'] =='non-facebook') & (df['is_available'] == 'failed_to_access'), 'is_available1'] = False
df.loc[(df['website_type'] =='non-facebook') & (df['is_available'] == ''), 'is_available1'] = False

string_list = ['not found', 'Not Found', 'This website is for sale', '403', 'Default Web Site',
               'Index of', 'Error', 'error', 'Website Expired', 'Account Suspended', 'domain', 'Domain',
               '404', 'domén', 'webstranky', 'Gateway time-out', 'už odstranený', 'Default index', 'cannot be found',
               'uckbook', 'hosting provider', 'website is suspended', 'Connection timed out', 'not exist',
               "Web Server's", 'EI LÖYTYNYT', 'ei löytynyt', 'ei löydy', 'Tietokantavirhe', 'Login to Redash',
               'Webhosting', 'bet365',  'Authorization Required']

for string in string_list:
    df.loc[(df['website_type'] == 'non-facebook') &
           (df['is_available'].str.contains(string)), 'is_available1'] = False

df.loc[(df['website_type'] =='non-facebook') & (df['is_available'].str.contains('Cloudflare')), 'is_available1'] = True

df['is_available2'] = True
df.loc[(df['website_type'] =='non-facebook') & (df['homesite_user_name'].isnull()), 'is_available2'] = False
df.loc[(df['website_type'] =='non-facebook') & (df['homesite_user_name'] == 'failed_to_access'), 'is_available2'] = False
df.loc[(df['website_type'] =='non-facebook') & (df['homesite_user_name'] == ''), 'is_available2'] = False

for string in string_list:
    df.loc[(df['website_type'] == 'non-facebook') &
           (df['homesite_user_name'].str.contains(string)), 'is_available2'] = False

df.loc[(df['website_type'] =='non-facebook') & (df['homesite_user_name'].str.contains('Cloudflare')), 'is_available2'] = True

df.loc[df['website_type'] == 'non-facebook', 'website_status'] = 'online'
df.loc[(df['is_available1'] == False) & (df['is_available2'] == False), 'website_status'] = 'unavailable'
df.loc[(df['is_available1'] == False) & (df['website'].str.contains('raflaamo', na=False)), 'website_status'] = 'unavailable'

# Save the data and remove not needed columns
df.to_csv('FI_webscan_all_columns.csv', index=False)
del df['subscribers'], df['is_available'], df['homesite_user_name'], df['is_available1'], df['is_available2']

# Reorder records
df_old = pd.read_csv('tripadvisor_european_restaurants.csv')
df_old = df_old.loc[df_old['country'] == 'Northern Ireland']

df_old = df_old.reset_index()
df_old = df_old.rename(columns={"index":"rank"})
df_old = df_old[['restaurant_link', 'rank']]

df = df.merge(df_old, how='inner', left_on='id', right_on='restaurant_link')
df = df.sort_values('rank')
del df['rank']
del df['restaurant_link']

# Final save
df.to_csv('FI_with_webscan.csv', index=False)