# Clean the data, obtained by restaurant_soap.py script

import numpy as np
import pandas as pd
from collections.abc import Iterable


df_new = pd.read_csv("NI_by_id_all.csv")
#df_new = pd.read_csv("SK_by_id_all.csv")
#df_new = pd.read_csv("BG_by_id_all.csv")
#df_new = pd.read_csv("FI_by_id_all.csv")
country = 'Northern Ireland'

# Set status column
df_new['status']  = 'in rating'
df_new.loc[df_new['rest_name'].str.endswith(' - CLOSED', na=False), 'status'] = 'closed'
df_new.loc[df_new['rest_name'].isnull(), 'status'] = 'redirect'

df_new['id_destination'] = df_new['actual_url'].str.extract('Restaurant_Review-(.+?)-Reviews')
changed_ids = df_new.loc[(df_new['id_destination'] != df_new['id']) & (df_new['id_destination'].notnull()),
                         'id_destination']
changed_ids_duplicates = df_new.loc[df_new['id'].isin(changed_ids), 'id']
df_new.loc[df_new['id'].isin(changed_ids_duplicates), 'status'] = 'duplicate'
df_new.loc[~df_new['country_region'].str.contains(country, na=True), 'status'] = 'duplicate'
del df_new['actual_url']

# Small fixes for multiple columns
df_new['rating'] = df_new['rating'].astype(np.float32)

for col in ['food_rating', 'service_rating', 'value_rating', 'atmosphere_rating']:
    df_new[col] = df_new[col].str.replace("bubble_", "")

df_new['n_reviews'] = df_new['n_reviews'].map(lambda x: str(x).lstrip('(').rstrip(')').replace(',', ''))
df_new['n_reviews'] = df_new['n_reviews'].map(lambda x: int(x) if x!='nan' else 0)

df_new['travellers_choice'] = df_new['travellers_choice'].str.contains("Travelers' Choice2022")
df_new['travellers_choice'] = df_new['travellers_choice'].fillna(0).astype(np.int8)

df_new['michelin'] = df_new['michelin'].str.replace('MICHELIN', '1')
df_new['michelin'] = df_new['michelin'].fillna(0).astype(np.int8)

df_new['price_category'] = df_new['price_range_and_top_tags'].apply(lambda x: str(x).split(',')[0])
df_new['price_category'] = df_new['price_category'].apply(lambda x: str(x).split("'")[1] if "'" in str(x) else 'nan')
df_new['price_category'] = df_new['price_category'].apply(lambda x: x if x in ['$', '$$ - $$$', '$$$$'] else np.NaN)

df_new['top_tags'] = df_new['price_range_and_top_tags'].apply(lambda x: str(x).split(','))
df_new['top_tags'] = df_new['top_tags'].apply(lambda x: x if x == 'nan' or x[0] not in ["['$$ - $$$'", "['$$$$'", "['$'"] else x[1:])
def fix_x(j):
    i_list = []
    for i in j:
        i_list.append(i.strip(" []'"))
    return ', '.join(i_list)
df_new['top_tags'] = df_new['top_tags'].apply(lambda x: fix_x(x))
df_new.loc[df_new['top_tags'].isin(['$', '$$ - $$$', 'nan', '']), 'top_tags'] = np.NaN
del df_new['price_range_and_top_tags']

df_new['meal_types'] = df_new['meal_types'].apply(lambda x: str(x).split(','))
df_new['meal_types'] = df_new['meal_types'].apply(lambda x: fix_x(x))
df_new.loc[df_new['meal_types'] == '', 'meal_types'] = np.NaN

df_new['features'] = df_new['features'].apply(lambda x: str(x).split(','))
df_new['features'] = df_new['features'].apply(lambda x: fix_x(x))
df_new.loc[df_new['features'] == '', 'features'] = np.NaN

df_new['is_claimed'] = df_new['is_claimed'].str.strip()

df_new['working_hours1'] = True
df_new.loc[df_new['working_hours'].str.contains(' Add hours', na=True), 'working_hours1'] = False
df_new['working_hours'] = df_new['working_hours1']
del df_new['working_hours1']

df_new['type'] = df_new['popularity_top'].apply(lambda x: ' '.join(str(x).split(' ')[3:]) if len(str(x).split(' ')) > 4 else x)
df_new['type'] = df_new['type'].apply(lambda x: str(x).split(' in')[0])
df_new['type'] = df_new['type'].apply(lambda x: 'Bakeries' if x == 'Bakery' else x if x == 'Coffee & Tea' else x if x.endswith('s') else x + 's')
df_new.loc[df_new['type'] == 'nans', 'type'] = np.NaN

df_new['website'] = df_new['website'].apply(lambda x: str(x).split('","email":"')[0] if "email" in str(x) else x)

df_new['telephone'] = df_new['telephone'].fillna(0)
df_new.loc[df_new['telephone'] != 0, 'telephone'] = 1
df_new['telephone'] = df_new['telephone'].astype(bool)

del df_new['selected_language']

# Initial cleaning of 'all_languages' column
df_new['all_languages'] = df_new['all_languages'].apply(lambda x: str(x).split(','))
def remove_all_languages(j):
    i_list = []
    for i in j:
        if 'All languages' not in i:
            i_list.append(i.strip(" {}'"))
    return i_list
df_new['all_languages'] = df_new['all_languages'].apply(lambda x: remove_all_languages(x))
df_new['all_languages'] = df_new['all_languages'].apply(lambda x: ', '.join(x))

# Create list of all unique languages
list_of_lang = df_new['all_languages'].apply(lambda x: str(x).split(',') if ',' in str(x) else x)
list_of_lang = [x for x in list_of_lang if str(x) != 'nan']
def flatten(coll):
    for i in coll:
            if isinstance(i, Iterable) and not isinstance(i, str):
                for subc in flatten(i):
                    yield subc
            else:
                yield i


all_of_lang = list(flatten(list_of_lang))
lang_cleaned = []
for i in all_of_lang:
    lang_cleaned.append(' '.join(i.split(' ')[:-1]).strip(' '))

lang_cleaned = list(set(lang_cleaned))
lang_cleaned.remove('')

# Calculate number of reviews in important languages
df_lang = pd.DataFrame(columns=lang_cleaned)

for i in df_new['all_languages']:
    result_string = ['None'] * len(lang_cleaned)
    if ',' in str(i):
        list_i = str(i).split(',')
    else:
        list_i = i
    if isinstance(list_i, str):
        for j in range(len(lang_cleaned)):
            if lang_cleaned[j] in i:
                result_string[j] = i
    elif str(i) != 'nan':
        for k in range(len(list_i)):
            for j in range(len(lang_cleaned)):
                if lang_cleaned[j] in list_i[k]:
                    result_string[j] = list_i[k]
    df_lang = df_lang._append(pd.DataFrame([result_string], columns=lang_cleaned), ignore_index=True)

for col in df_lang.columns:
    df_lang[col] = df_lang[col].apply(lambda x: str(x).split(' ')[-1].strip('()') if str(x) != 'nan' else 0)
    df_lang.loc[df_lang[col] == 'None', col] = 0
    df_lang.loc[df_lang[col] == 'English', col] = 0
    df_lang[col] = df_lang[col].fillna(0).astype(np.int16)

df_lang['non-English'] = df_lang.sum(axis=1)
df_lang['non-English'] = df_lang['non-English'] - df_lang['English']
#df_lang['local'] = df_lang['English']
#df_lang['local'] = df_lang['Slovak']
df_lang['local'] = df_lang['Finnish']

df_join = df_lang[['English', 'non-English', 'local']]
df_new = pd.concat([df_new, df_join], axis=1)

df_new.to_csv('NI_by_id_clean.csv', index=False)
