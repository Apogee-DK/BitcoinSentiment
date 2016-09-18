import csv
from parseTweet import *

import sys
sys.path.insert(0, '../database/')

# Retrieves data from database
from dbStatistics import *

def getfeatureOccurence():
    # dbStatistics function that returns a list of 'key': {'pos':1, 'neut':2, 'neg':3}
    # return getKeyAndValue()
    return getAllWeightedWords()

def calculateSentiment(_features, _featureOccurenceValues):

    tweetWordProbability = []
    probabilityOfPositiveFeature = 1.0
    probabilityOfNegativeFeature = 1.0
    result = 0
    
    # dbStatistics will handle the following functions
    # P ( Value )
    # Must provide floating number
    totalNumberOfPositiveTweets = float(getNumberOfPositiveTweets())
    totalNumberOfNegativeTweets = float(getNumberOfNegativeTweets())
    totalNumberOfTweets = float(getNumberOfTweets())
    
    # FOR UNIT_TEST
    # totalNumberOfNegativeTweets = 77.0
    # totalNumberOfPositiveTweets = 137.0
    # totalNumberOfTweets = 300.0

    probabilityOfPositivity = totalNumberOfPositiveTweets/totalNumberOfTweets
    probabilityOfNegativity = 1.0 - probabilityOfPositivity
    
    # P ( Feature | Value )
    for feature in _features:
        if(feature in _featureOccurenceValues):
            listOfValues = _featureOccurenceValues[feature]

        else:
            # Need to create function that will address words that never appeared in the database

            # Use API to get pos and neg probability, and multiply the probability with the total number of tweets

            # Store in the database
            
            continue
            
        # Maximum value of the list
        probabilityOfPositiveFeature *= (listOfValues['pos'] + listOfValues['lpos'])/totalNumberOfPositiveTweets
        probabilityOfNegativeFeature *= (listOfValues['neg'] + listOfValues['lneg'])/totalNumberOfNegativeTweets
        
        
        if(probabilityOfPositiveFeature > probabilityOfNegativeFeature):
            if(listOfValues['pos'] > listOfValues['lpos']):
                result = 2
            else:
                result = 1

        elif(probabilityOfPositiveFeature < probabilityOfNegativeFeature):
            if(listOfValues['neg'] > listOfValues['lneg']):
                result = -2
            else:
                result = -1
        else:
            result = 0               
    
    return result

def getTweetSentiment(_tweetObject):
    # Get dictionary of <word, list of values (pos, lpos, neu, lneg, neg)>
    featureOccurenceValues = getfeatureOccurence()
    
    # Get necessary values from TweetObject
    features = getFeatures(_tweetObject)
    print(_tweetObject.getTweet())
    
    result = calculateSentiment(features, featureOccurenceValues)

    if(result == 0):
        # result = input('Require user analysis (pos, neg, neut) - ' + _tweetObject.getTweet() + ' - ')
        result = 0
    
    # Determine the total value of the tweet    
    return result

def unit_test():
    array = {'love' : {'neg':4, 'neut':10, 'pos':4},
             'bitcoin' : {'neg':7, 'neut':4, 'pos':10},
             'bearish' : {'neg':6, 'neut':0, 'pos':2},
             'bullish' : {'neg':2, 'neut':0, 'pos':13},
             'trend' : {'neg':8, 'neut':2, 'pos':6},
             'intrusive' : {'neg':15, 'neut':2, 'pos':0},
             'inconceivable' : {'neg':10, 'neut':2, 'pos':2},
             'good' : {'neg':4, 'neut':12, 'pos':18},
             'sad' : {'neg':10, 'neut':13, 'pos':2}}

    features = {'love', 'bitcoin', 'bullish'}

    print(calculateSentiment(features, array))

    # result should be 0.79... which is correct


# main #

tweetObjectList = []

with open('../dataset/tweet3.csv', 'rb') as csvfile:
    tweetreader = csv.DictReader(csvfile)
    linectr = 0
    
    for row in tweetreader:
        linectr += 1
        # print', '.join(row)
        # print row['tweetID'], row['tweetText']
        to = TweetObject(row)
        tweetObjectList.append(to)
        if linectr == 300:
            break

for to in tweetObjectList:
    print(to.userID, ' ', to.tweetText, ' ', to.sentiment)
    classifyWord(to)
    # print '\n'

with open('../dataset/tweet3.csv', 'rb') as csvfile:
    tweetreader = csv.DictReader(csvfile)
    linectr = 0
    
    for row in tweetreader:
        linectr += 1
        if(linectr < 301):
            continue        
        # print', '.join(row)
        # print row['tweetID'], row['tweetText']
        to = TweetObject(row)
        print(getTweetSentiment(to))
        if linectr == 400:
            break

