# -*- coding: utf-8 -*-
"""
Created on Wed May 16 12:32:01 2018
@author: PearlyBun
"""
import re
import json
from twython import Twython

#Create the Twitter class
class Twitter:

    #Initialize the keys
    
    def __init__(self,twitter_handle=None):
        if twitter_handle == None:
            print('Please enter twitter handle in class initialization')
        else:
            self.APP_KEY = ''
            self.APP_SECRET = ''
            self.OAUTH_TOKEN = ''
            self.OAUTH_TOKEN_SECRET = ''
            self.___twitter_handle___ = twitter_handle
            self.twitter = Twython(self.APP_KEY, self.APP_SECRET,self.OAUTH_TOKEN, self.OAUTH_TOKEN_SECRET)
    def get_profile(self):
        return self.replace(self.twitter.show_user(screen_name=self.___twitter_handle___))
    
    def get_followers(self,count,cursor):
         result=None
         next_cursor=None
         if cursor=='' or cursor==0 or cursor=='0' or cursor==None:
            result=self.replace(self.twitter.get_followers_list(count=count, screen_name=self.___twitter_handle___))
            next_cursor=self.get_next_cursor(result)
         else:
             result=self.replace(self.twitter.get_followers_list(count=count, screen_name=self.___twitter_handle___,cursor=str(cursor)))
             next_cursor=self.get_next_cursor(result)
         return result,next_cursor    
    
    def get_friends(self, count):
        return self.replace(self.twitter.get_friends_list(count=count, screen_name=self.___twitter_handle___))
    
    def get_tweets(self, count):
        return self.replace(self.twitter.get_user_timeline(count=count, screen_name=self.___twitter_handle___))
    
    def get_favorites_tweets(self,count):
        return self.replace(self.twitter.get_favorites(count=count, screen_name=self.___twitter_handle___))
    
    def get_user_list(self):
        result=self.replace(self.twitter.show_list(screen_name=self.___twitter_handle___))
        print(self.get_next_cursor(result))
        return result 
        
    #Filter the json to remove qoutes and enclose None in qoutes
    def replace(self,myjson):
        result = str(myjson)
        result=re.sub('None','""',result)
        result=re.sub('True','"True"',result)
        result=re.sub('False','"False"',result)
        result=re.sub(r'[a-zA-Z0-9]+(\')[a-zA-Z0-9]+','',result)
        result=re.sub('=(")','',result)
        result=re.sub('(") rel','',result)
        result=re.sub('(")>','',result)
        result=json.dumps(eval(result))
        result=json.loads(result)
        final_result = result
        return final_result
        
    #Get the next_cursor for pagination
    
    def get_next_cursor(self,the_json):
        next_cursor=None
        #the_json=json.loads(eval(the_json))
        if 'next_cursor' in the_json and not the_json['next_cursor']==None:
            next_cursor=the_json['next_cursor']
        return next_cursor
        
