# Twitter_API

The original idea behind this project has its roots in a PyLadies of San Francisco workshop (13 October 2016) led by Georgiana Ogrean as well as from the R-based analysis of tweets performed by David Robinson (http://varianceexplained.org/r/trump-tweets/)

General Goal: A NLP project, using Twitter's API (and Tweepy), that allows for data exploration as well as a study of the richness of the Twitter vocabulary for a given user (here, recent events dictate that person to be Donald Trump). A sentiment analysis (polarity and subjectivity thanks to Text Blob) is also carried out for the tweets in general as well as for adjectives in particular (tagging words with nltk POS and Stanford's NER).

- Preview of the wordcloud based on the Donald Trump's tweets:
<figure>
  <img style="float: right;" src="https://github.com/AnnaVM/Twitter_API/blob/master/images/twitter_wordcloud.png"
   alt="wordcloud for Twitter account"
    width="456">
  <figcaption>Fig0. - Wordcloud in the shape of the Twitter bird, based on tweets from realDonaldTrump's account, posted from Android and not in quotation.</figcaption>
</figure>

## Using the Twitter API

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

## Exploration of the data and feature engineering

A Jupyter Notebook `Trump_or_staff` explores the differences between features of tweets written on Android vs iPhone, as this seems to be a difference between tweets written directly by Donald Trump, vs those written by his staff. The time and day of the week show different patterns, as do the use of links/hashtags or the use of quotation marks.

-Looking at tweets in quotes (Donald Trump's way of retweeting):
<figure>
  <img style="float: right;" src="https://github.com/AnnaVM/Twitter_API/blob/master/images/isQuote.png"
   alt="tweets in quotes"
    width="456">
  <figcaption>Fig1. - Bar graph of tweets from Android vs iPhone - looking at tweets in quotes.</figcaption>
</figure>

- Looking at tweets with links (more of a staff behavior):
<figure>
  <img style="float: right;" src="https://github.com/AnnaVM/Twitter_API/blob/master/images/hasLinks.png"
   alt="tweets with links"
    width="456">
  <figcaption>Fig2. - Bar graph of tweets from Android vs iPhone - looking at presence/absence of links in the tweets.</figcaption>
</figure>


- Looking at time of day when tweets are published with an iPhone vs on Android plateform:
<figure>
  <img style="float: right;" src="https://github.com/AnnaVM/Twitter_API/blob/master/images/hour_graph.png"
   alt="hours of tweets"
    width="456">
  <figcaption>Fig3. - Graph of when tweets from Android vs iPhone are published</figcaption>
</figure>

## Richness of vocabulary

The aim of this section is to explore the diversity of the vocabulary used in tweets that are identified as coming from Donald Trump rather than his staff and that are not simply retweets (tweet in quotes in this particular data). The tweets will therefore be tokenized, the tokens will be tagged as well as processed (lemmatized or stemmed, with stopwords and very short words also removed). The Jupyter Notebook `Trump_vocabulary` allows you to follow along.

<figure>
  <img style="float: right;" src="https://github.com/AnnaVM/Twitter_API/blob/master/images/twitter_wordcloud.png"
   alt="Twitter wordcloud"
    width="456">
  <figcaption>Fig4. - Wordcloud of Donald Trump's vocabulary.</figcaption>
</figure>

#### Tags:
A very slow, but information rich, step implemented here is tagging tokens with i) standard part of speech tags (standard `nltk` package -- we can focus on adjectives vs verbs for instance) as well as with ii) 3 classes for named entity recognizers ie. person, organization, location (`StanfordNERTagger` - http://nlp.stanford.edu/software/CRF-NER.shtml).

#### Explore adjective, adverbs and verb tags:

The POS tags allow us to selectively look at adjectives, adverbs and verbs.
<figure>
  <img style="float: right;" src="https://github.com/AnnaVM/Twitter_API/blob/master/images/adj_count.png"
   alt="most frequent adjectives"
    width="250">
    <img style="float: right;" src="https://github.com/AnnaVM/Twitter_API/blob/master/images/adv_count.png"
     alt="most frequent adverbs"
      width="250">
    <img style="float: right;" src="https://github.com/AnnaVM/Twitter_API/blob/master/images/verb_count.png"
       alt="most frequent verbs"
        width="250">
  <figcaption>Fig5. - Bar charts to show the count of the most frequent adjectives, adverbs and verbs.</figcaption>
</figure>

Using `Textblob` the subjectivity and the positive/negative content know as polarity of tweets were investigated. A specific sub-category of the vocabulary, adjectives, were then analyzed. The results are summarized in the following graph to acocunt for frequency of usage as well as for sentiment charge.  
<figure>
  <img style="float: right;" src="https://github.com/AnnaVM/Twitter_API/blob/master/images/sentiment_analysis.png"
   alt="Twitter wordcloud"
    width="456">
  <figcaption>Fig4. - Sentiment analysis of Donald Trump's adjective use. Size of the word reflects its usage, x position its polarity (-1 is negative, 1 positive sentiments) and y position its subjectivity (0 for objective and 1 for subjective).</figcaption>
</figure>
