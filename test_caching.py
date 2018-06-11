#!/usr/bin/env python
import pandas as pd
import logging
from caching import cache_dataframe
from caching import csv_hash



@cache_dataframe(csv_hash)
def create_dataframe(dummy='a'):
    df = pd.DataFrame({'col_A': [1,2,3,4,5],
                       'col_B': [dummy for x in range(5)]})
    return(df)

if __name__ == "__main__":

    # logger for convenience
    logger = logging.getLogger()
    ch = logging.StreamHandler()
    formatter = logging.Formatter('%(asctime)s - %(name)s.%(funcName)s - %(levelname)s - %(message)s')
    ch.setFormatter(formatter)
    logger.addHandler(ch)
    logger.setLevel(logging.INFO)


    # demo

    # default arguments
    df1 = create_dataframe()
    print(df1)

    # positional argument
    df2 = create_dataframe('b')
    print(df2)

    # keyword argument (same as default)
    df3 = create_dataframe(dummy = 'a')
    print(df3)

    
