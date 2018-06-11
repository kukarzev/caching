import logging
import pandas as pd
import os
from inspect import getcallargs
from inspect import signature
from hashlib import md5



def csv_hash(f, *args, **kwargs):
    '''
    Simple hash key function.
    Creates a name for a CSV file to cache pandas dataframe into.
    Uses function name + all function arguments and their values 
    to create md5 hash.
    '''
    cache_name = '{}'.format(f.__name__)
        
    # recover key-values for all args to use as cache key
    ba = signature(f).bind(*args,**kwargs)
    ba.apply_defaults()
    
    #print(ba.arguments)
    arg_string = ''
    for a in ba.arguments.items():
        arg_string += '{}{}'.format(a[0],a[1])
    _hash = md5(arg_string.encode()).hexdigest()
        
    cache_name += '__{}.csv'.format(_hash)

    return(cache_name)


def cache_dataframe(hash_function,
                    location='./',
                    logger=None):
    '''
    Decorator to make caching of data frames easier and standardized.
     - hash_function - function that will produce cache file name from call signature
     - location - path to directory, default if not specified
     - logger - will create default if not specified
    '''
    
    if logger is None:
        logger= logging.getLogger()

    def cache_dataframe_decorator(f):
        def wrapper(*args, **kwargs):

            cache_name = hash_function(f, *args, **kwargs)
            
            assert(os.path.isdir(location))
                        
            
            # debug
            #logger.debug('cache name: '+cache_name)
            
            cache_path = '{}/{}'.format(location.rstrip('/'),cache_name)
            if os.path.exists(cache_path):
                # if cache exists, read from cache
                logger.info('reading from cache: {}...'.format(cache_path))
                _df=pd.read_csv(cache_path)
            else:
                # run and cache if the output is data frame
                _df = f(*args, **kwargs)
                assert(isinstance(_df,pd.DataFrame))
                logger.info('writing cached version to {}...'.format(cache_path))
                _df.to_csv(cache_path, index=False)
                
            return(_df)

        return(wrapper)
    return(cache_dataframe_decorator)
