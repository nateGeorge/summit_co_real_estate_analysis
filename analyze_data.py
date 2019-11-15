import os
import glob

import pandas as pd
import cufflinks as cf
cf.go_offline()


files = glob.glob('data/*.xls*')
dfs = [pd.read_excel(f) for f in files]
all_data = pd.concat(dfs)
all_data.reset_index(inplace=True)
# fix date errors
typos = ['5016-11-02 00:00:00', '5017-11-21 00:00:00']
all_data['Office Date'] = all_data['Office Date'].astype('str')
all_data.at[all_data.index[all_data['Office Date'] == typos[0]][0], 'Office Date'] = '2016-11-02 00:00:00'
all_data.at[all_data.index[all_data['Office Date'] == typos[1]][0], 'Office Date'] = '2017-11-21 00:00:00'
for c in ['Office Date', 'Record Date']:
    all_data[c] = pd.to_datetime(all_data[c])

all_data.set_index('Office Date', inplace=True)
all_data.sort_index(inplace=True)

# get price per SF
all_data['price per SF'] = all_data['Sale Price'] / all_data['SFLA']

# only keep useful columns
cols = ['Sale Price',
        'Acres',
        'Sales Valid',
        'Subdiv Desc',
        'SFLA',
        'Econ',
        'NHood',
        'price per SF']


"""
Office Date -- appears to be date the deed was signed and ownership transferred

Sales Valid -- sales validation code; e.g. 90, 91 are good sales
51 is partial interest -- should exclude these for full sales
10/11 are related parties -- ignore
40 is court ordered (ignore)
good ones to keep: 0, 90, 91
80 is 'excluded sale' -- need to check

SFLA -- sq feet living area

Econ -- town/area (e.g. Silverthorne)
"""

all_data_cln = all_data[cols]
# keep only good sales codes
codes = [0, 90, 91]
all_data_cln = all_data_cln[all_data_cln['Sales Valid'].isin(codes)]

# get treehouse data
th_df = all_data_cln[all_data_cln['Subdiv Desc'].str.contains('TREEHOUSE')]
# only get 3rd floor units
th_df_3 = th_df[th_df['SFLA'] == 1008]

# not super informative
th_df_3['Sale Price'].iplot(asPlot=True)
th_df_3_med = th_df_3.groupby([th_df_3.index.year, th_df_3.index.month]).median()
th_df_3_med['price per SF'].iplot(asPlot=True)

# look at all treehouse
th_med = th_df.groupby([th_df.index.year, th_df.index.month]).median()
th_med['price per SF'].iplot(asPlot=True)


# look at all condos
condos = all_data_cln[all_data_cln['Subdiv Desc'].str.contains('CONDO')]
condo_med = condos.groupby([condos.index.year, condos.index.month]).median()
condo_med['price per SF'].iplot(asPlot=True)