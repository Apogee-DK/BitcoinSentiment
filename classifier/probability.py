# import parseTweet

# Retrieves data from database
# from dbStatistics import *

def getfeatureOccurence():
    # dbStatistics function that returns a list of 'key':[pos, neu, neg]
    return getKeyAndValue()

def calculateSentiment(_features, _featureOccurenceValues):

    tweetWordProbability = []

    probabilityOfFeatures = 1.0
    probabilityOfFeatureWithKnownValue = 1.0
    
    # dbStatistics will handle the following functions
    # P ( Value )
    # Must provide floating number
    totalNumberOfPositiveTweets = getNumberOfPositiveTweets()
    totalNumberOfTweets = float(getNumberOfTweets())
    
    # for unit_test
    # totalNumberOfPositiveTweets = 26
    # totalNumberOfTweets = 50

    probabilityOfValue = totalNumberOfPositiveTweets/totalNumberOfTweets
    
    # P ( Feature )
    for feature in _features:
        listOfValues = _featureOccurenceValues[feature]
        sum = 0

        if(listOfValues['neut'] < listOfValues['pos'] or listOfValues['neut'] < listOfValues['neg']):
            sum += listOfValues['pos'] + listOfValues['neut'] + listOfValues['neg']
            tweetWordProbability.append(sum/totalNumberOfTweets)
    
    for probability in tweetWordProbability:
        probabilityOfFeatures *= probability

    # P ( Feature | Value )
    for feature in _features:
        listOfValues = _featureOccurenceValues[feature]
        
        # Maximum value of the list
        if(listOfValues['neut'] < listOfValues['pos'] or listOfValues['neut'] < listOfValues['neg']):
            probabilityOfFeatureWithKnownValue *= listOfValues['pos']/totalNumberOfPositiveTweets
        
    return (probabilityOfValue * probabilityOfFeatureWithKnownValue)/probabilityOfFeatures

def getTweetSentiment(_tweetObject):
    # Get dictionary of <word, list of values (pos, neu, neg)>
    featureOccurenceValues = getfeatureOccurence()
    
    # Get necessary values from TweetObject
    features = _tweetObject.getFeatures()

    # Determine the total value of the tweet
    return calculateSentiment(features, featureOccurenceValues)

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

