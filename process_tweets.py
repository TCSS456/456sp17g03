# -*- coding: utf-8 -*-
#process stored tweets from Twitter Public Stream
import os
import re
import json
import string
import pickle
import pandas as pd
import matplotlib.pyplot as plt
from nltk.tokenize import TweetTokenizer

raw_data = []
processed_tweets = []
microsoft_tweets = []
apple_tweets = []
google_tweets = []
missingTweets = 0
tknzr = TweetTokenizer()
removeStopwords = False


#for file in files:
    
def readTweetsFromFiles(removeS):   
    #get tweet, date, category (text, created_at, category)
    global removeStopwords
    removeStopwords = removeS
    script_dir = os.path.dirname(__file__)
    data_files = os.listdir("raw_data")
    for f in data_files:
        #process 50k tweets at a time
        path = "raw_data/" + f
        tweets_json = open(path, "r")
        for line in tweets_json:
            try:
                tweet = json.loads(line)
                raw_data.append((tweet['created_at'], tweet['text'].encode("utf-8")))
            except:
                continue
    print "number of input tweets read in: " + str(len(raw_data))
    
    #load stopwords
    global stopwords
    stopwords = []
    script_dir = os.path.dirname(__file__)
    rel_path = "corpora/stopwords.txt"
    file_path = os.path.join(script_dir, rel_path)
    sw_file = open(file_path, 'r')
    words = sw_file.readlines()
    for w in words:
        sw = w.strip()
        stopwords.append(sw)
    
    #print len(raw_data)
    for tweet in raw_data:
        processTweet(tweet)
    for t in microsoft_tweets:
        processed_tweets.append(['microsoft']+ (t))
    for t in apple_tweets:
        processed_tweets.append(['apple']+ (t))
    for t in google_tweets:
        processed_tweets.append(['google']+ (t))
    #for p in processed_tweets:
    #    print p
    print "Number of processed tweets: " + str(len(processed_tweets))
    print "Missing tweets: " + str(missingTweets) 
    if removeStopwords:
        save_processed = open("stopwordprocessed.pickle","wb")
    else:
        save_processed = open("processedTweets.pickle","wb")
    pickle.dump(processed_tweets, save_processed)
    save_processed.close()
    return processed_tweets
    

def processTweet(tweet):
    #clean up data from Twitter and categorize
    apple = ["@apple", "#apple", "@tim_cook", "apple"]
    microsoft = ["@microsoft", "#microsoft", "@satyanadella", "microsoft"]
    google = ["@google", "#google", "@sundarpichai", "google"]
    isApple = False
    isMicrosoft = False
    isGoogle = False
    
    tweetDate = tweet[0]
    tweetText = tweet[1].lower()
    #tweetText = unicode(tweetText, errors='replace')
    tweetText = re.sub(r'((http?://[^\s]+))','URL',tweetText)
    tweetText = re.sub(r'((https?://[^\s]+))','URL',tweetText)
    for t in apple:
        if t in tweetText:
            isApple = True
    for t in microsoft:
        if t in tweetText:
            isMicrosoft = True
    for t in google:
        if t in tweetText:
            isGoogle = True
    if not isGoogle and not isMicrosoft and not isApple:
        global missingTweets
        missingTweets += 1

    tweetText = re.sub(r'#([^\s]+)', 'HASHTAG', tweetText)
    tweetText = re.sub(r'@([^\s]+)', 'USER', tweetText)
    parseText = tknzr.tokenize(tweetText)
    for t in parseText:
        if removeStopwords:
            if t in stopwords:
                parseText[:] = [x for x in parseText if x != t]
        else:
            if t in ['URL', 'HASHTAG', 'USER', 'RT', 'rt']:
                parseText[:] = [x for x in parseText if x != t]
    tweetText = "".join([" "+i if not i.startswith("'") and i not in string.punctuation else i for i in parseText]).strip()
    if isGoogle:
        google_tweets.append([tweetDate, tweetText])
    if isMicrosoft:
        microsoft_tweets.append([tweetDate, tweetText])
    if isApple:
        apple_tweets.append([tweetDate, tweetText])

def main():
    readTweetsFromFiles()    
if __name__=="__main__":
    main()
    
    
    
