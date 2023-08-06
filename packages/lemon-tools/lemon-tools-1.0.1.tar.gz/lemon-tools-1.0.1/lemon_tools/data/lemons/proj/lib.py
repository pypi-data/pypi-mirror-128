# -*- coding: utf-8 -*-
""" Main lib for proj Project
"""

from os.path import split
import pandas as pd
import datetime

pd.set_option('display.width', 200)

def clean_data(data):
    """ clean data
    """
    # remove colums starts with vote
    cols = [x for x in data.colums if x.find('vote') >= 0]
    data.drop(cols, axis=1, inplace=True)
    # remove special characters from columns
    data.loc[:, 'civility'] = data['civility'].replace('\.', '', regex=True)
    # calculate age from day of birth
    actual_year = datetime.datetime.now().year
    data.loc[:, 'Year_Month'] = pd.to_datetime(data.birthdate)
    data.loc[:, 'Age'] = actual_year - data['Year_Month'].dt.year
    # uppercase variable to avoid duplicates
    data.loc[:, 'city'] = data['city'].str.upper()
    # take 2 first digits, 2700 -> 02700 so first two are region
    data.loc[:, 'postal_code'] = data.postal_code.str.zfill(5).str[0:2]
    # remove columns with more than 50% of nans
    cnans = data.shape[0] / 2
    data = data.dropna(thresh=cnans, axis=1)
    # remove rows with more than 50% of nans
    rnans = data.shape[1] / 2
    data = data.dropna(thresh=rnans, axis=0)
    # discretize based on quantiles
    data.loc[:, 'duration'] = pd.qcut(data['surveyduration'], 10)
    # discretize based on values
    data.loc[:, 'Age'] = pd.cut(data['Age'], 10)
    # rename columns
    data.rename(columns={'q1': 'Frequency'}, inplace=True)
    # transform type of columns
    data.loc[:, 'Frequency'] = data['Frequency'].astype(int)
    # rename values in rows
    drows = {1: 'Manytimes', 2: 'Onetimebyday', 3: '5/6timesforweek',
             4: '4timesforweek', 5: '1/3timesforweek', 6: '1timeformonth',
             7: '1/trimestre', 8: 'Less', 9: 'Never'}
    data.loc[:, 'Frequency'] = data['Frequency'].map(drows)
    return data

if __name__ == '__main__':
    # for introspection purposes to quickly get this functions on ipython
    import proj
    folder_source, _ = split(proj.__file__)
    df = pd.read_csv('{}/data/data.csv.gz'.format(folder_source))
    clean_data = clean_data(df)
    print(' dataframe cleaned')