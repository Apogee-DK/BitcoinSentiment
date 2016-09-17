import csv
from parseTweet import *

# Retrieves data from database
# from dbStatistics import *

def getfeatureOccurence():
    # dbStatistics function that returns a list of 'key': {'pos':1, 'neut':2, 'neg':3}
    return getKeyAndValue()

def calculateSentiment(_features, _featureOccurenceValues):

    tweetWordProbability = []
    probabilityOfPositiveFeature = 1.0
    probabilityOfNegativeFeature = 1.0
    
    # dbStatistics will handle the following functions
    # P ( Value )
    # Must provide floating number
    totalNumberOfPositiveTweets = float(getNumberOfPositiveTweets())
    totalNumberOfNegativeTweets = float(getNumberOfNegativeTweets())
    totalNumberOfTweets = float(getNumberOfTweets())
    
    # FOR UNIT_TEST
    # totalNumberOfNegativeTweets = 122.0
    # totalNumberOfPositiveTweets = 225.0
    # totalNumberOfTweets = 443.0

    probabilityOfPositivity = totalNumberOfPositiveTweets/totalNumberOfTweets
    probabilityOfNegativity = 1.0 - probabilityOfPositivity
    
    # P ( Feature | Value )
    for feature in _features:
        listOfValues = _featureOccurenceValues[feature]
        
        # Maximum value of the list
        probabilityOfPositiveFeature *= listOfValues['pos']/totalNumberOfPositiveTweets
        probabilityOfNegativeFeature *= listOfValues['neg']/totalNumberOfNegativeTweets
        
        
        if(probabilityOfPositiveFeature > probabilityOfNegativeFeature):
            result = 1
        elif(probabilityOfPositiveFeature < probabilityOfNegativeFeature):
            result = -1
        else:
            result = 0               
    
    return result

def getTweetSentiment(_tweetObject):
    # Get dictionary of <word, list of values (pos, neu, neg)>
    featureOccurenceValues = getfeatureOccurence()
    
    # Get necessary values from TweetObject
    features = getFeatures(_tweetObject)
    print(features)
    
    result = calculateSentiment(features, featureOccurenceValues)

    if(result == 0):
        result = input('Require user analysis (pos, neg, neut) - ' + _tweetObject.getTweet() + ' - ')

    
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

with open('../dataset/tweet2.csv', 'rb') as csvfile:
    tweetreader = csv.DictReader(csvfile)
    linectr = 0
    
    for row in tweetreader:
        linectr += 1
        # print', '.join(row)
        # print row['tweetID'], row['tweetText']
        to = TweetObject(row)
        tweetObjectList.append(to)
        if linectr == 10:
            break

for to in tweetObjectList:
    print(to.userID, ' ', to.tweetText, ' ', to.sentiment)
    classifyWord(to)
    # print '\n'

with open('../dataset/tweet2.csv', 'rb') as csvfile:
    tweetreader = csv.DictReader(csvfile)
    linectr = 0
    
    for row in tweetreader:
        linectr += 1
        # print', '.join(row)
        # print row['tweetID'], row['tweetText']
        to = TweetObject(row)
        print(to.tweetText, " ", getTweetSentiment(to))
        if linectr == 10:
            break

