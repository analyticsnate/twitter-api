# api packages
import requests
from requests_oauthlib import OAuth1

# data packages
import pandas as pd
import json
from datetime import datetime
date_format = '%a %b %d %H:%M:%S %Y'

class TwitterAPI():

    def __init__(self):
        self.auth = self.load_api_keys('api_keys.json')
        self.user_tweet_cols = ['id', 'created_at', 'text', 'retweeted']
        self.date_format = '%a %b %d %H:%M:%S %Y'
        
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
        # load api keys json file into dict
        api_keys_file = open(json_file)
        api_keys_str = api_keys_file.read()
        api_keys_dict = json.loads(api_keys_str)

        # return OAuth1 object
        return OAuth1(
            api_keys_dict['api_key']
            ,api_keys_dict['api_secret_key']
            ,api_keys_dict['access_token']
            ,api_keys_dict['access_secret_token']
        )

    def user_tweet_search(self, screen_name, max_id=None, since_id=None, include_rts=True, count=200):
        # resource url
        user_search_url = 'https://api.twitter.com/1.1/statuses/user_timeline.json'

        # user search params
        user_search_payload = {
            'screen_name': screen_name
            ,'include_rts': include_rts
            ,'count': count
            ,'max_id': max_id
            ,'since_id': since_id}

        # api call
        user_search_response = requests.get(
            user_search_url
            ,params=user_search_payload
            ,auth=self.auth)

        # return api response
        return user_search_response

    def response_to_df(self, response, filter_cols=False, cols=None):
        df = pd.DataFrame(response.json())
        if filter_cols:
            df = df.filter(cols)
        return df

    def get_max_id(self, screen_name):
        response = self.user_tweet_search(screen_name)
        df = self.response_to_df(response)
        return df['id'][0] + 1