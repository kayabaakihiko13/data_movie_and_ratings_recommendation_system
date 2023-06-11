from pandas import read_csv
import pandas as pd

def dataset(url:str)-> pd.DataFrame :
    load_csv=read_csv(url,dtype=str)
    return load_csv
    