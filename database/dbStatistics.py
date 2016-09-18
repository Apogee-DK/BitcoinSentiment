import firebase
import json
firebase_URL = 'https://bitcoinsentiment.firebaseio.com/'


def putWord(word, pos, lpos, neut, neg, lneg):
    firebase.put(firebase_URL + word, {'pos': pos, 'lpos': lpos, 'neut': neut, 'neg': neg, 'lneg': lneg})

def getWord(word):
    # since the json from firebase is encoded as 'u', its extracted now
    # per member, instead of getting it as a whole and parsing the members after
    # consider to improve for performance

    weightedWord = {}
    weightedWord[word] = {}

    # jsonWeights = firebase.get(firebase_URL + word)
    # token = firebase.get(firebase_URL + word)

    weightedWord[word]['pos'] = firebase.get(firebase_URL + word + '/' + 'pos')
    weightedWord[word]['lpos'] = firebase.get(firebase_URL + word + '/' + 'lpos')
    weightedWord[word]['neut'] = firebase.get(firebase_URL + word + '/' + 'neut')
    weightedWord[word]['neg'] = firebase.get(firebase_URL + word + '/' + 'neg')
    weightedWord[word]['lneg'] = firebase.get(firebase_URL + word + '/' + 'lneg')
    
    # print word, ' : ', pos, ' ', lpos, ' ', neut, ' ', neg, ' ', lneg
    
    return weightedWord 

