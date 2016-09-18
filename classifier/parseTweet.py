import re
from nltk.corpus import stopwords
import nltk
import pprint
import json
import requests
import pycurl
import cStringIO, ast, sys, time
sys.path.insert(0, '../database/')

from dbStatistics import *
#from vaderSentiment.vaderSentiment import sentiment as vaderSentiment


excludeWords = ['AT_USER', 'at_user', 'url', 'rt', 'user', 'btc', 'bitcoin', 'bitstamp']
weightedWords = {}


class TweetObject():
    tweetObjectCount = 0
    
    def __init__(self, row):
        self.userID = row['userID']
        
        # print row['userID'] , ' ', row['tweetText']
        # print row['userID'] , ' ', preprocessTweet(row['tweetText'])
        self.originalTweet = row['tweetText']
        self.tweetText = normalize(preprocessTweet(row['tweetText']))
        self.sentiment = int(row['Sentiment'])

    def getTweet(self):
        return self.tweetText

# changed
def getFeatures(tweetObj):
    tokens = nltk.word_tokenize(tweetObj.tweetText)
    return tokens

# returns probabilities of 
def textProcessingAPI(posts):

    sentiments = []
    try:
        bufferIO = cStringIO.StringIO()
        c = pycurl.Curl()
        c.setopt(c.URL, 'http://text-processing.com/api/sentiment/')
        c.setopt(c.WRITEFUNCTION, bufferIO.write)
        postdata = 'text=' + posts
        c.setopt(c.POSTFIELDS, postdata)
        c.perform()
        val = bufferIO.getvalue()
        data = ast.literal_eval(val)
        data["post"] = posts
        sentiments.append(data)
        bufferIO.close()
    except pycurl.error, error:
        errno, errstr = error
        print "An error occured: ", errstr

    #print "sentiments computed for %d posts" % cnt
    print sentiments
    return sentiments


"""
#compute sentiments using vaderSentiment
def vaderSentimentAPI(posts):
    sentiments = []
    data = {}
    data["post"] = posts
    vs = vaderSentiment(posts)
    #print vs
    if vs["neg"] >= vs["neu"] and vs["neg"] >= vs["pos"]:
        data["label"] = "neg"
    elif vs["pos"] >= vs["neu"] and vs["pos"] >= vs["neg"]:
        data["label"] = "pos"
    elif vs["neu"] >= vs["neg"] and vs["neu"] >= vs["pos"]:
        data["label"] = "neutral"    

    data['probability'] = {'neg': vs['neg'], 'neutral': vs['neu'], 'pos': vs['pos']}
    sentiments.append(data)
    print sentiments
    return sentiments
"""


def preprocessTweet(tweet):

    #Convert to lower case
    tweet = tweet.lower()
    #Convert www.* or https?://* to URL
    tweet = re.sub('((www\.[^\s]+)|(https?://[^\s]+))','URL',tweet)
    #Convert @username to AT_USER
    tweet = re.sub('@[^\s]+','USER',tweet)
    #Remove additional white spaces
    tweet = re.sub('[\s]+', ' ', tweet)
    #Replace #word with word
    tweet = re.sub(r'#([^\s]+)', r'\1', tweet)
    #trim
    tweet = tweet.strip('\'"')
    #replace # between words with ' '
    tweet = tweet.replace("#", " ")

    return tweet


# replace all negation words by "negati"
def replaceNegation(tweet):

    for i in range(len(tweet)):
        word = tweet[i].lower()
        if (word == "no" or word == "not" or word.count("n't") > 0 or word.count("esnt") > 0):
            tweet[i] = 'negati'

    return tweet


# get currency price, USDJPY:CUR for USDJPY , CL1:COM for Crude oil and etc..
def bbgPrice(quoteName):

    base_url = 'http://www.bloomberg.com/quote/'
    content = urllib.urlopen(base_url + quoteName).read()
    anchor = '<div class="price">'
    startIndex = content.index('<div class="price">')
    content = content[startIndex + len(anchor) : startIndex + 45]
    content = content.replace(",","")
    m = re.findall('\d+.\d+', content)

    return m[0]



def normalize(tweet):
    """
    :param tweet: tweet text
    :return: normalized text according to: Alec Go (2009)'s Twitter Sentiment Classification using Distant Supervision
    """
    # http://stackoverflow.com/questions/2304632/regex-for-twitter-username
    tweet = re.sub('(?<=^|(?<=[^a-zA-Z0-9-_\.]))@([A-Za-z]+[A-Za-z0-9]+)', 'USER', tweet)
    tweet = tweet.replace('\\', '')
    tweet = re.sub('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', 'URL', tweet)
    tweet = replaceNegation(tweet.lower().split())
    stops = set(stopwords.words("english"))
    # append exclude words to the stopwords set
    stops.update(excludeWords)
    tokens = [t for t in tweet if (not t in stops)]
    tokens = [t for t in tokens if "#" in t or t.isalnum()]

    return " ".join(set(tokens))


def classifyWord(tweet):
    tokens = nltk.word_tokenize(tweet.tweetText)
    for token in tokens:

        # if already in list, skip, else add to current value
        if token in weightedWords:
            if tweet.sentiment == 2:
                weightedWords[token]['pos'] += 1
            if tweet.sentiment == 1:
                weightedWords[token]['lpos'] += 1
            elif tweet.sentiment == 0:
                weightedWords[token]['neut'] += 1
            elif tweet.sentiment == -1:
                weightedWords[token]['neg'] += 1
            elif tweet.sentiment == -2:
                weightedWords[token]['lneg'] += 1
        else:
            weightedWords[token] = {}
            if tweet.sentiment == 2:
                weightedWords[token]['pos'] = 1
                weightedWords[token]['lpos'] = 0
                weightedWords[token]['neut'] = 0
                weightedWords[token]['neg'] = 0
                weightedWords[token]['lneg'] = 0
            if tweet.sentiment == 1:
                weightedWords[token]['pos'] = 0
                weightedWords[token]['lpos'] = 1
                weightedWords[token]['neut'] = 0
                weightedWords[token]['neg'] = 0
                weightedWords[token]['lneg'] = 0
            elif tweet.sentiment == 0:   
                weightedWords[token]['pos'] = 0
                weightedWords[token]['lpos'] = 0
                weightedWords[token]['neut'] = 1
                weightedWords[token]['neg'] = 0
                weightedWords[token]['lneg'] = 0      
            elif tweet.sentiment == -1:
                weightedWords[token]['pos'] = 0
                weightedWords[token]['lpos'] = 0
                weightedWords[token]['neut'] = 0
                weightedWords[token]['neg'] = 1
                weightedWords[token]['lneg'] = 0
            elif tweet.sentiment == -2:
                weightedWords[token]['pos'] = 0
                weightedWords[token]['lpos'] = 0
                weightedWords[token]['neut'] = 0
                weightedWords[token]['neg'] = 0
                weightedWords[token]['lneg'] = 1
                
        pos = weightedWords[token]['pos']
        lpos = weightedWords[token]['lpos']
        neut = weightedWords[token]['neut']
        neg = weightedWords[token]['neg']
        lneg = weightedWords[token]['lneg']

        # write to db, then print it
        putWord(token,pos,lpos,neut,neg,lneg)
        pprint.pprint( getWord(token))
        
        # firebase.put(firebase_URL + token, {'pos': pos, 'neut': neut, 'neg': neg})
        # print token, ' ', firebase.get(firebase_URL + token)
        ##print ('\n')
                
def getKeyAndValue():
    return weightedWords   

