# -*- coding: utf-8 -*-
#Normalize data between the two training corpus for use in training
import csv
import nltk
import string
import os
import re
import numpy as np
import random

from nltk.tokenize import TweetTokenizer


def loadSanders(filepath, removeS):
    #print "In loadSanders"
    tweet_sentiments = list()
    training_file = open(filepath, 'r')
    tweetreader = csv.reader(training_file, delimiter=",")
    for tweet in tweetreader:
        sent = ''
        if tweet[1] == 'positive':
            sent = 'pos'
        elif tweet[1] == 'negative':
            sent = 'neg'
        else:
            continue
        text = tweet[4]
        tweet_sentiments.append((text.lower(), sent))
    random.shuffle(tweet_sentiments)
    #for row in tweet_sentiments:
    #    print row
    tweet_sentiments = processTweets(tweet_sentiments, removeS)
    return iter(tweet_sentiments)

def loadStanford(filepath, count, removeS):
    #print "In loadStanford"
    negCount = 0
    posCount = 0
    tweet_sentiments = list()
    training_file = open(filepath, 'r')
    tweetreader = csv.reader(training_file, delimiter=",")
    for tweet in tweetreader:
        #print "Sentiment: " + tweet[0] + ", Tweet: " + tweet[5]
        sent = ''
        if tweet[0] == '0' and negCount < count:
            sent = 'neg'
            negCount += 1
        elif tweet[0] == '4' and posCount < count:
            sent = 'pos'
            posCount += 1
        else:
            continue
        text = tweet[5]
        tweet_sentiments.append((text.lower(), sent))
        if(count <= negCount and count <= posCount):
            break
    random.shuffle(tweet_sentiments)
    #print "done loading stanford"
    #for row in tweet_sentiments:
    #    print row
    tweet_sentiments = processTweets(tweet_sentiments, removeS)
    return iter(tweet_sentiments)

def processTweets(tweets, removeS):
    #stopwords - http://www.academia.edu/7221849/STOPWORDS_a_about_above_across_after_again_against_all_almost_alone_along_already_also_although_always_among_an_and_another_any_anybody_anyone
    tknzd_sentiments = []
    tknzr = TweetTokenizer()
    stopwords = []
    script_dir = os.path.dirname(__file__)
    rel_path = "corpora/stopwords.txt"
    file_path = os.path.join(script_dir, rel_path)
    sw_file = open(file_path, 'r')
    words = sw_file.readlines()
    #remove stopwords and get features
    for w in words:
        sw = w.strip()
        stopwords.append(sw)

    for row in tweets:
        text = row[0]
        text = re.sub(r'((http?://[^\s]+))','URL',text)
        text = re.sub(r'#([^\s]+)', 'HASHTAG', text)
        text = re.sub(r'@([^\s]+)', 'USER', text)
        text = text.strip('\'"')
        #bypass for non-unicode chars in stanford corpus
        text = unicode(text, errors='replace')
        text = tknzr.tokenize(text)
        for t in text:
            if removeS:
                if t in stopwords:
                    text[:] = [x for x in text if x != t]
            if t in ['URL', 'HASHTAG', 'USER']:
                text[:] = [x for x in text if x != t]
        #text = "".join([" "+i if not i.startswith("'") and i not in string.punctuation else i for i in text]).strip()
        tknzd_sentiments.append((text, row[1]))
    return tknzd_sentiments

