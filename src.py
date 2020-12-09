import json
import requests
import re
import pytz
# import pandas as pd
from datetime import datetime


def board_main(board,creds):
    r = requests.get(f'https://api.trello.com/1/boards/{board}?cards=visible',params=creds)
    return r.json() 

def board_data(board,category,creds):
    r = requests.get(f'https://api.trello.com/1/boards/{board}/{category}',params=creds)
    return r.json() 

def card_dt(card_id):
    creation_time = datetime.fromtimestamp(int(card_id[0:8],16))
    utc_creation_time = pytz.utc.localize(creation_time)
    r = str(utc_creation_time)[0:19]
    return r

def date_last(value):
    matched = re.search('\d\d\d\d-\d\d-\d\d\w\d\d:\d\d:\d\d',value)
    values = matched.group()
    values = values.replace('T',' ')
    return values

def lst_name(value,lists_lst):
    return list(filter(lambda lst: lst['id'] == value, lists_lst))[0]['name']

def get_points(value):
    try:
        value = ''.join(value.split())
        pattern = re.compile(r"\((\d+)\)")
        points = pattern.findall(value)[0]
        return int(points)
    except Exception:
        pass
        return 0

def card_mov_simple(card_id,creds):
    r = requests.get(f'https://api.trello.com/1/cards/{card_id}/actions',params=creds)
    v = r.json()
    lst_movs = list()
    for i in v:
        lst_movs.append(i)
    return lst_movs

def card_dict(lst):
    mydic = {}
    
    for l in reversed(lst):
        if l['type'] == 'updateCard':
            mydic[l['data']['listAfter']['name']] = card_dt(l['id'])
       
    mydic['Name'] = (l['data']['card']['name'])
    mydic['Points'] = get_points(l['data']['card']['name'])
    mydic['CreatedOn'] = card_dt(l['data']['card']['id'])
    mydic['ShortLink'] = 'https://trello.com/c/'+l['data']['card']['shortLink']
    return mydic
    
