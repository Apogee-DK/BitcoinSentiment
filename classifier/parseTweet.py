import re
from nltk.corpus import stopwords
import nltk
import pprint


excludeWords = ['AT_USER', 'url', 'rt', 'user']
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

    return tweet


# replace all negation words by "negati"
def replaceNegation(tweet):

    for i in range(len(tweet)):
        word = tweet[i].lower()
        if (word == "no" or word == "not" or word.count("n't") > 0 or word.count("esnt") > 0):
            tweet[i] = 'negati'

    return tweet


def normalize(tweet):
    """
    :param tweet: tweet text
    :return: normalized text according to: Alec Go (2009)'s Twitter Sentiment Classification using Distant Supervision
    """
    # http://stackoverflow.com/questions/2304632/regex-for-twitter-username
    tweet = re.sub('(?<=^|(?<=[^a-zA-Z0-9-_\.]))@([A-Za-z]+[A-Za-z0-9]+)', 'USER', tweet)
    tweet = tweet.replace('\\', '')
    tweet = re.sub('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', 'URL', tweet)
    tweet = removeNegation(tweet.lower().split())
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
            if tweet.sentiment == 1:
                weightedWords[token]['pos'] += 1
            elif tweet.sentiment == 0:
                weightedWords[token]['neut'] += 1
            elif tweet.sentiment == -1:
                weightedWords[token]['neg'] += 1
        else:
            weightedWords[token] = {}
            if tweet.sentiment == 1:
                weightedWords[token]['pos'] = 1
                weightedWords[token]['neut'] = 0
                weightedWords[token]['neg'] = 0 
            elif tweet.sentiment == 0:   
                weightedWords[token]['pos'] = 0
                weightedWords[token]['neut'] = 1
                weightedWords[token]['neg'] = 0        
            elif tweet.sentiment == -1:
                weightedWords[token]['pos'] = 0
                weightedWords[token]['neut'] = 0
                weightedWords[token]['neg'] = 1 
                
def getKeyAndValue():
    return weightedWords   
