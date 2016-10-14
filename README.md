# Twitter_API

The original idea behind this project has its origin in a PyLadies of San Francisco workshop (13 October 2016) led by Georgiana Ogrean.

## Twitter API

The Twitter API has a python wrapper thanks to the package Tweepy (http://docs.tweepy.org/en/v3.5.0/).

#### Authentication

The Tweepy documentation explains how to use OAuth for authentication. Here, I combine it with the use of `yaml` to keep private codes secure.
Consumer key and secret codes as well as access tokens are generated from https://apps.twitter.com/.


```python
import tweepy
import yaml

twitter_cred = yaml.load(open('../credentials/credentials.yml'))

consumer_key = twitter_cred['Twitter_api_Key']
consumer_secret = twitter_cred['Twitter_api_secret']

access_token = twitter_cred['Twitter_access_token_key']
access_token_secret = twitter_cred['Twitter_access_token_secret']

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)
```

#### Getting the data

Usage: run the script and choose Twitter account to investigate, thanks to its username.

```code
$python api_script.py realDonaldTrump
```

Twitter does not want its data shared between users, everyone will need to make their own. You can get the tweet information through Cursor, that handles all the pagination behind the scene, with items or pages method.

```python
# example of how to get the information with the Twitter API
username = 'realDonaldTrump'
list_data = []
for page in tweepy.Cursor(api.user_timeline, screen_name=username,
                              count=200, include_rts=False).pages(17):
        for status in page:
            data = status._json
            list_data.append(data)
```

The tweet information can be obtained in a dictionary (`data`). Keys are:
- contributors, truncated, text, is_quote_status, in_reply_to_status_id, id, favorite_count, source, retweeted, coordinates, entities, in_reply_to_screen_name, in_reply_to_user_id, retweet_count, id_str, favorited, user, geo, in_reply_to_user_id_str, possibly_sensitive, lang, created_at, in_reply_to_status_id_str, place.

The retrieved information, including the raw text of the tweet, make storing the information in a .csv format a little ticky. Thankfully, Python `csv` package has a `DictWriter` class that can handle this issue.
This .csv file can be read into a `Pandas DataFrame` or `DictReader`.



```python
categories_wanted = ['id', 'created_at', 'retweeted','source','text',\
                          'lang','favorite_count', 'retweet_count']
```
