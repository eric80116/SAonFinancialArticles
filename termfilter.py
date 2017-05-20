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
from polarity import findpolarity 

#------connect DB----------
db = MySQLdb.connect("ip","account","password","dbname" )
db.set_character_set('utf8')

#---------get content-------------------
cursor = db.cursor()

sql="SELECT content FROM textinfo;"
cursor.execute(sql)
results = cursor.fetchall()
content=[]
for row in results:
 content.append(row[0])

#---------article tokenize----------
articleaftertoken=[]
#---------filter terms based on part of speech----------
for i in range(1,5):
    words=pseg.cut("\""+content[i]+"\"") 
    string=""
    for key in words:
        if(key.flag=="n"):
        #if(key.flag=="n"or key.flag=="v" or key.flag=="vn" or key.flag=="a"):   
            #print(str(key.word.encode('utf-8')))
            string=string+" "+str(key.word.encode('utf-8'))
    articleaftertoken.append(string)
    
    
#------------------------- calculated tfidf-----------------------
if __name__ == "__main__":  
    vectorizer=CountVectorizer()  
    transformer=TfidfTransformer() 
    tfidf=transformer.fit_transform(vectorizer.fit_transform(articleaftertoken))  
    word=vectorizer.get_feature_names()  
    weight=tfidf.toarray()
    
    for i in range(len(weight)):
        print u"-------no",i,u"--tf-idf------"  
        for j in range(len(word)):  
            print word[j],weight[i][j]




    

         
  






