# -*- coding: utf-8 -*-
"""Untitled3.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1Z1uf7sLgFU1LkGshJLYo7UZEXENXH6Gh
"""

import json
import pandas as pd
import numpy as np
import os
import datetime

os.system("curl -O https://api.rootnet.in/covid19-in/stats/hospitals");

os.system("curl -O https://api.rootnet.in/covid19-in/stats/daily")

os.system("curl -O https://api.rootnet.in/covid19-in/contacts")

with open('hospitals') as json_file:
	data = json.load(json_file)

df = pd.DataFrame(columns=['state', 'ruralHospitals', 'ruralBeds', 'urbanHospitals', 'urbanBeds', 'totalHospitals', 'totalBeds'])

for item in data['data']['regional']:
    df = df.append(item, ignore_index=True)

with open('daily') as f:
  data = json.load(f)
  max_date = data['data'][-1]['day']
for item in data['data']:
    day = datetime.datetime.strptime(item['day'], '%Y-%m-%d').strftime("%B %d")
    for reg_item in item['regional']:
        if not day in df.columns:
            df[day] = 0
        df.loc[df['state'] == reg_item['loc'], day] =  reg_item['confirmedCasesIndian'] + reg_item['confirmedCasesForeign']
df['Final'] = df[datetime.datetime.strptime(max_date, '%Y-%m-%d').strftime("%B %d")]

df['hospitalBeds'] = df['totalBeds']

with open('contacts') as f:
  data = json.load(f)

df['helpline'] = 1075

for item in data['data']['contacts']['regional']:
    df.loc[df['state'] == item['loc'], 'helpline'] = item['number']

df = df.fillna(0)

index = df[df['state'] == 'INDIA'].index
df.drop(index , inplace=True)

df = df.rename(columns={
    "state": "Name",
    "ruralHospitals": "Rural Hospitals", 
    "ruralBeds": "Rural Beds", 
    "urbanHospitals": "Urban Hospitals", 
    "urbanBeds": "Urban Beds", 
    "totalHospitals": "Total Hospitals",
    "hospitalBeds": "Hospital Beds",
    "confirmed": "Confirmed Cases",
    "recovered": "Recovered Cases", 
    "deaths": "Deaths",
    "helpline": "Helpline"
    })

for index, row in df.iterrows():
    if '&'in row['Name']:
        df.loc[index, 'Name'] = row['Name'].replace('&', 'and')

for index, row in df.iterrows():
    if '&'in str(row['Helpline']):
        df.loc[index, 'Helpline'] = str(row['Helpline']).replace('+91-', '0')
    if ',' in str(row['Helpline']):
        df.loc[index, 'Helpline'] = str(df.loc[index, 'Helpline']).split(',')[0]

df.to_csv('india_states_daily.csv', index=False)

"""## For map data"""

df = pd.DataFrame(columns=['state', 
                           'ruralHospitals', 'ruralBeds', 
                           'urbanHospitals', 'urbanBeds', 
                           'totalHospitals', 'totalBeds', 
                           'confirmed', 'recovered', 'deaths', 'date'])

with open('hospitals') as json_file:
	data = json.load(json_file)
india = data['data']['summary']
india['state'] = 'India'
df = df.append(india, ignore_index=True)
for item in data['data']['regional']:
    df = df.append(item, ignore_index=True)

df.head()

with open('daily') as f:
  data = json.load(f)
item = data['data'][-1]
day = datetime.datetime.strptime(item['day'], '%Y-%m-%d').strftime("%B %d")
index = df['state'] == 'India'
df.loc[index, 'state'] =  'India'
df.loc[index, 'confirmed'] =  item['summary']['total'], 
df.loc[index, 'deaths'] =  item['summary']['deaths']
df.loc[index, 'recovered'] =  item['summary']['discharged'], 
df.loc[index, 'date'] = day
for reg_item in item['regional']:
    index = df['state'] == reg_item['loc']
    df.loc[index, 'state'] =  reg_item['loc']
    df.loc[index, 'confirmed'] =  reg_item['confirmedCasesIndian'] + reg_item['confirmedCasesForeign']
    df.loc[index, 'deaths'] =  reg_item['deaths']
    df.loc[index, 'recovered'] =  reg_item['discharged']
    df.loc[index, 'date'] = day

df.head()

with open('contacts') as f:
  data = json.load(f)

contacts = data['data']

df['helpline'] = 0
df.loc[df['state'] == 'India', 'helpline'] = data['data']['contacts']['primary']['number-tollfree']

for item in data['data']['contacts']['regional']:
    df.loc[df['state'] == item['loc'], 'helpline'] = item['number']

df = df.fillna(0)

df = df.rename(columns={
    "state": "Name",
    "ruralHospitals": "Rural Hospitals", 
    "ruralBeds": "Rural Beds", 
    "urbanHospitals": "Urban Hospitals", 
    "urbanBeds": "Urban Beds", 
    "totalHospitals": "Total Hospitals",
    "totalBeds": "Total Beds",
    "confirmed": "Confirmed Cases",
    "recovered": "Recovered Cases", 
    "Deaths": "Deaths"
    })

for index, row in df.iterrows():
    if '&'in row['Name']:
        df.loc[index, 'Name'] = row['Name'].replace('&', 'and')

df.to_csv('india_states.csv', index=False)