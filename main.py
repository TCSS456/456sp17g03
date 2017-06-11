# -*- coding: utf-8 -*-
import os
import pickle
import csv

from training import train, extract_features
from process_tweets import readTweetsFromFiles
from sklearn.naive_bayes import MultinomialNB, BernoulliNB
from sklearn.linear_model import LogisticRegression,SGDClassifier
from sklearn.svm import SVC, LinearSVC, NuSVC


feature_list = []

def main():
    #train and load classifier
    #arguments, "NB" (Naive Bayes) , "MNB" (Multi-Nomial Naive Bayes), 
    #           "BNB" (Benroulli Naive Bayes), "LSVC" (Linear SVC),
    #           "SGDC", 
    #           set 'removeStopwords = True' to remove stop words 
    classifierType = "LSVC"
    removeStopwords = False
    
    
    classifier = train(classifierType, removeStopwords)
    #get data from Twitter stream JSON resposne
    unclassified_data = readTweetsFromFiles(removeStopwords)
    classified_data = []
    for d in unclassified_data:
        text = extract_features(d[2])
        sentiment = classifier.classify(text)
        #print "SENTIMENT = " + sentiment + ": " + d[2]
        classified_data.append([d[0], d[1][:10], d[2].encode("utf-8"), sentiment])
    save_processed = open("processedSentiment.pickle", "wb")
    pickle.dump(classified_data, save_processed)
    save_processed.close()
    with open("processedTweets.csv", "wb") as f:
        writer = csv.writer(f)
        writer.writerows(classified_data)
    #final data consists of ['COMPANY', 'DATETIME', 'TWEET_ID', 'SENTIMENT']
    #take classified data by date/company and associate stock opening, high, closing price, and trading volume for each category
    dates = ['Thu May 25', 'Fri May 26', 'Sat May 27', 'Sun May 28', 'Mon May 29', 'Tue May 30', 'Wed May 31',
             'Thu Jun 01', 'Fri Jun 02', 'Sat Jun 03', 'Sun Jun 04', 'Mon Jun 05', 'Tue Jun 06', 'Wed Jun 07',
             'Thu Jun 08', 'Fri Jun 09', 'Sat Jun 10']
    dailyData = []
    google_tweets = {}
    apple_tweets = {}
    microsoft_tweets = {}
    for d in dates:
        google_tweets[d] = []
        apple_tweets[d] = []
        microsoft_tweets[d] = []

    for c in classified_data:
        cat=c[0]
        if cat == 'google':
            google_tweets[c[1]].append(c[3])
        elif cat == 'apple':
            apple_tweets[c[1]].append(c[3])
        elif cat == 'microsoft':
            microsoft_tweets[c[1]].append(c[3])
    for key in google_tweets:
        a = 0
        b = 0
        print 'Google: ' + str(key)
        value = google_tweets[key]
        for f in value:
            if f == 'pos':
                a += 1
            elif f == 'neg':
                b +=1
        print 'pos: ' + str(a) + '   neg: ' + str(b)
        dailyData.append(('Google', key, a, b))
    for key in apple_tweets:
        a = 0
        b = 0
        print 'Apple: ' + str(key)
        value = apple_tweets[key]
        for f in value:
            if f == 'pos':
                a += 1
            elif f == 'neg':
                b +=1
        print 'pos: ' + str(a) + '   neg: ' + str(b)
        dailyData.append(('Apple', key, a, b))
    for key in microsoft_tweets:
        a = 0
        b = 0
        print 'Microsoft: ' + str(key)
        value = microsoft_tweets[key]
        for f in value:
            if f == 'pos':
                a += 1
            elif f == 'neg':
                b +=1
        print 'pos: ' + str(a) + '   neg: ' + str(b)
        dailyData.append(('Microsoft', key, a, b))
        
    save_daily = open("dailyData.pickle", "wb")
    pickle.dump(dailyData, save_daily)
    save_daily.close()
    

def loadFromSaved(classifier):
    return
        
if __name__=="__main__":
    main()
    
    
