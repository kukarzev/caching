# Caching
A decorator for caching pandas dataframes returned by a function.

Takes a hash function as parameter. A simple csv_hash is included.

Usage:

	from caching import cache_dataframe
	from caching import csv_hash
	
	@cache_dataframe(csv_hash)
    def my_function(x,y,z):
		...
		df = pandas.DataFrame(...)
		...
		return(df)
