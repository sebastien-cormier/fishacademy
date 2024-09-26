import pandas as pd

from include.app_config import *
from datetime import datetime
from zoneinfo import ZoneInfo

def now() :
	return datetime.now(ZoneInfo(DATE_ZONE_INFO))
			  
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

def serie_parse_elastic_date(_serie) :
	"""
	Format from an iso format to another format
	"""
	_tmp_serie = _serie.apply(lambda x : datetime.fromisoformat(x))
	_tmp_serie = _tmp_serie.apply(lambda x : x.astimezone(ZoneInfo(DATE_ZONE_INFO)))
	return _tmp_serie.apply(lambda x : get_str_datetime(x)) 

def convert_csv_series_to_date(_series) :
	"""
	Convert Pandas series to datetime 
	"""
	return pd.to_datetime(_series, format = '%d/%m/%Y %H:%M:%S', dayfirst = True)

def get_str_datetime(dt=now()) :
	return dt.strftime('%Y-%m-%d %H:%M:%S')