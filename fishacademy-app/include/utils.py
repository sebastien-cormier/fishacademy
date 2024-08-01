import pandas as pd

def to_euro(_val) :
	"""
	Convert float value to monetary displayable string (EUR)
	"""
	return "{:.2f} €".format(_val).replace('.',',')


def serie_to_euro_format(_serie) :
	"""
	Convert a whole Pandas series to displayable EUR format
	"""
	return _serie.apply(lambda x : to_euro(x)) 


def convert_series_to_date(_series) :
	"""
	Convert Pandas series to datetime 
	"""
	return pd.to_datetime(_series, format = '%d/%m/%Y %H:%M:%S', dayfirst = True)

