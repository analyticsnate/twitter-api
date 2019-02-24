# api packages
import requests
from requests_oauthlib import OAuth1
import pyPTP
import os

# data packages
import pandas as pd
import json
import time
from datetime import datetime
date_format = '%a %b %d %H:%M:%S %Y'

class TwitterAPI():

    def __init__(self, s=1):
        """
        Params:
        -------
        s : int
        sleep time between api calls (seconds)
        """
        self.auth = self.load_api_keys('api_keys.json')
        self.user_tweet_cols = ['id', 'created_at', 'text', 'retweeted']
        self.date_format = '%a %b %d %H:%M:%S %Y'
        self.s = s # standard sleep time between api calls

        # set up api endpoints
        self.user_url = 'https://api.twitter.com/1.1/statuses/user_timeline.json'
        self.keyword_url = 'https://api.twitter.com/1.1/search/tweets.json'
        
        # @realDonaldTrump first tweet id of each month
        self.tweet_max_ids = {
            'Jan 2018': 947802588174577664
            ,'Feb 2018': 959029384052166657
            ,'Mar 2018': 969178931369783296
            ,'Apr 2018': 980421275326865409
            ,'May 2018': 991267863674675200
            ,'Jun 2018': 1002506360351846400
            ,'Jul 2018': 1013391783533989888
            ,'Aug 2018': 1024450744198553600
            ,'Sep 2018': 1035678961349668864
            ,'Oct 2018': 1046708836407685122
            ,'Nov 2018': 1057797701834813440}

    def load_api_keys(self, json_file):
        location = os.path.realpath(
            os.path.join(os.getcwd(), os.path.dirname(__file__)))

        # load api keys json file into dict
        api_keys_file = open(os.path.join(location, json_file))
        api_keys_str = api_keys_file.read()
        api_keys_dict = json.loads(api_keys_str)

        # return OAuth1 object
        return OAuth1(
            api_keys_dict['api_key']
            ,api_keys_dict['api_secret_key']
            ,api_keys_dict['access_token']
            ,api_keys_dict['access_secret_token']
        )

    def id_tweet_search(self, id):
        """
        Returns single tweet with the given id.
        """

        # id search params
        id_search_payload = {
            'max_id': id
            , 'count': 1}

        # api call
        id_search_response = requests.get(
            self.keyword_url
            , params=id_search_payload
            , auth=self.auth)

        # check api call status
        if id_search_response.status_code == 200:
            return pd.DataFrame(id_search_response.json())

    def user_tweet_search(self, screen_name, max_id=None, since_id=None, include_rts=True, count=200):

        # user search params
        user_search_payload = {
            'screen_name': screen_name
            ,'include_rts': include_rts
            ,'count': count
            ,'max_id': max_id
            ,'since_id': since_id}

        # api call
        user_search_response = requests.get(
            self.user_url
            ,params=user_search_payload
            ,auth=self.auth)

        # check api call status
        if user_search_response.status_code == 200:
            # api call succeeded
            # convert response to json, then to a dataframe and filter down
            return pd.DataFrame(user_search_response.json()['statuses'])
        elif user_search_response.status_code == 429:
            # api call failed because I'm not paying money - return None
            print('Too many twitter api requests!')
            return None
        else:
            # api call failed - return None
            print('API Call failed. Status Code {0}'.format(
                user_search_response.status_code))
            return None

    def keyword_tweet_search(self, search_term, count=100, max_id=None, until=None):

        # keyword search params
        keyword_search_payload = {
            'q': search_term
            ,'count': count
            ,'until': until
            ,'max_id': max_id}

        # twitter api call
        keyword_search_response = requests.get(
            self.keyword_url
            ,params=keyword_search_payload
            ,auth=self.auth)

        # check api call status
        if keyword_search_response.status_code == 200:
            # api call succeeded
            # convert response to json, then to a dataframe and filter down
            return pd.DataFrame(keyword_search_response.json()['statuses'])
        elif keyword_search_response.status_code == 429:
            # api call failed because I'm not paying money - return None
            print('Too many twitter api requests!')
            return None
        else:
            # api call failed - return None
            print('API Call failed. Status Code {0}'.format(
                keyword_search_response.status_code))
            return None

    def get_tweets_since(self, search_term, start_dt=datetime(2018, 11, 1)):
        current_dt = datetime.today()
        max_id = None
        cols = ['id', 'created_at', 'geo', 'favorited_count', 'retweet_count' 'place', 'text', 'user']
        df = pd.DataFrame(columns=cols)
        ptp = pyPTP.process_time_printer()
        
        while start_dt < current_dt:
            st = ptp.get_time()
            temp_df = self.keyword_tweet_search(search_term, max_id=max_id)
            if temp_df is not None:
                temp_df = temp_df.filter(cols)
                df = df.append(temp_df)
            else:
                # returning none means the API failed
                break
            
            # get value of last tweet id and subtract 1
            # this becomes the max_id of next iteration
            try:
                max_id = temp_df.tail(1)['id'][len(temp_df)-1] - 1
            except:
                break
            
            # get date of last tweet or first tweet...?
            # this becomes the current_dt value
            datepart_1 = temp_df.tail(1)['created_at'][len(temp_df)-1][:19]
            datepart_2 = temp_df.tail(1)['created_at'][len(temp_df)-1][-5:]
            current_dt = datetime.strptime(datepart_1 + datepart_2, self.date_format)
            
            ptp.increment(st)
            time.sleep(self.s)
            
        return df

    def get_max_id(self, screen_name):
        df = self.user_tweet_search(screen_name)
        return df['id'][0] + 1

    def seconds_since_tweet(self, row):
        datepart_1 = row['created_at'][:19]
        datepart_2 = row['created_at'][-5:]
        dt = datetime.strptime(datepart_1 + datepart_2, date_format)
        return round((datetime.utcnow() - dt).total_seconds(), 1)

    def minutes_since_tweet(self, row):
        return row['seconds_since_tweet'] / 60

    def days_since_tweet(self, row):
        return row['seconds_since_tweet'] / (60 * 60 * 24)

    def get_username(self, row):
        return '@' + row['user']['screen_name']

    def get_user_location(self, row):
        return row['user']['location']

    def get_day(self, row):
        datepart_1 = row['created_at'][:19]
        datepart_2 = row['created_at'][-5:]
        dt = datetime.strptime(datepart_1 + datepart_2, self.date_format)
        return dt.day