import parseTweet

# Retrieves data from database
from dbStatistics import *

def getWordOccurence():
    # dbStatistics function that returns a list of 'key':[pos, neu, neg]
    return getKeyAndValue()

def calculateSentiment(_words, _wordOccurenceValues):

    tweetWordProbability = []

    probabilityOfFeatures = 1
    probOfFeatureWithKnownValue = 1
    
    # dbStatistics will handle the following functions
    # P ( Value )
    totalNumberOfPositiveTweets = getNumberOfPositiveTweets()
    totalNumberOfTweets = getNumberOfTweets()

    probabilityOfValue = totalNumberOfPositiveTweets/totalNumberOfTweets
    
    # P ( Feature )
    for word in _words:
        listOfValues = _wordOccurenceValues[word]
        sum = 0
        
        for value in listOfValues:
            sum += value

        tweetWordProbability.append(sum/totalNumberOfTweets)

    
    for probability in tweetWordProbability:
        probabilityOfFeatures *= probability

    # P ( Feature | Value )
    for word in _words:
        listOfValues = _wordOccurenceValues[word]
        
        # Maximum value of the list
        if(max(listOfValues) == listOfValues[neu])
            continue
        
        # Getting only the positive value
        value = listOfValues[pos] 
        probabilityOfFeatureWithKnownValue *= value/totalNumberOfPositiveTweets

    return (probabilityOfValue * probabilityOfFeatureWithKnownValue)/probilityOfFeatures

def getTweetSentiment(_tweetObject):
    # Get dictionary of <word, list of values (pos, neu, neg)>
    wordOccurenceValues = getWordOccurence()
    
    # Get necessary values from TweetObject
    words = _tweetObject.getWords()

    # Determine the total value of the tweet
    return calculateSentiment(words, wordOccurenceValues)
