'''
give_source_name: identify the label of the source (Android, iPhone, ...)
get_time: get a Timestamp, which is easy to manipulate (delta time, hours, dow)
iSQuote: flags tweets that are entirely in quotation (Trump's way of retweeting)

get_counts: get number of tweets with False and True flags in a column
plot_histogram: plots the histogram corresponding to get_counts

get_hashtags & analyze_hashtags: extracts the hashtags (#...) and put them in a counter
get_mentions & analyze_mentions: extracts the mentions (@...) and put them in a counter
print_counter: nice way to visualize counters from 2 previous functions

clean_up_text: remove # and https
percent_words_all_caps: percentage of words in tweet in capital letters
'''
from datetime import datetime
import matplotlib.pyplot as plt
import numpy as np
import re
from collections import Counter

def give_source_name(value, source_types, source_names):
    '''
    parameters
    ----------
    value: as STR
          the information in the 'source' column
    source_types: as LST
          all the different values that value can take
    source_name: as LST
          human readable labels for the source_types, in the same order

    returns
    -------
    the label for the given source
    '''
    for index in range(len(source_types)):
        source_type = source_types[index]
        if value == source_type:
            return source_names[index]

def get_time(humanTime):
    '''
    parameter
    ---------
    humanTime: as strptime
               the information in the 'created_at' column
               for ex: Fri Oct 14 20:21:25 +0000 2016

    return
    ------
    timestamp
    '''
    date_object = datetime.strptime(humanTime[:-10] + humanTime[-4:],
                                    '%a %b %d %H:%M:%S %Y')
    return date_object

def isQuote(text):
    '''
    parameters
    ----------
    text: as STR

    returns
    -------
    True if the text is in quotation
    (how Trump retweets)
    '''
    return (text[0] == '"') and (text[-1] == '"')

def get_counts(df, column_name, mask):
    '''
    parameters
    ----------
    df: pandas DataFrame
    column_name: as STR
                the column must contain only True/False values
    mask: as Boolean series of len(df)

    returns
    -------
    number of tweets with mask (for instance to get only Android posted
    tweets) applied
    '''
    value_false = df[column_name][mask].value_counts()[False]
    value_true = df[column_name][mask].value_counts()[True]
    return value_false, value_true

def plot_histogram(df, column_name, mask_android, mask_iphone):
    '''
    parameters
    -----------
    see get_counts
    '''
    android_false, android_true = get_counts(df, column_name, mask_android)
    iphone_false, iphone_true = get_counts(df, column_name, mask_iphone)

    #plot
    fig, ax = plt.subplots()
    w = 0.3
    x = np.array([1,2])
    y = [android_false, iphone_false]
    z = [android_true, iphone_true]
    ax.bar(x, y ,width=w,color='b', label='not '+column_name)
    ax.bar(x+w, z ,width=w,color='g', label=column_name)
    plt.legend()
    plt.ylabel('Number of tweets')
    plt.title('Study of '+ column_name)
    ax.set_xticks(x + w)
    ax.set_xticklabels(('Android', 'iPhone'))
    plt.show()
    print 'Android (False/True): ', android_false, android_true
    print 'iPhone (False/True): ', iphone_false, iphone_true

def get_hashtags(text):
    '''
    returns
    -------
    list of all the hashtags in the tweet
    '''
    hashtag = re.compile(r'[#]\w*')
    return re.findall(hashtag, text)

def get_mentions(text):
    '''
    returns
    -------
    list of all the mentions in the tweet
    '''
    mention = re.compile(r'[@]\w*')
    return re.findall(mention, text)

def analyze_hashtags(df, mask):
    '''
    df must have a 'hashtags' column

    returns
    -------
    Counter of all the hashtags
    '''
    list_hashtags = []
    for item in df[mask]['hashtags']:
        list_hashtags.extend(item)
    return Counter(list_hashtags)

def analyze_mentions(df, mask):
    '''
    df must have a 'mentios' column

    returns
    -------
    Counter of all the mentions
    '''
    list_mentions = []
    for item in df[mask]['mentions']:
        list_mentions.extend(item)
    return Counter(list_mentions)

def print_counter(counter, min_count=1):
    for key, count in sorted(counter.iteritems(),\
                             key=lambda x: x[1], reverse=True):
        if count > min_count:
            print key, ': ', count

def clean_up_text(text):
    '''
    remove https links, hashtags and mentions
    '''
    hashtag = re.compile(r'[#]\w*')
    https = re.compile(r'https?:\/\/[a-zA-z0-9\/#%\.]+')
    mention = re.compile(r'[@]\w*')
    text = re.sub(hashtag, '', text)
    text = re.sub(https, '', text)
    text = re.sub(mention, '', text)
    return text

def percent_words_all_caps(text):
    '''
    returns
    -------
    percentage of words fully capitalized
    '''
    word = re.compile(r'\b[A-Za-z]+\b')
    all_caps_word = re.compile(r'\b[A-Z]+\b')
    num_words = len(re.findall(word, text))
    num_cap_words = len(re.findall(all_caps_word, text))
    if num_words == 0:
        return 0
    return round(float(num_cap_words)/num_words,2)
