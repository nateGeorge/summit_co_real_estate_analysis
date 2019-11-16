"""
filepaths are relative; this is intended to be run from the home directory of the repo
"""

import os
import glob

import pandas as pd
import cufflinks as cf
cf.go_offline()

def load_data():
    """
    loads data from excel files
    data source: http://www.co.summit.co.us/389/Sales-Reports
    """
    files = glob.glob('data/*.xls*')
    monthly_files = glob.glob('data/2019/*.xls*')
    files += monthly_files
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
            'price per SF',
            'Property Desc']


    """
    Office Date -- appears to be date the deed was signed and ownership transferred

    Sales Valid -- sales validation code; e.g. 90, 91 are good sales
    0 is skip -- not sure what this means
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
    # some 'Improvement Only' with code 90...seems like remodeling or something
    all_data_cln = all_data_cln[~all_data_cln['Property Desc'].str.contains('Improvement Only')]

    # some sales with very low price per SF for some reason, and some with very high
    # all_data_cln = all_data_cln[all_data_cln['price per SF'] > 20]

    # ignore office dates before 2014
    all_data_cln = all_data_cln[all_data_cln.index.year >= 2014]

    # some SF measurements of 0; some of these are land
    all_data_cln = all_data_cln[all_data_cln['SFLA'] > 0]

    return all_data_cln


def flatten_multiindex(df):
    """
    flattens a multiindex dataframe where indices are month and years

    returns a dataframe with a datetimeindex
    """
    flat_idx = df.index.to_flat_index()
    flat_idx_dt = pd.DatetimeIndex([pd.to_datetime(str(f[1]) + '-' + str(f[0])) for f in flat_idx])
    flat_df = pd.DataFrame(index=flat_idx, data=df.to_dict())
    flat_df.set_index(flat_idx_dt, inplace=True)
    return flat_df


if __name__ == '__main__':
    all_data_cln = load_data()

    # get treehouse data
    th_df = all_data_cln[all_data_cln['Subdiv Desc'].str.contains('TREEHOUSE')]
    # maybe a typo or something, but one unit with very low price
    th_df = th_df[th_df['Sale Price'] > 10000]
    # only get 3rd floor units with ~1000 sq ft
    th_df_3 = th_df[th_df['SFLA'] == 1008]

    # plot sales price of third floor units
    filename = 'images/3rd_floor_unit_sales.png'
    fig = th_df_3['Sale Price'].iplot(kind='scatter',
                                        mode='lines+markers',
                                        size=7,
                                        opacity=0.5,
                                        asFigure=True,
                                        xTitle='date',
                                        yTitle='USD sales price',
                                        title='individual USD sales price of 3rd floor treehouse condos')
    fig.write_image(filename, scale=3)

    # plot price per SF for 3rd floor units
    filename = 'images/3rd_floor_unit_sales_per_sf.png'
    th_df_3_med = th_df_3.groupby([th_df_3.index.year, th_df_3.index.month]).median()
    flat_df = flatten_multiindex(th_df_3_med)
    fig = flat_df['price per SF'].iplot(kind='scatter',
                                        mode='lines+markers',
                                        size=7,
                                        opacity=0.5,
                                        asFigure=True,
                                        xTitle='date',
                                        yTitle='USD sales price per SF',
                                        title='monthly USD sales price per SF of 3rd floor treehouse condos')
    fig.write_image(filename, scale=3)

    # look at all treehouse
    # overall price histogram is skewed (possibly from time)
    # so use median as central tendency measure
    # th_df['price per SF'].iplot(kind='histogram', asPlot=True)
    # sales_count = th_df.groupby([th_df.index.year, th_df.index.month]).count()
    # sales_count.iplot(asPlot=True)

    th_med = th_df.groupby([th_df.index.year, th_df.index.month]).median()
    
    flat_df = flatten_multiindex(th_med)

    filename = 'images/treehouse_price_per_sf.png'
    fig = flat_df['price per SF'].iplot(kind='scatter',
                                        mode='lines+markers',
                                        size=7,
                                        opacity=0.5,
                                        asFigure=True,
                                        xTitle='date',
                                        yTitle='USD sales price per SF',
                                        title='monthly USD sales price per SF of treehouse condos')
    fig.write_image(filename, scale=3)


    # look at all condos
    condos = all_data_cln[all_data_cln['Subdiv Desc'].str.contains('CONDO')]
    # some very high price per SF, must be a mistake or something
    condos = condos[condos['price per SF'] < 1500]
    condo_med = condos.groupby([condos.index.year, condos.index.month]).median()
    flat_df = flatten_multiindex(condo_med)
    filename = 'images/summit_co_condo_price_per_sf.png'
    fig = flat_df['price per SF'].iplot(kind='scatter',
                                        mode='lines+markers',
                                        size=7,
                                        opacity=0.5,
                                        asFigure=True,
                                        xTitle='date',
                                        yTitle='USD sales price per SF',
                                        title='monthly USD sales price per SF of Summit County condos')
    fig.write_image(filename, scale=3)

    # plot number of sales
    filename = 'images/summit_co_condo_number_of_sales.png'
    condo_count = condos.groupby([condos.index.year, condos.index.month]).count()
    flat_df = flatten_multiindex(condo_count)
    fig = flat_df['price per SF'].iplot(kind='scatter',
                                        mode='lines+markers',
                                        size=7,
                                        opacity=0.5,
                                        asFigure=True,
                                        xTitle='date',
                                        yTitle='number of sales',
                                        title='number of Summit County condo sales by month')
    fig.write_image(filename, scale=3)