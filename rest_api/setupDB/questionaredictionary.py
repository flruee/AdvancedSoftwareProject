

# these should be the options for the dropdownmenu location
boroughs = [
    'The Bronx',
    'Brooklyn',
    'Manhattan',
    'Queens',
    'Staten Island'
]


Interest = [
    'Food',
    'Art & Music',
    'Sightseeing',
    'Shopping',
    'Sports',
    'Nightlife'
]

age_range = {
    'a': '18-30',
    'b': '31-50',
    'c': '51-120'
}

age_range2 = ['18-30','31-50','51-120']
import json
import wget
import os
import pandas as pd
import numpy as np

if os.path.exists('newyork_data.json'):
    os.remove('newyork_data.json')
wget.download('https://cocl.us/new_york_dataset/newyork_data.json')

with open('newyork_data.json') as json_data:
    newyork_data = json.load(json_data)

# define the dataframe columns
column_names = ['Borough', 'Neighborhood']

# instantiate the dataframe
neighborhoods = pd.DataFrame(columns=column_names)
neighborhoods_data = newyork_data['features']

for data in neighborhoods_data:
    borough = data['properties']['borough']
    neighborhood_name = data['properties']['name']

    neighborhoods = neighborhoods.append({'Borough': borough,
                                          'Neighborhood': neighborhood_name}, ignore_index=True)
                                                


print("\n")
print('The dataframe has {} boroughs and {} neighborhoods.'.format(
        len(neighborhoods['Borough'].unique()),
        neighborhoods.shape[0]
    )
)
print(neighborhoods.head())

villages = np.unique(neighborhoods['Neighborhood'])
print(villages)
df = pd.DataFrame(columns=['village',"category"])

def addData(l,df):
    for cat in l:
        df = df.append({'village':village,'category': cat},ignore_index=True)
    return df

for village in villages:

## TOP 20 Neighborhoods Manhattan
    if village == 'Midtown':
        l = ['a','b','c','Food', 'Sightseeing', 'Nightlife']
        df=addData(l, df)

    if village == 'Soho':
        l = ['a','b','c','Art & Music', 'Shopping', 'Food']
        df=addData(l, df)
    if village == 'Chelsea':
        l = ['a','b','c','Art & Music', 'Shopping', 'Food', 'Nightlife']
        df=addData(l, df)

    if village == 'Upper East Side':
        l = ['b','c','Shopping', 'Sightseeing']
        df=addData(l, df)

    if village == 'East Village':
        l = ['a','b','Art & Music', 'Food', 'Nightlife']
        df=addData(l, df)


    if village == 'Lower East Side':
        l = ['a','Art & Music', 'Food', 'Nightlife']
        df=addData(l, df)


    if village == 'Tribeca':
        l = ['b','c','Food', 'Sightseeing']
        df=addData(l, df)


    if village == 'Greenwich Village':
        l = ['a','b','c','Art & Music', 'Sightseeing', 'Food']
        df=addData(l, df)


    if village == 'Harlem':
        l = ['b','Art & Music']
        df=addData(l, df)


    if village == 'Flatiron':
        l = ['b','c','Sightseeing', 'Food']
        df=addData(l, df)

    if village == 'Chinatown':
        l = ['a','Food', 'Nightlife', 'Sightseeing', 'Shopping']
        df=addData(l, df)

    if village == 'Upper West Side':
        l = ['c','Sightseeing', 'Food']
        df=addData(l, df)

    if village == 'West Village':
        l = ['a','b','Food', 'Shopping']
        df=addData(l, df)

    if village == 'Gramercy':
        l = ['b','c','Sightseeing', 'Art & Music']
        df=addData(l, df)

    if village == 'Nolita':
        l = ['a','b','c','Shopping', 'Sightseeing']
        df=addData(l, df)

    if village == 'Battery Park City':
        l = ['c','Sightseeing']
        df=addData(l, df)

    if village == 'Noho':
        l = ['a','b','Food']
        df=addData(l, df)


    # Top 10 Brookyln

    if village == 'Park Slope':
        l = ['b','c','Food', 'Art & Music']
        df=addData(l, df)

    if village == 'Carroll Gardens':
        l = ['a','b','c','Food', 'Art & Music']
        df=addData(l, df)

    if village == 'Cobble Hill':
        l = ['b','c','Sightseeing', 'Food', 'Shopping']
        df=addData(l, df)

    if village == 'Greenpoint':
        l = ['a','Food', 'Nightlife']
        df=addData(l, df)

    if village == 'Fort Greene':
        l = ['a','b','Art & Music', 'Food', 'Shopping', 'Nightlife']
        df=addData(l, df)

    if village == 'Brooklyn Heights':
        l = ['a','Food']
        df=addData(l, df)

    if village == 'Dumbo':
        l = ['a','b','Sightseeing', 'Food', 'Nightlife']
        df=addData(l, df)

    if village == 'Williamsburg':
        l = ['a','Nightlife', 'Food', 'Shopping']
        df=addData(l, df)

    if village == 'Bushwick':
        l = ['a','Art & Music', 'Food', 'Nightlife']
        df=addData(l, df)

    if village == 'Red Hook':
        l = ['a','b','Art & Music', 'Food', 'Nightlife']
        df=addData(l, df)


    # Top 10 Bronx

    if village == 'Concourse':
        l = ['a','b','Food', 'Sightseeing']
        df=addData(l, df)

    if village == 'Fordham':
        l = ['a','b','c','Sightseeing', 'Shopping']
        df=addData(l, df)

    if village == 'Kingsbridge':
        l = ['a','b','Sightseeing']
        df=addData(l, df)

    if village == 'Mott Haven':
        l = ['a','b','c','Food']
        df=addData(l, df)

    if village == 'Riverdale':
        l = ['c','Food']
        df=addData(l, df)

    if village == 'Woodlawn':
        l = ['a','b','Nightlife']
        df=addData(l, df)

    if village == 'South Bronx':
        l = ['b','Sightseeing']
        df=addData(l, df)

    if village == 'City Island':
        l = ['a','b','c','Food']
        df=addData(l, df)

    if village == 'Belmont':
        l = ['a','b','Food']
        df=addData(l, df)


    # Top 8 Staten Island

    if village == 'West Brighton':
        l = ['b','c','Food']
        df=addData(l, df)

    if village == 'St. George':
        l = ['a','b','c','Food', 'Sightseeing', 'Nightlife']
        df=addData(l, df)

    if village == 'New Dorp':
        l = ['a','b','c','Food', 'Sightseeing', 'Nightlife', 'Art & Music']
        df=addData(l, df)

    if village == 'Great Kills':
        l = ['b','c','Sightseeing']
        df=addData(l, df)

    if village == 'Oakwood':
        l = ['b','c','Shopping']
        df=addData(l, df)

    if village == 'Todt Hill':
        l = ['c','Food']
        df=addData(l, df)

    if village == 'Randall Manor':
        l = ['c','Sightseeing']
        df=addData(l, df)

    # Top 9 Queens

    if village == 'Long Island City':
        l = ['a','b','c','Sightseeing', 'Nightlife', 'Food', 'Art & Music']
        df=addData(l, df)

    if village == 'Astoria':
        l = ['a','Sightseeing', 'Art & Music', 'Food']
        df=addData(l, df)

    if village == 'Jackson Heights':
        l = ['a','b','Food', 'Nightlife']
        df=addData(l, df)
    if village == 'Forest Hills':
        l = ['b','c','Sightseeing']
        df=addData(l, df)

    if village == 'Corona':
        l = ['a','b','Art & Music']
        df=addData(l, df)

    if village == 'Rockaway Beach':
        l = ['a','b','c','Shopping', 'Art & Music', 'Food']
        df=addData(l, df)

    if village == 'Flushing':
        l = ['a','Food']
        df=addData(l, df)

    if village == 'Jamaica Hills':
        l = ['b','c','Sightseeing']
        df=addData(l, df)

    if village == 'Tompkinsville':
        l = ['b','c','Food','Sightseeing']
        df=addData(l, df)

    if village == 'Sunnyside':
        l = ['a','b','c','Sightseeing', 'Food', 'Nightlife']
        df=addData(l, df)


df['category'] = df['category'].replace(age_range)
df['village'] = df['village'].astype(str)
df['category'] = df['category'].astype(str)

df1 = df[df['category'].isin(age_range2)].copy()
df1.columns = ['village',"age"]
df1['village'] = df1['village'].astype(str)
df1['age'] = df1['age'].astype(str)



df2 = df[df['category'].isin(Interest)].copy()
df2.columns = ['village','interest']
df2['village'] = df2['village'].astype(str)
df2['interest'] = df2['interest'].astype(str)
df3 = df1.merge(df2,on="village",how="outer")

df3.to_csv("neighborhood_activity.csv",index=False)

























