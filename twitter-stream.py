# -*- coding: utf-8 -*-
#file for retrieving and storing Twitter streaming data
#Import the necessary methods from tweepy library
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream

access_token = "***************************************************"
access_token_secret = "***************************************************"
consumer_key = "***************************************************"
consumer_secret = "***************************************************"


class StdOutListener(StreamListener):

    def on_data(self, data):
        print data
        return True

    def on_error(self, status):
        print status


if __name__ == '__main__':
    l = StdOutListener()
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    stream = Stream(auth, l)
    stream.filter(track=['#apple', '#microsoft', '#google', '@apple', '@microsoft', '@google', '@sundarpichai', '@satyanadella', '@tim_cook'], languages=['en'])


