# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-
import os
import nltk
import pickle
import itertools
import re
import random

from training_preprocessing import loadStanford, loadSanders
from nltk.tokenize import word_tokenize, TweetTokenizer
from itertools import chain
from nltk.classify.scikitlearn import SklearnClassifier
from sklearn.naive_bayes import MultinomialNB, BernoulliNB, GaussianNB
from sklearn.linear_model import LogisticRegression,SGDClassifier
from sklearn.svm import SVC, LinearSVC, NuSVC

word_features = []    

def train(classifyType, removeS):
    features = load_features(removeS)
    train_set = features[9500:]
    test_set = features[:1406]
        
    
    global word_features
    word_features = get_word_features(get_words_in_tweets(train_set))
    training_set = nltk.classify.apply_features(extract_features, train_set)
    testing_set = nltk.classify.apply_features(extract_features, test_set)
    if classifyType == "MNB":
        MNBclassifier = SklearnClassifier(MultinomialNB())
        MNBclassifier.train(training_set)
        save_classifier = open("MNBClassifier.pickle","wb")
        pickle.dump(MNBclassifier, save_classifier)
        save_classifier.close()
        print("MNB_classifier accuracy percent:",(nltk.classify.accuracy(MNBclassifier, testing_set))*100)
        return MNBclassifier
    elif classifyType == "BNB":
        BNBClassifier = SklearnClassifier(BernoulliNB())
        BNBClassifier.train(training_set)
        save_classifier = open("BNBClassifier.pickle", "wb")
        pickle.dump(BNBClassifier, save_classifier)
        save_classifier.close()
        print("BernoulliNB_classifier accuracy percent:",(nltk.classify.accuracy(BNBClassifier,testing_set))*100)
        return BNBClassifier
    elif classifyType == "NB":
        NBClassifier = nltk.NaiveBayesClassifier.train(training_set)
        save_classifier = open("NBClassifier.pickle", "wb")
        pickle.dump(NBClassifier, save_classifier)
        save_classifier.close()
        NBClassifier.show_most_informative_features(40)
        print("Original Naive Bayes Algo accuracy percent:",(nltk.classify.accuracy(NBClassifier, testing_set))*100)
        return NBClassifier
    elif classifyType == "LSVC":
        LSVClassifier = SklearnClassifier(LinearSVC())
        LSVClassifier.train(training_set)
        save_classifier = open ("LSVClassifier.pickle", "wb")
        pickle.dump(LSVClassifier, save_classifier)
        save_classifier.close()
        print("LSVClassifier accuracy percent:", (nltk.classify.accuracy(LSVClassifier, testing_set))*100)
        return LSVClassifier
    elif classifyType == "SGDC":
        SGDC = SklearnClassifier(SGDClassifier())
        SGDC.train(training_set)
        save_classifier = open("SGDClassifier.pickle","wb")
        pickle.dump(SGDC, save_classifier)
        save_classifier.close()
        print("SGDClassifier accuracy percent:", (nltk.classify.accuracy(SGDC, testing_set))*100)
        return SGDC
    else:
        print "Classifier not specified."
        return


    
def get_words_in_tweets(tweets):
    all_words = []
    for (words, sentiment) in tweets:
        all_words.extend(words)
    return all_words

def get_word_features(wordlist):
    wordlist = nltk.FreqDist(wordlist)
    word_features = wordlist.keys()
    return word_features
    
def load_features(removeS):
    #load training sets and associated features
    script_dir = os.path.dirname(__file__)
    rel_path = "corpora/training.1600000.processed.noemoticon.csv"
    file_path = os.path.join(script_dir, rel_path)
    stanford = loadStanford(file_path, 5000, removeS)
    rel_path = "corpora/sanders-corpus.csv"
    file_path = os.path.join(script_dir, rel_path)
    sanders = loadSanders(file_path, removeS)
    features = list(itertools.chain(stanford, sanders))
    #features = list(sanders)
    random.shuffle(features)    
    print "Number of training tweets loaded: " + str(len(features))
    #build vocabulary list
    return features

    
def extract_features(document):
    document_words = set(document)
    features = {}
    for word in word_features:
        features['contains(%s)' % word] = (word in document_words)
    return features

#==============================================================================
# def processTweet(tweet):
#     features = []
#     tknzr = TweetTokenizer()
#     stopwords = []
#     script_dir = os.path.dirname(__file__)
#     rel_path = "corpora/stopwords.txt"
#     file_path = os.path.join(script_dir, rel_path)
#     sw_file = open(file_path, 'r')
#     words = sw_file.readlines()
#     #remove stopwords and get features
#     for w in words:
#         sw = w.strip()
#         stopwords.append(sw)
# 
#     tweet = re.sub(r'((http?://[^\s]+))','URL',tweet)
#     tweet = re.sub(r'#([^\s]+)', 'HASHTAG', tweet)
#     tweet = re.sub(r'@([^\s]+)', 'USER', tweet)
#     tweet = tweet.strip('\'"')
#     #bypass for non-unicode chars in stanford corpus
#     tweet = tknzr.tokenize(tweet)
#     for t in tweet:
#         if t in ['URL', 'HASHTAG', 'USER']:
#             continue
#         else:
#             features.append(t.lower())
#     return features
#==============================================================================

def testClassifiers():
    return
    
    
#if __name__=="__main__":
#    main()
    
    


