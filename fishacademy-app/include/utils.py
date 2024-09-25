import pandas as pd

import dateutil.parser
from datetime import datetime
from pytz import timezone

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

def serie_reformat_isodate(_serie, format='%x', target_tz="Europe/Paris") :
	"""
	Format from an iso format to another format
	"""
	_tmp_serie = _serie.apply(lambda x : dateutil.parser.isoparse(x))
	_tmp_serie = _tmp_serie.apply(lambda x : x.astimezone(timezone(target_tz)))
	return _tmp_serie.apply(lambda x : x.strftime(format)) 

def convert_csv_series_to_date(_series) :
	"""
	Convert Pandas series to datetime 
	"""
	return pd.to_datetime(_series, format = '%d/%m/%Y %H:%M:%S', dayfirst = True)

def get_datetime_paris() :
	return pytz.timezone("Europe/Paris").localize(datetime.now(), is_dst=None)

def get_str_datetime_paris() :
	return get_datetime_paris().strftime('%Y-%m-%d %H:%M:%S')