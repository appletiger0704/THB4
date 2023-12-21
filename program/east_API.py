# -*- coding: utf-8 -*-
"""
Created on Wed Dec 20 14:44:58 2023

@author: User
"""

import pandas as pd 
from datetime import datetime, timedelta
import os 

now = datetime.now()
yday = now - timedelta(days = 1)
today = now.strftime("%Y%m%d")
yesterday = yday.strftime("%Y%m%d")

path = rf"C:\Users\User\Desktop\East_auto\yday_accumulate\{today}"

if os.path.exists(path):
    
    os.chdir(path)
    
else:
    
    os.mkdir(path)
    os.chdir(path)
    
url = "https://opendata.cwa.gov.tw/api/v1/rest/datastore/O-A0002-001?Authorization=rdec-key-123-45678-011121314"

raw_data = pd.read_json(url)
station = raw_data.records.Station


station_id = [
    {'stat_id' : 'C1U840', 'precip' : None},  # 東澳嶺
    {'stat_id' : 'C0U760', 'precip' : None},  # 東澳
    {'stat_id' : 'C0UA60', 'precip' : None},  # 樟樹山
    {'stat_id' : 'C1U850', 'precip' : None},  # 觀音海岸
    {'stat_id' : 'C0T9D0', 'precip' : None},  # 和中
    {'stat_id' : 'C0Z310', 'precip' : None},  # 清水斷崖
    {'stat_id' : 'C0T790', 'precip' : None},  # 大禹嶺
    {'stat_id' : 'C1T810', 'precip' : None},  # 慈恩
    {'stat_id' : 'C1T830', 'precip' : None},  # 布洛灣
    {'stat_id' : 'C1S850', 'precip' : None},  # 豐南
    {'stat_id' : '21U110', 'precip' : None},  # 池端
    {'stat_id' : '01U060', 'precip' : None},  # 梵梵(2)
    {'stat_id' : 'C1U501', 'precip' : None},  # 牛鬥
    {'stat_id' : 'C0U720', 'precip' : None},  # 南山
    {'stat_id' : 'C1U920', 'precip' : None},  # 思源
    {'stat_id' : 'C0U520', 'precip' : None},  # 雙連埤
    {'stat_id' : 'C0T9H0', 'precip' : None},  # 加路蘭山
    {'stat_id' : 'C0T9I0', 'precip' : None},  # 豐濱
    {'stat_id' : 'C0U770', 'precip' : None},  # 南澳
    {'stat_id' : 'C1T800', 'precip' : None},  # 洛韶
    {'stat_id' : '01T9L0', 'precip' : None}   # 東富
    ]


for id_s in station_id:
    
    for stat in station:
        
        if id_s["stat_id"] == stat["StationId"]:
            
            now_prep = stat["RainfallElement"]["Now"]["Precipitation"]
            yday_prep = stat["RainfallElement"]["Past2days"]["Precipitation"]
            id_s["precip"] = yday_prep - now_prep
            
            
road_station = {"C1U840" : None,             # 東澳嶺
                "C0U760、C0U770" : None,     # 東澳、南澳
                "C1U850、C0UA60" : None,     # 觀音海岸、樟樹山
                "C0T9D0、C0Z310" : None,     # 和中、清水斷崖
                "C0T790" : None,             # 大禹嶺
                "C1T810、C1T800" : None,     # 慈恩、洛韶
                "C1T830" : None,             # 布洛灣
                "C1S850" : None,             # 豐南
                "21U110、01U060" : None,     # 池端、梵梵(2)
                "C1U501、01U060" : None,     # 牛鬥、梵梵(2)
                "C0U720" : None,             # 南山
                "C1U920、C0U720" : None,     # 思源、南山
                "C0U520" : None,             # 雙連埤
                "C0T9H0" : None,             # 加路蘭山
                "01T9L0、C0T9I0" : None,     # 東富、豐濱
    }

def compare(first, second):
    
    rainfall = 0
    
    for i in station_id:
        
        if i["stat_id"] == first or i["stat_id"] == second:
            
            if i["precip"] == None or i["precip"] >= rainfall:
                
                rainfall = i["precip"]
                
    return rainfall
            

def insert_value():
    
    for i in road_station:
        
        for stat in station_id:
            
            if i == stat["stat_id"]:
                
                road_station[i] = stat["precip"]
        
        if i == "C0U760、C0U770":
            
            road_station[i] = compare("C0U760", "C0U770")
            
        elif i == "C1U850、C0UA60":
            
            road_station[i] = compare("C1U850", "C0UA60")
            
        elif i == "C0T9D0、C0Z310":
            
            road_station[i] = compare("C0T9D0", "C0Z310")
            
        elif i == "C1T810、C1T800":
            
            road_station[i] = compare("C1T810", "C1T800")
            
        elif i == "21U110、01U060":
            
            road_station[i] = compare("21U110", "01U060")
            
        elif i == "C1U501、01U060":
            
            road_station[i] = compare("C1U501", "01U060")
            
        elif i == "C1U920、C0U720":
            
            road_station[i] = compare("C1U920", "C0U720")
            
        elif i == "01T9L0、C0T9I0":
            
            road_station[i] = compare("01T9L0", "C0T9I0")
            
insert_value()

data_list = []
index_list = []

for i in road_station:
    
    index_list.append(i)
    data_list.append(road_station[i])
    
data = pd.DataFrame(data_list, index = index_list, columns = ["昨日累積雨量"])

data.to_csv(f"{yesterday}_累積雨量.csv", encoding = "big5")
