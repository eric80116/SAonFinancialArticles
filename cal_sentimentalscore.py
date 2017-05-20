#encoding=utf-8
import jieba
import MySQLdb
import urllib, urllib2
import jieba.posseg as pseg  
import jieba.analyse
import os  
import sys  
from sklearn import feature_extraction  
from sklearn.feature_extraction.text import TfidfTransformer  
from sklearn.feature_extraction.text import CountVectorizer
import polarity
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import xlwt
 
#------connect DB----------
db = MySQLdb.connect("ip","account","password","dbname" )
db.set_character_set('utf8')

#---------get content-------------------
cursor = db.cursor()
sql = "SELECT date FROM textinfo WHERE (date>='startdate' and date<='enddate') GROUP bY date ORDER BY date;"
cursor.execute(sql)
results = cursor.fetchall()
contentdate=[]
for row in results:
 contentdate.append(row[0])


#---------sort content by date------
cursor1 = db.cursor()
combine=""
combine_content=[]
for i in range(len(contentdate)):
    sql1="SELECT content FROM textinfo WHERE date='"+str(contentdate[i])+"'"
    cursor1.execute(sql1)
    results1 = cursor1.fetchall()
    for row in results1:
        combine=combine+row[0]
    combine_content.append(combine)
    combine=""
    
#--------got verb from contents---------------
stopwords=[]
for i in open('D://dictionary/stop_words.txt'):
    stopwords.append(str(i))
articleaftertoken=[]
for j in range(len(combine_content)):
    words=pseg.cut("\""+combine_content[j]+"\"")
    string="" 
    for key in words:
        if(key.flag=="v" or key.flag=="vn"):
            if(stopwords[0].find(str(key.word.encode('utf-8')))==-1):
                string=string+" "+str(key.word.encode('utf-8'))
    articleaftertoken.append(string)

   
#--------tokenization------------
term=[]  
storecontent=[]
term_num=[]
for m in range(len(articleaftertoken)): 
    storecontent.append(articleaftertoken[m]) 
    if __name__ == "__main__":  
        vectorizer=CountVectorizer()  
        transformer=TfidfTransformer() 
        tfidf=transformer.fit_transform(vectorizer.fit_transform(storecontent))  
        word=vectorizer.get_feature_names() 
        term_num.append(len(word)) 
        weight=tfidf.toarray() 
        
        for k in range(len(weight)):  
            for l in range(len(word)):
                term.append((m+1,word[l])) #(which content, term)
        del storecontent[:]
            
        
#-------calculate the sentimental score--------------
score_sum=0
pos_num=0
neg_num=0
content_score=[]

for x in range(1,len(articleaftertoken)+1):
    
    for y in range(len(term)):
        if(term[y][0]==x):
            score_sum=score_sum+polarity.findpolarity(term[y][1])
            if(polarity.findpolarity(term[y][1])==1):
                pos_num=pos_num+1
            if(polarity.findpolarity(term[y][1])==-1):
                neg_num=neg_num+1
    content_score.append(float(score_sum)/float(term_num[x-1]))
    score_sum=0

#------ export the result file-------------------

file = xlwt.Workbook()
table = file.add_sheet('test')
for w in range(len(content_score)):
    table.write(0,w,contentdate[w])
    table.write(1,w,content_score[w])
file.save('C://Users/liouyt/Desktop/demo09101112-3.xls')
print("finish")

    

         

    