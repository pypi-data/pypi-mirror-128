from sqlite3.dbapi2 import Connection, Cursor
from requests.models import Response
from .DateTime import DateTime
from .ExObject import ExObject
from urllib.parse import urlencode
import time
import requests
import sys
import os
import json
import datetime
import sqlite3
data_dict=None
def _get(url)->Response:
    response=None
    for i in range(0, 3):
        try:
            # r = requests.post(url,data=json.dumps(params), headers={"Content-Type": "application/json"}, timeout=5)
            response = requests.get(url,timeout=5)
            break
        except:
            time.sleep(1)
            pass
    return response

def _create_dblite(cursor:Cursor):
    sql='''
        CREATE TABLE IF NOT EXISTS stock_price(
        code TEXT NOT NULL,
        dt TEXT NOT NULL,
        open NUMERIC NULL DEFAULT NULL,
        close NUMERIC NULL DEFAULT NULL,
        high NUMERIC NULL DEFAULT NULL,
        low NUMERIC NULL DEFAULT NULL,
        volume NUMERIC NULL DEFAULT NULL,
        amount NUMERIC NULL DEFAULT NULL,
        amplitude NUMERIC NULL DEFAULT NULL,
        zdf NUMERIC NULL DEFAULT NULL,
        zde NUMERIC NULL DEFAULT NULL,
        turnover NUMERIC NULL DEFAULT NULL,
        PRIMARY KEY (code,dt))
    '''
    cursor.execute(sql)

def _to_sqlite(cursor,table,data):
    dbItem=data
    params=[]
    for key in dbItem:
        params.append(dbItem[key])
    sql=f"INSERT OR IGNORE INTO {table} ({','.join(dbItem.keys())}) VALUES ({','.join(['?' for i in range(len(dbItem.keys()))])}) "

    # sql+="ON DUPLICATE KEY UPDATE "
    # for key in dbItem:
    #     if key in ["code","dt"]:
    #         continue
    #     if dbItem[key]:
    #         sql+= key+"=?,"
    #         params.append(dbItem[key])
    #sql=sql[:-1]+";"
    cursor.execute(sql,params)

def get_holiday_from_api(year=None):
    if not year:
        year=DateTime.Now().Year
    url="http://timor.tech/api/holiday/year/"+str(year)
    result=[]
    data=None
    for i in range(0, 3):
        try:
            # r = requests.post(url,data=json.dumps(params), headers={"Content-Type": "application/json"}, timeout=5)
            r = requests.get(url,timeout=5)
            data=r.json()
            break
        except:
            time.sleep(1)
            pass
    for key in data["holiday"]:
        if data["holiday"][key]["holiday"]:
            result.append(data["holiday"][key]["date"])

    return result

def get_holiday(year=None):
    global data_dict
    if not year:
        year=DateTime.Now().Year
    if not os.path.exists(".exobj"):
        os.mkdir(".exobj")
    if not os.path.exists(".exobj/exstock.json"):
        with open(".exobj/exstock.json","w",encoding='utf-8') as file:
            file.write("{}")
    
    if not data_dict:
        data_dict=json.loads(open(".exobj/exstock.json").read())

    holidays=data_dict.get(str(year))
    if not holidays:
        holidays=get_holiday_from_api(year)
        data_dict[str(year)]=holidays
        with open(".exobj/exstock.json","w+",encoding='utf-8') as file:
            file.write(json.dumps(data_dict))

    return holidays

def is_trading_day(dt)->bool:
    _dt=""
    if type(dt) is DateTime:
        _dt=dt.ToString('yyyy-MM-dd')
    elif type(dt) is datetime.datetime:
        _dt=dt.strftime('%Y-%m-%d')
    elif type(dt) is datetime.date:
        _dt=str(dt)
    elif type(dt) is str:
        _dt=DateTime.AutoConvert(dt).ToString('yyyy-MM-dd')
    else:
        raise Exception("UNSUPPORTED TYPE:"+str(type(dt)))

    if _dt in get_holiday():
        return False
    if DateTime.Convert(_dt,"yyyy-MM-dd").WeekDay>=6:
        return False
    return True

def get_next_trading_day(dt)->DateTime:
    _dt=None
    if type(dt) is DateTime:
        _dt=dt
    elif type(dt) is datetime.datetime:
        _dt=DateTime.Convert(dt.strftime('%Y-%m-%d'),"yyyy-MM-dd")
    elif type(dt) is datetime.date:
        _dt=DateTime.Convert(str(dt),"yyyy-MM-dd")
    elif type(dt) is str:
        _dt=DateTime.AutoConvert(dt).ToString('yyyy-MM-dd')
    
    if not _dt:
        raise Exception("UNSUPPORTED dt")

    while True:
        _dt=_dt.AddDays(1)
        if(is_trading_day(_dt)):
            return _dt.Date()

def get_last_trading_day(dt)->DateTime:
    _dt=None
    if type(dt) is DateTime:
        _dt=dt
    elif type(dt) is datetime.datetime:
        _dt=DateTime.Convert(dt.strftime('%Y-%m-%d'),"yyyy-MM-dd")
    elif type(dt) is datetime.date:
        _dt=DateTime.Convert(str(dt),"yyyy-MM-dd")
    elif type(dt) is str:
        _dt=DateTime.AutoConvert(dt).ToString('yyyy-MM-dd')
    
    if not _dt:
        raise Exception("UNSUPPORTED dt")

    while True:
        _dt=_dt.AddDays(-1)
        if(is_trading_day(_dt)):
            return _dt.Date()

def get_price_from_api(code,date=None):
    url=f"http://quote.eastmoney.com/{code}.html"
    _str=_get(url).text
    sec_id=ExObject.regexOne('nid=([0-9a-zA-Z\.]+)&',_str)
    if not sec_id:
        raise Exception("Get Price Failure!")
    url=f"http://46.push2his.eastmoney.com/api/qt/stock/kline/get?"
    params={
        "secid":sec_id,
        "fields1":"f1,f2,f3,f4,f5,f6",
        "fields2":"f51,f52,f53,f54,f55,f56,f57,f58,f59,f60,f61",
        "klt":"101",
        "fqt":"0",
        "end":"20500101" if not date else date.ToString("yyyyMMdd"),
        "lmt":"120"
    }
    url+=urlencode(params)
    data=_get(url).json()
    result=[]
    for line in data["data"]["klines"]:
        items=line.split(",")
        result.append(items)
    return result

def get_price_from_sqlite(cursor:Cursor,code:str,date:str,lang="en"):
    cursor.execute(f"SELECT * FROM stock_price WHERE code='{code}' AND dt='{date}' LIMIT 0,1")
    item=cursor.fetchone()
    if not item:
        return None
    result={}
    result["code"]=item[0]
    result["dt"]=item[1]
    result["open"]=item[2]
    result["close"]=item[3]
    result["high"]=item[4]
    result["low"]=item[5]
    result["volume"]=item[6]
    result["amount"]=item[7]
    result["amplitude"]=str(item[8])+"%"
    result["zdf"]=str(item[9])+"%"
    result["zde"]=item[10]
    result["turnover"]=str(item[11])+"%"
    
    if lang=="cn":
        _result={
            "代码":result["code"],
            "日期":result["dt"],
            "开盘":result["open"],
            "收盘":result["close"],
            "最高":result["high"],
            "最低":result["low"],
            "成交量":result["volume"],
            "成交额":result["amount"],
            "振幅":result["amplitude"],
            "涨跌幅":result["zdf"],
            "涨跌额":result["zde"],
            "换手率":result["turnover"],
        }
        return _result
    return result

def get_price(code,dt,lang="en"):
    _dt=""
    if type(dt) is DateTime:
        _dt=dt.ToString('yyyy-MM-dd')
    elif type(dt) is datetime.datetime:
        _dt=dt.strftime('%Y-%m-%d')
    elif type(dt) is datetime.date:
        _dt=str(dt)
    elif type(dt) is str:
        _dt=DateTime.AutoConvert(dt).ToString('yyyy-MM-dd')
    else:
        raise Exception("UNSUPPORTED TYPE:"+str(type(dt)))

    #判断是否存在SQLITE数据库
    if not os.path.exists(".exobj"):
        os.mkdir(".exobj")
    conn=None
    cursor=None
    if not os.path.exists(".exobj/price.db"):
        conn = sqlite3.connect(".exobj/price.db")
        cursor = conn.cursor()
        _create_dblite(cursor)
    else:
        conn = sqlite3.connect(".exobj/price.db")
        cursor = conn.cursor()
    
    result=get_price_from_sqlite(cursor,code,_dt,lang)
    if not result:
        code_sp=code.split(".")
        _datas=get_price_from_api(code_sp[1].lower()+code_sp[0],DateTime.Convert(_dt,"yyyy-MM-dd").AddDays(1))
        if not _datas:
            raise Exception("Get Price Failure!")
        for _data in _datas:
            dbItem={
                "code":code,
                "dt":_data[0],
                "open":_data[1],
                "close":_data[2],
                "high":_data[3],
                "low":_data[4],
                "volume":_data[5],
                "amount":_data[6],
                "amplitude":_data[7],
                "zdf":_data[8],
                "zde":_data[9],
                "turnover":_data[10],
            }
            _to_sqlite(cursor,"stock_price",dbItem)
        conn.commit()
        result=get_price_from_sqlite(cursor,code,_dt,lang)
    return result