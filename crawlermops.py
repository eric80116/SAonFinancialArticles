#encoding=utf-8
#-----crawler for url-----
import urllib2
import re
import MySQLdb
from bs4 import BeautifulSoup
import time
import bs4



#---------connect DB----------------
db = MySQLdb.connect("127.0.0.1","root","xu.6u4wu/6","finance" )
db.set_character_set('utf8')
co_id=[2439,2440,2441,2442,2443,2444,2448,2449,2450,2451,2453,2454,2455,2456,2457,2458,2459,2460,2461,2462,2464,2465,2466,2467,2468,2471,2472,2474,2475,2476,2477,2478,2480,2481,2482,2483,2484,2485,2486,2488,2489,2491,2492,2493,2495,2496,2497,2498,2499,3002,3003,3005,3006,3008,3010,3011,3013,3014,3015,3016,3017,3018,3019,3021,3022,3023,3024,3025,3026,3027,3028,3029,3030,3031,3032,3033,3034,3035,3036,3037,3038,3040,3041,3042,3043,3044,3045,3046,3047,3048,3049,3050,3051,3054,3055,3057,3058,3059,3060,3062,3090,3094,3130,3149,3189,3209,3229,3231,3257,3296,3305,3308,3311,3312,3315,3338,3356,3376,3380,3383,3406,3416,3419,3432,3437,3443,3450,3454,3474,3481,3494,3501,3504,3514,3515,3518,3519,3532,3533,3535,3545,3550,3557,3559,3561,3573,3576,3579,3583,3584,3588,3591,3593,3596,3598,3605,3607,3617,3622,3645,3653,3661,3665,3669,3673,3679,3682,3686,3694,3698,3701,3702,3704,3706,4904,4906,4915,4916,4919,4934,4935,4938,4942,4952,4956,4958,4960,4976,4977,4984,4994,4999,5203,5215,5225,5234,5243,5259,5264,5269,5285,5305,5388,5434,5469,5471,5484,6108,6112,6115,6116,6117,6120,6128,6131,6133,6136,6139,6141,6142,6145,6152,6153,6155,6164,6165,6166,6168,6172,6176,6183,6189,6191,6192,6196,6197,6201,6202,6205,6206,6209,6213,6214,6215,6216,6224,6225,6226,6230,6235,6239,6243,6251,6257,6269,6271,6277,6278,6281,6282,6283,6285,6286,6289,6405,6409,6412,6414,6415,6422,6431,6449,6451,8011,8016,8021,8039,8046,8070,8072,8081,8101,8103,8105,8110,8112,8114,8131,8150,8163,8201,8210,8213,8215,8249,8261,8271,9912]

#---------get content----------------
for q in range(len(co_id)):
    print(co_id[q])
    crawerurl= "http://mops.twse.com.tw/mops/web/ajax_t05st01?SourceencodeURIComponent=1&step=1&firstin=1&off=1&keyword4=&code1=&TYPEK2=&checkbtn=&queryName=co_id&TYPEK=all&co_id="+str(co_id[q])+"&year=103&month=&b_date=&e_date="
    response = urllib2.urlopen(crawerurl)
    html = response.read()
    soup= BeautifulSoup(html)
    
    seq_no=[]
    spoke_date=[]
    spoke_time=[]
    
    date=[]
    timedb=[]
    title=[]
    content=[]
    
    
#---------used regular expression to filter useless info----------------    
    m = re.findall("(\d{3}.\d{2}.\d{2})", html)
    for i in range(len(m)):
        date.append(m[i].replace("103","2014"))   
        spoke_date.append(m[i].replace("/", "").replace("103","2014"))
    
    m1= re.findall("(\d{2}:\d{2}:\d{2})", html)
    for j in range(len(m1)):   
        timedb.append(m1[j])
        spoke_time.append(m1[j].replace(":", ""))
        
    m2= re.findall("seq_no.value='(\d+)'", html)  
    for k in range(len(m2)):   
        seq_no.append(m2[k])  
    
    ss=[]
    print(len(m))
    
    for l in range(min([len(m),len(spoke_time),len(seq_no)])):
        print(l)
        ss.append(l)
        crawlercontent= "http://mops.twse.com.tw/mops/web/t05st01?encodeURIComponent=1&firstin=true&b_date=&e_date=&TYPEK=sii&year=103&month=all&type=&co_id="+str(co_id[q])+"&spoke_date="+spoke_date[l]+"&spoke_time="+spoke_time[l]+"&seq_no="+seq_no[l]+"&e_month=all&step=2&off=1"
        print(crawlercontent)
        
        response1 = urllib2.urlopen(crawlercontent)
        print(response1)
        html1 = response1.read()
        soup1= BeautifulSoup(html1)
        url=soup1.find_all("pre")
        
        if(len(url)!=0):
            print(url[0].string)
            #print(url[1].string)
        
            title.append(url[0].string)
            content.append(url[1].string)
        time.sleep(3)
    
    
    
    #---------insert DB----------------
    for p in range(len(title)):
        print(p)
        
        #print(date[p])
        #print(timedb[p])
        sql = "INSERT INTO textinfo(title,content,date,time,source,type) VALUES('"+title[p]+"','"+content[p]+"','"+date[ss[p]]+"','"+timedb[ss[p]]+"','mops','importantnews')"
        cursor = db.cursor()
        cursor.execute(sql)
        db.commit()