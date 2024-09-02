import pandas as pd

import dateutil.parser

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

def serie_reformat_isodate(_serie, _format='%x') :
	"""
	Format from an iso format to another format
	"""
	_tmp_serie = _serie.apply(lambda x : dateutil.parser.isoparse(x))
	return _tmp_serie.apply(lambda x : x.strftime(_format)) 

def convert_series_to_date(_series) :
	"""
	Convert Pandas series to datetime 
	"""
	return pd.to_datetime(_series, format = '%d/%m/%Y %H:%M:%S', dayfirst = True)

