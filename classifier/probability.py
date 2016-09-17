import parseTweet

# Retrieves data from database
from dbStatistics import *

def getfeatureOccurence():
    # dbStatistics function that returns a list of 'key':[pos, neu, neg]
    return getKeyAndValue()

def calculateSentiment(_features, _featureOccurenceValues):

    tweetWordProbability = []

    probabilityOfFeatures = 1
    probOfFeatureWithKnownValue = 1
    
    # dbStatistics will handle the following functions
    # P ( Value )
    totalNumberOfPositiveTweets = getNumberOfPositiveTweets()
    totalNumberOfTweets = getNumberOfTweets()

    probabilityOfValue = totalNumberOfPositiveTweets/totalNumberOfTweets
    
    # P ( Feature )
    for feature in _features:
        listOfValues = _featureOccurenceValues[feature]
        sum = 0
        
        for value in listOfValues:
            sum += value

        tweetWordProbability.append(sum/totalNumberOfTweets)

    
    for probability in tweetWordProbability:
        probabilityOfFeatures *= probability

    # P ( Feature | Value )
    for feature in _features:
        listOfValues = _featureOccurenceValues[feature]
        
        # Maximum value of the list
        if(max(listOfValues) == listOfValues[neut])
            continue
        
        # Getting only the positive value
        value = listOfValues[pos] 
        probabilityOfFeatureWithKnownValue *= value/totalNumberOfPositiveTweets

    return (probabilityOfValue * probabilityOfFeatureWithKnownValue)/probilityOfFeatures

def getTweetSentiment(_tweetObject):
    # Get dictionary of <word, list of values (pos, neu, neg)>
    featureOccurenceValues = getfeatureOccurence()
    
    # Get necessary values from TweetObject
    features = _tweetObject.getFeatures()

    # Determine the total value of the tweet
    return calculateSentiment(features, featureOccurenceValues)
