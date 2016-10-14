'''
this script allows the user to create the csv file with the tweets and
meta-data for these tweets for a given Twitter user

the Twitter user who account is looked at is defined with username,
and can be given in the command line

prerequisite:
------------
    credentials.yml must have your Twitter tokens and access_token:
    --> Twitter_api_Key: ********
        Twitter_api_secret: **********
        Twitter_access_token_key: *********
        Twitter_access_token_secret: *********

    structure of repository:
    - credentials
    - Twitter_API
        - code
        - data
'''

import tweepy
import yaml
import csv
import sys

def authentication(credential_filename):
    '''
    getting a working line to the Twitter API, with authentification
    '''
    twitter_cred = yaml.load(open(credential_filename))

    consumer_key = twitter_cred['Twitter_api_Key']
    consumer_secret = twitter_cred['Twitter_api_secret']

    access_token = twitter_cred['Twitter_access_token_key']
    access_token_secret = twitter_cred['Twitter_access_token_secret']

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    api = tweepy.API(auth)
    return api

def get_data(api, username):
    '''
    parameters
    ----------
    api: the tweepy api with the authorization
        tweepy.API(auth)
    username: as STR

    return
    ------
    a list of dictionaries containing the information for each tweet
    '''
    list_data = []
    for page in tweepy.Cursor(api.user_timeline, screen_name=username,
                                  count=200, include_rts=False).pages(17):
        for status in page:
            data = status._json
            for key in data:
                try:
                    data[key] = data[key].encode('ascii', 'ignore')
                except:
                    continue
            list_data.append(data)
    return list_data

def keep_only_wanted_categories(list_data, categories_wanted):
    '''
    parameters
    ----------
    list_data: as LST of DICT
               the response of the Twitter API
    categories_wanted: as LST of STR
            the categories from the API that we want to keep

    return
    ------
    a list of dictionaries with only the keys corresponding the categories
    we want to keep
    '''
    set_categories_wanted = set(categories_wanted)
    list_wanted_information = []
    for data in list_data:
        d = {}
        for key in data:
            if key in set_categories_wanted:
                d[key] = data[key]
        list_wanted_information.append(d)
    return list_wanted_information

def write_csv(filename, list_wanted_information, categories_wanted):
    with open(filename, 'w') as csvfile:
        fieldnames = categories_wanted
        writer = csv.DictWriter(csvfile, fieldnames=categories_wanted)
        writer.writeheader()
        for d in list_wanted_information:
            writer.writerow(d)

if __name__ == '__main__':
    if len(sys.argv[1]) != 0:
        username = sys.argv[1]
    else:
        username = 'realDonaldTrump'

    print('looking at ', username, ' account.')

    categories_wanted = ['id', 'created_at', 'retweeted','source','text',\
                              'lang','favorite_count', 'retweet_count']
    credential_filename = '../../credentials/credentials.yml'

    api = authentication(credential_filename)
    print('get the information from Twitter API')
    list_data = get_data(api, username)
    list_wanted_information = keep_only_wanted_categories(list_data, categories_wanted)

    print('Write a csv file')
    filename = '../data/' + username + '.csv'
    write_csv(filename, list_wanted_information, categories_wanted)
