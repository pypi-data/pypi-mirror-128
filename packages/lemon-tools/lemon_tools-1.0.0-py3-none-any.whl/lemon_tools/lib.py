# -*- coding: utf-8 -*-

from os.path import abspath
from os.path import dirname
import pandas as pd

def get_data():
    """ Create data
    """
    return "a lot of data"

def clean_data(data):
    """ clean data
    """
    return data.upper()

def make_result(df, filename):
    """ write output result in filename
    """
    df.drop(["datatime", "timestamp", "score_value"], axis=1, inplace=True)
    df["player"] = df.player.str.upper()
    df.to_csv(filename)
    print(" {} Made")
    
if __name__ == '__main__':
    # for introspection purposes to quickly get this functions on ipython
    # with data
    import lemon_tools
    
    datapath = dirname(abspath(lemon_tools.__file__)) + "/data"
    data = "{}/data.csv".format(datapath)
    df = pd.read_csv(data)
    data = get_data()
    clean_data = clean_data(data)
    print("df, data and clean_data made")