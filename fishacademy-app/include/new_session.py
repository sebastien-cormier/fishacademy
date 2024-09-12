import os
import pandas as pd

from datetime import datetime 
from include.app_config import *
from pathlib import Path

def save_shopping(_session, _shopper, _list_players, _contribution) :
    
    total_amount_ = len(_list_players) * _contribution

    df_ = pd.DataFrame(
        {
            '@timestamp': datetime.now(),
            'session': _session,
            'player': _shopper, 
            'tx_type': 'COURSES',
            'amount': round(total_amount_,2)
        }
        , index=[0])
    
    for p in _list_players :
        new_row_ = pd.DataFrame(
            {
                '@timestamp': datetime.now(),
                'session': _session,
                'player': p, 
                'tx_type': 'REPAS',
                'amount': -round(_contribution,2),
                'beneficiary': _shopper,
            }
            , index=[0])
        df_ = pd.concat([df_.loc[:],new_row_]).reset_index(drop=True)
    
    save_draft_csv(df_)
    return df_


def save_recave(_df, _session_name, _user, _amount) :
    new_row_ = pd.DataFrame(
        {
            '@timestamp': datetime.now(),
            'session': _session_name,
            'player': _user, 
            'tx_type': 'BUY_CHIPS',
            'amount': -round(_amount,2)
        }
        , index=[0])
    res_ = pd.concat([_df.loc[:],new_row_]).reset_index(drop=True)
    save_draft_csv(res_)
    return res_


def save_chips_return(_df, _session_name, _user, _amount) :
    new_row_ = pd.DataFrame(
        {
            '@timestamp': datetime.now(),
            'session': _session_name,
            'player': _user, 
            'tx_type': 'SELL_CHIPS',
            'amount': round(_amount,2)
        }
        , index=[0])
    res_ = pd.concat([_df.loc[:],new_row_]).reset_index(drop=True)
    save_draft_csv(res_)
    return res_

def backup_draft_csv(_df_session) :
    """
    Create a backup copy of the draft
    """
    filename_ = CSV_SESION_BACKUP_FILE.replace('<DATE>',datetime.now().strftime('%Y-%m-%d_%H%M%S'))
    _df_session.to_csv(filename_, sep=',', encoding='utf-8')


def load_draft_csv() :
     if Path(CSV_CURRENT_SESSION).is_file() :
        df_ = pd.read_csv(CSV_CURRENT_SESSION, 
                        usecols = ['@timestamp', 'session', 'player', 'tx_type', 'amount', 'beneficiary'],
                        dtype = {
                                '@timestamp' : str,
                                'session': str,
                                'player': str,
                                'tx_type': str,
                                'amount': float,
                                'beneficiary': str
                            })
        #df_['@timestamp2'] = pd.to_datetime(df_['@timestamp']).dt.strftime('%Y-%m-%dT%H:%M:%SZ')
        df_['@timestamp'] = pd.to_datetime(df_['@timestamp'])
        return df_
     else :
         return None

def save_draft_csv(_df_session) :
    _df_session.to_csv(CSV_CURRENT_SESSION, sep=',', encoding='utf-8')
    return _df_session.shape[0]

def delete_draft_csv() :
    os.remove(CSV_CURRENT_SESSION)

