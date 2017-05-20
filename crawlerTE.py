# -*- coding: utf-8 -*-
#-----crawler for url-----
import urllib2
import re
import MySQLdb
from bs4 import BeautifulSoup
import csv
import os

#---------connect DB----------------
db = MySQLdb.connect("ip","account","password","dbname" )
db.set_character_set('utf8')




#--------get all files from folders-------------
for root, dirs, files in os.walk("D://data/te/test/"):
    print("")



#--------load files-------------
TEdate=[]
TE=[] 
for i in range(len(files)):
    f = open('D://data/te/test/'+files[i], 'r')  
    for j in csv.DictReader(f, ["日期", "電子類指數"]):  
        TEdate.append(j["日期"].replace(j["日期"][0:3], str(2014)))
        TE.append(j["電子類指數"])
    
    for k in range(len(TEdate)):
        
#---------insert DB----------------
        print(TEdate[k])
        print(TE[k])
        sql = "INSERT INTO teinfo(date, price) VALUES ('"+TEdate[k]+"','"+TE[k]+"')"
        cursor = db.cursor()
        cursor.execute(sql)
        db.commit()
    del TEdate[:]
    del TE[:]
f.close() 