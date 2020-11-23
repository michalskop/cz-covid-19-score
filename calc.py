"""Calculate traffic light score, ORPs."""

# import csv
import datetime
import numpy as np
import pandas as pd

# parameters: first date
first_date = '2020-03-16'

# read data from UZIS
url = "https://onemocneni-aktualne.mzcr.cz/api/v2/covid-19/orp.csv"
df = pd.read_csv(url, delimiter=",")

# correct ORP codes from UZIS to CZSO
df.loc[df['orp_kod'] == 0, 'orp_kod'] = 1000 # Praha
df.loc[(df['orp_kod'] > 2000) & (df['orp_kod'] < 3000), 'orp_kod'] = df.loc[(df['orp_kod'] > 2000) & (df['orp_kod'] < 3000)]['orp_kod'].add(100)    # Stredni Cechy
df.loc[(df['orp_kod'] > 6000) & (df['orp_kod'] < 7000), 'orp_kod'] = df.loc[(df['orp_kod'] > 6000) & (df['orp_kod'] < 7000)]['orp_kod'].add(-200)    # Jizni Morava, Vysocina
df.loc[(df['orp_kod'] > 8000) & (df['orp_kod'] < 9000), 'orp_kod'] = df.loc[(df['orp_kod'] > 8000) & (df['orp_kod'] < 9000)]['orp_kod'].add(100)    # Moravskoslezsky

# load ORPs info
orps = pd.read_csv("orp_population.csv")

# set dates
first_day = datetime.date.fromisoformat(first_date)
today = datetime.date.today()
todate = today.isoformat()
last_day = today
last_ok_day = today + datetime.timedelta(days=-1)

def value_1_to_score(n):
    if n < 10:
        return 0
    if n < 25:
        return 2
    if n < 50:
        return 4
    if n < 120:
        return 7
    if n < 240:
        return 10
    if n < 480:
        return 13
    if n < 960:
        return 16
    return 20

def value_2_to_score(b):
    if b:
        return 0
    else:
        return 0

def value_3_to_score(n):
    if n < 10:
        return 0
    if n < 25:
        return 2
    if n < 50:
        return 4
    if n < 120:
        return 7
    if n < 240:
        return 10
    if n < 480:
        return 13
    if n < 960:
        return 16
    return 20

# Test 4: value to score
def value_4_to_score(b):
    if b:
        return 2
    else:
        return 0

# Test 5: value to score
def value_5_to_score(n):
    if n < 3:
        return 0
    if n < 7:
        return 3
    if n < 11:
        return 7
    if n < 15:
        return 11
    if n < 19:
        return 15
    if n < 23:
        return 20
    if n < 26:
        return 25
    return 30

# Test 6: value to score
def value_6_to_score(b):
    if b:
        return 2
    else:
        return 0

# Test 7: value to score
def value_7_to_score(n):
    if n < 0.8:
        return 0
    if n < 1:
        return 5
    if n < 1.2:
        return 10
    if n < 1.4:
        return 15
    if n < 1.6:
        return 20
    if n < 1.9:
        return 25
    return 30

# define final file
data = pd.DataFrame(columns=['date', 'code', 'name', 'score'])
data_regions = pd.DataFrame(columns=['date', 'code', 'name', 'score'])
data_cz = pd.DataFrame(columns=['date', 'code', 'name', 'score'])

# for each date
for i in range(0, (last_day - first_day).days + 1):
    day = first_day + datetime.timedelta(days=i)
    date = day.isoformat()
    date_5 = (day - datetime.timedelta(days=5)).isoformat()
    date_7 = (day - datetime.timedelta(days=7)).isoformat()
    date_14 = (day - datetime.timedelta(days=14)).isoformat()

    selected = df[df['datum'] == date].merge(orps, left_on='orp_kod', right_on='code')
    selected = selected.set_index('code', drop=False)
    selected.sort_index(inplace=True)
    selected_regions = pd.pivot_table(selected, values=['incidence_7', 'incidence_65_7', 'testy_7', 'population', 'population_65'], index=['code_region', 'name_region'], aggfunc=np.sum)
    selected_cz = pd.pivot_table(selected, values=['incidence_7', 'incidence_65_7', 'testy_7', 'population', 'population_65'], index=['code_cz', 'name_cz'], aggfunc=np.sum)

    selected_5 = df[df['datum'] == date_5].merge(orps, left_on='orp_kod', right_on='code')
    selected_5 = selected_5.set_index('code', drop=False)
    selected_5.sort_index(inplace=True)
    selected_5_regions = pd.pivot_table(selected_5, values=['incidence_7', 'incidence_65_7', 'testy_7', 'population', 'population_65'], index=['code_region', 'name_region'], aggfunc=np.sum)
    selected_5_cz = pd.pivot_table(selected_5, values=['incidence_7', 'incidence_65_7', 'testy_7', 'population', 'population_65'], index=['code_cz', 'name_cz'], aggfunc=np.sum)


    selected_7 = df[df['datum'] == date_7].merge(orps, left_on='orp_kod', right_on='code')
    selected_7 = selected_7.set_index('code', drop=False)
    selected_7.sort_index(inplace=True)
    selected_7_regions = pd.pivot_table(selected_7, values=['incidence_7', 'incidence_65_7', 'testy_7', 'population', 'population_65'], index=['code_region', 'name_region'], aggfunc=np.sum)
    selected_7_cz = pd.pivot_table(selected_7, values=['incidence_7', 'incidence_65_7', 'testy_7', 'population', 'population_65'], index=['code_cz', 'name_cz'], aggfunc=np.sum)


    selected_14 = df[df['datum'] == date_14].merge(orps, left_on='orp_kod', right_on='code')
    selected_14 = selected_14.set_index('code', drop=False)
    selected_14.sort_index(inplace=True)
    selected_14_regions = pd.pivot_table(selected_14, values=['incidence_7', 'incidence_65_7', 'testy_7', 'population', 'population_65'], index=['code_region', 'name_region'], aggfunc=np.sum)
    selected_14_cz = pd.pivot_table(selected_14, values=['incidence_7', 'incidence_65_7', 'testy_7', 'population', 'population_65'], index=['code_cz', 'name_cz'], aggfunc=np.sum)

    # Test 1 - "incidence_14" per 100000
    selected['value_1'] = (selected['incidence_7'] + selected_7['incidence_7']) / selected['population'] * 100000
    selected['score_1'] = selected['value_1'].apply(lambda x: value_1_to_score(x))
    selected_regions['value_1'] = (selected_regions['incidence_7'] + selected_7_regions['incidence_7']) / selected_regions['population'] * 100000
    selected_regions['score_1'] = selected_regions['value_1'].apply(lambda x: value_1_to_score(x))
    selected_cz['value_1'] = (selected_cz['incidence_7'] + selected_7_cz['incidence_7']) / selected_cz['population'] * 100000
    selected_cz['score_1'] = selected_cz['value_1'].apply(lambda x: value_1_to_score(x))

    # Test 2 - "incidence_14" grows
    selected['value_2'] = selected['value_1'] > ((selected_7['incidence_7'] + selected_14['incidence_7']) / selected_7['population'] * 100000)
    selected['score_2'] = selected['value_2'].apply(lambda x: value_2_to_score(x))
    selected_regions['value_2'] = selected_regions['value_1'] > ((selected_7_regions['incidence_7'] + selected_14_regions['incidence_7']) / selected_7_regions['population'] * 100000)
    selected_regions['score_2'] = selected_regions['value_2'].apply(lambda x: value_2_to_score(x))
    selected_cz['value_2'] = selected_cz['value_1'] > ((selected_7_cz['incidence_7'] + selected_14_cz['incidence_7']) / selected_7_cz['population'] * 100000)
    selected_cz['score_2'] = selected_cz['value_2'].apply(lambda x: value_2_to_score(x))

    # Test 3 - "incidence_65_14" per 100000
    selected['value_3'] = (selected['incidence_65_7'] + selected_7['incidence_65_7']) / selected['population_65'] * 100000
    selected['score_3'] = selected['value_3'].apply(lambda x: value_3_to_score(x))
    selected_regions['value_3'] = (selected_regions['incidence_65_7'] + selected_7_regions['incidence_65_7']) / selected_regions['population_65'] * 100000
    selected_regions['score_3'] = selected_regions['value_3'].apply(lambda x: value_3_to_score(x))
    selected_cz['value_3'] = (selected_cz['incidence_65_7'] + selected_7_cz['incidence_65_7']) / selected_cz['population_65'] * 100000
    selected_cz['score_3'] = selected_cz['value_3'].apply(lambda x: value_3_to_score(x))

    # Test 4 - "incidence_65_14" grows
    selected['value_4'] = selected['value_3'] > ((selected_7['incidence_65_7'] + selected_14['incidence_65_7']) / selected_7['population'] * 100000)
    selected['score_4'] = selected['value_4'].apply(lambda x: value_4_to_score(x))
    selected_regions['value_4'] = selected_regions['value_3'] > ((selected_7_regions['incidence_65_7'] + selected_14_regions['incidence_65_7']) / selected_7_regions['population'] * 100000)
    selected_regions['score_4'] = selected_regions['value_4'].apply(lambda x: value_4_to_score(x))
    selected_cz['value_4'] = selected_cz['value_3'] > ((selected_7_cz['incidence_65_7'] + selected_14_cz['incidence_65_7']) / selected_7_cz['population'] * 100000)
    selected_cz['score_4'] = selected_cz['value_4'].apply(lambda x: value_4_to_score(x))

    # Test 5 - incidence_7 / testy_7
    selected['value_5'] = selected['incidence_7'].div(selected['testy_7']).replace(np.inf, 0) * 100
    selected['score_5'] = selected['value_5'].apply(lambda x: value_5_to_score(x))
    selected_regions['value_5'] = selected_regions['incidence_7'].div(selected_regions['testy_7']).replace(np.inf, 0) * 100
    selected_regions['score_5'] = selected_regions['value_5'].apply(lambda x: value_5_to_score(x))
    selected_cz['value_5'] = selected_cz['incidence_7'].div(selected_cz['testy_7']).replace(np.inf, 0) * 100
    selected_cz['score_5'] = selected_cz['value_5'].apply(lambda x: value_5_to_score(x))

    # Test 6 - incidence_7 / testy_7 grows
    selected['value_6'] = selected['value_5'] > selected_7['incidence_7'].div(selected_7['testy_7']).replace(np.inf, 0) * 100
    selected['score_6'] = selected['value_6'].apply(lambda x: value_6_to_score(x))
    selected_regions['value_6'] = selected_regions['value_5'] > selected_7_regions['incidence_7'].div(selected_7_regions['testy_7']).replace(np.inf, 0) * 100
    selected_regions['score_6'] = selected_regions['value_6'].apply(lambda x: value_6_to_score(x))
    selected_cz['value_6'] = selected_cz['value_5'] > selected_7_cz['incidence_7'].div(selected_7_cz['testy_7']).replace(np.inf, 0) * 100
    selected_cz['score_6'] = selected_cz['value_6'].apply(lambda x: value_6_to_score(x))

    # Test 7 - R : incidence_7 / selected_7[incidence_7]
    selected['value_7'] = selected['incidence_7'].div(selected_5['incidence_7']).replace(np.inf, 0)
    selected['score_7'] = selected['value_7'].apply(lambda x: value_7_to_score(x))
    selected_regions['value_7'] = selected_regions['incidence_7'].div(selected_5_regions['incidence_7']).replace(np.inf, 0)
    selected_regions['score_7'] = selected_regions['value_7'].apply(lambda x: value_7_to_score(x))
    selected_cz['value_7'] = selected_cz['incidence_7'].div(selected_5_cz['incidence_7']).replace(np.inf, 0)
    selected_cz['score_7'] = selected_cz['value_7'].apply(lambda x: value_7_to_score(x))

    # Total score
    selected['score'] = 0
    for i in range(1, 8):
        selected['score'] = selected['score'] + selected['score_' + str(i)]
    
    selected_regions['score'] = 0
    for i in range(1, 8):
        selected_regions['score'] = selected_regions['score'] + selected_regions['score_' + str(i)]

    selected_cz['score'] = 0
    for i in range(1, 8):
        selected_cz['score'] = selected_cz['score'] + selected_cz['score_' + str(i)]
    
    # save analytical files
    selected.to_csv("results/orp_table_" + date + ".csv", index=False)
    selected_regions['date'] = date
    selected_regions.to_csv("results/regions_table_" + date + ".csv")
    selected_cz['date'] = date
    selected_cz.to_csv("results/cz_table_" + date + ".csv")


    # final files
    data = data.append(selected.loc[:,['code', 'name', 'score', 'datum']].rename(columns={'datum': 'date'}), ignore_index=True)
    selected_regions.reset_index(level=selected_regions.index.names, inplace=True)
    data_regions = data_regions.append(selected_regions.rename(columns={'code_region': 'code', 'name_region': 'name'}).loc[:,['code', 'name', 'score', 'date']], ignore_index=True)
    selected_cz.reset_index(level=selected_cz.index.names, inplace=True)
    data_cz = data_cz.append(selected_cz.rename(columns={'code_cz': 'code', 'name_cz': 'name'}).loc[:,['code', 'name', 'score', 'date']], ignore_index=True)
    

    # current score - by yesterday
    if day == last_ok_day:
        last_ok_data = selected.loc[:,['datum', 'code', 'name', 'score']].rename(columns={'datum': 'date'})
        last_ok_data_regions = selected_regions.rename(columns={'code_region': 'code', 'name_region': 'name'}).loc[:,['date', 'code', 'name', 'score']]
        last_ok_data_cz = selected_cz.rename(columns={'code_cz': 'code', 'name_cz': 'name'}).loc[:,['date', 'code', 'name', 'score']]

# save final file
data.to_csv("results/orp_all_scores.csv", index=False)
data_regions.to_csv("results/regions_all_scores.csv", index=False)
data_cz.to_csv("results/cz_all_scores.csv", index=False)

# save current scores - by yesterday
last_ok_data.to_csv("orp_scores.csv", index=False)
last_ok_data_regions.to_csv("regions_scores.csv", index=False)
last_ok_data_cz.to_csv("cz_scores.csv", index=False)
