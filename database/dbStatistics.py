import firebase
import json
firebase_URL = 'https://bitcoinsentiment.firebaseio.com/'


def putWord(word, pos, lpos, neut, neg, lneg):
    firebase.put(firebase_URL + word, {'pos': pos, 'lpos': lpos, 'neut': neut, 'neg': neg, 'lneg': lneg})

# this is possible since the get result of Firebase is already a JSON
def getWord(word):
    weightedWordDict = getAllWeightedWords()
    return weightedWordDict[word]

def getAllWeightedWords():
    return firebase.get(firebase_URL)


def getNumberOfPositiveTweets():
    sumPos = 0
    weightedWordDict = getAllWeightedWords()
    for w in weightedWordDict:
        print(weightedWordDict[w]['lpos'])
        sumPos += int(weightedWordDict[w]['lpos']) +  int(weightedWordDict[w]['pos'])
    return sumPos
    
def getNumberOfNegativeTweets():
    sumNeg = 0
    weightedWordDict = getAllWeightedWords()
    for w in weightedWordDict:
        print(weightedWordDict[w]['lpos'])
        sumNeg += int(weightedWordDict[w]['lneg']) +  int(weightedWordDict[w]['neg'])
    return sumNeg

def getNumberOfTweets():
    return len(getAllWeightedWords())
