import firebase
import json
import MySQLdb
firebase_URL = 'https://bitcoinsentiment.firebaseio.com/'

conn = MySQLdb.connect('localhost', 'ExpressJS2016', 'twitter123','test', charset ='utf8', use_unicode = True)
cursor = conn.cursor()
cursor.execute('SET NAMES utf8mb4')
cursor.execute("SET CHARACTER SET utf8mb4")
cursor.execute("SET character_set_connection=utf8mb4")


def getNumberOfTweets():
    # tweetNum
    cursor.execute("SELECT COUNT(*) FROM traintweet")
    tweetNum = cursor.fetchone()
    #print tweetNum[0]
    return tweetNum[0]

def getNumberOfPositiveTweets():
    # numPositive
    cursor.execute("SELECT COUNT(*) FROM traintweet WHERE BestSentiment > 0")
    posNum = cursor.fetchone()
    #print posNum[0]
    return posNum[0]

def getNumberOfNegativeTweets():
    # numNegative
    cursor.execute("SELECT COUNT(*) FROM traintweet WHERE BestSentiment < 0")
    negNum = cursor.fetchone()
    #print negNum[0]
    return negNum[0]


def putWord(word, pos, lpos, neut, neg, lneg):
    cursor.execute("INSERT INTO trainfeature (word, pos, lpos, neut, neg, lneg) VALUES (%s, %s, %s, %s, %s, %s)",
                    (word, pos, lpos, neut, neg, lneg))
    conn.commit()
    #firebase.put(firebase_URL + word, {'pos': pos, 'lpos': lpos, 'neut': neut, 'neg': neg, 'lneg': lneg})

# this is possible since the get result of Firebase is already a JSON
def getWord(word):
    weightedWordDict = getAllWeightedWords()
    return weightedWordDict[word]


def getAllWeightedWords():
    cursor = conn.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('''SELECT word, pos, lpos, neut, neg, lneg FROM trainfeature''')
    results = cursor.fetchall()
    lol = {}
    for row in results:
        row = {row['word']: {'pos': int(row['pos']), 'lpos': int(row['lpos']), 'neut': int(row['neut']), 'neg': int(row['neg']), 'lneg': int(row['lneg'])}}
        lol.update(row)
   
    return lol

    #return firebase.get(firebase_URL)

#print getAllWeightedWords()
"""
def getNumberOfPositiveTweets():
    sumPos = 0
    weightedWordDict = getAllWeightedWords()
    for w in weightedWordDict:
        print weightedWordDict[w]
        sumPos += int(weightedWordDict[w]['lpos']) +  int(weightedWordDict[w]['pos'])
    return sumPos
    
def getNumberOfNegativeTweets():
    sumNeg = 0
    weightedWordDict = getAllWeightedWords()
    for w in weightedWordDict:
        sumNeg += int(weightedWordDict[w]['lneg']) +  int(weightedWordDict[w]['neg'])
    return sumNeg

def getNumberOfTweets():
    return len(getAllWeightedWords())
"""