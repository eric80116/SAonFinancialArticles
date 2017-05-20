
#----crawler for content-----
import urllib, urllib2
import requests
import MySQLdb

from bs4 import BeautifulSoup

#---------connect DB----------------
db = MySQLdb.connect("ip","account","password","dbname" )
db.set_character_set('utf8')


for n in range(6, 10):
 crawerurl= "http://news.cnyes.com/search.aspx?q=%E5%8F%B0%E7%A9%8D%E9%9B%BB&D=7&P="+str(n)+"&1=1"
 print(crawerurl)
 response1 = urllib2.urlopen(crawerurl)
 html1 = response1.read()
 soup1= BeautifulSoup(html1)

#---------get url-------------------
url=soup1.find_all("a")
print(url)
for i in range(len(url)):
 if (url[i].get('href').find("2")==1):
  url_list.append(url[i])

#----------get content-----------

for j in range(261,len(url_list)+1):
 response = urllib2.urlopen(urllib.quote(url_list[j], ":?=/"))
 html = response.read()
 soup = BeautifulSoup(html)
#title
 title = soup.title.string
 
#time
 time= soup.find('div',attrs={'class':"info"})#.get_text().split()
 if(time!=None):
  time1=time.get_text().split()


#content

 paragraph = soup.find_all(id='newsText')
 paragraph = soup.select("div#newsText > p")

 content=""
 for i in range(0,len(paragraph)):
  content=content+paragraph[i].get_text()
 print content

#-----insert to DB----------

 sql1 = "INSERT INTO news(title,content,date,time) VALUES ('"+title+"',"+"'"+content+"',"+"'"+time1[2]+"',"+"'"+time1[3]+"')"
 cursor.execute(sql1)
db.commit()


