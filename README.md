# Apply Semtimental Analysis on financial documents to get sentimental score

## Introduction
Automatically collected the financial documents online then filtered out nouns and state verbs. Used LDA model classify nouns to several
themes then used state verbs to calculate sentimental score by sentimental analysis. Sentimental score can be standardize to sentimental 
index to improve the accuracy of stock price index prediction (Y.T.Liou, [Research of Applying Sentimental Analysis on Financial Documents to Predict Taiwan Electronic Sub-Index Trend](http://handle.ncl.edu.tw/11296/ndltd/04177084310486352052), 2015).

## Data Pre-processing
Used Python Library Beautifulsoup4.2 develope crawlers to collect industry news, enterprise announcements and annual reports automatically from financial websites. Used the regilar expresstions to filter irrelevant information and garbled text. Used Jieba library to tokenized contents and filter out nouns and status verbs according its Term Frequency and Inversed Documents Frequency.
+   crawlercnyes
+   crawlerTE
+   crawlermops
+   termfilter

## Data Classification
Used Latent Dirichlet allocation models classify the data to several topics. LDA controls the probability distribution through the hyper-parameter α and β. α controls the probability distribution of topic in documents, and β controls the probability distribution of words in topics. Researchers could adjust the α and β to get the perplexities and find out the number of topics. After that LDA uses the Gibbs sampling and iterative computing to calculate the probability of words in topics to find out the words belong to which topic.
+   lda_classification

## Calculating Sentimental Score
Seperated status verbs to positive verbs and nagetive verbs according to the sentimentle dictionary of finance which revised by NTUSD. It gets 1 point if it shows in the positive words set. On the other hand, it gets -1 point if it shows in the negative word set. Then summary the points to get the setimental scores.
+   cal_sentimentalscore

## The Correlation of Stock Price Index and Sentimental Score
Computed the cosine similarity of stock price index and sentimental score to prove there is a strong correlation. The result shows that the cosine similarity between tock price index and sentimental score is 0.985. Also, used Tableau to draw the trend line to show its similarity.
![alt text](https://raw.githubusercontent.com/eric80116/SAonFinancialArticles/correlation_graph.png)


