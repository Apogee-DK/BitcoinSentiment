from twitter import *
from twitter.stream import *
from datetime import datetime, time
import io, os, errno, time, re, csv, urllib2, datetime, time, urllib, json, requests
import httplib
from requests.exceptions import *
from urllib2 import *
from decimal import *

# set up OAUTH
def connectTwitter():

    # Variables that contains the user credentials to access Twitter API 
    ACCESS_TOKEN = "4184038576-UNMwtrHiJWLSARuBeWLmEULfxsQyPxUCPs3dyqB"
    ACCESS_SECRET = "MIrhNZoXfhaCuMMMiRNGTkk3Y1hqQhXpNNPTxH1or3JQZ"
    CONSUMER_KEY = "IEzSw6OTfJbn8LmWK1raEiu1q"
    CONSUMER_SECRET = "eNQLpiZavSGoWhxfK3aIaF9fZJOMN1K6ZAd02wxCF7PQSnhliQ"

    oa = OAuth(ACCESS_TOKEN, ACCESS_SECRET, CONSUMER_KEY, CONSUMER_SECRET)

    return oa
	
def twitterParseText(tweet_count,keyword):
    # connect to MySQL database & cursor
    # This version should work when ran under cmd...
    # conn = MySQLdb.connect('localhost', 'ExpressJS2016', 'twitter123','test', charset ='utf8', use_unicode = True)
    # cursor = conn.cursor()
    # cursor.execute('SET NAMES utf8mb4')
    # cursor.execute("SET CHARACTER SET utf8mb4")
    # cursor.execute("SET character_set_connection=utf8mb4")
	
    # Initiate the connection to Twitter Streaming API
    twitter_stream = TwitterStream(auth = connectTwitter())
    #t = Twitter(auth = connectTwitter())

    # Print each tweet in the stream to the screen 
    # You don't have to set it to stop, but can continue running 
    # the Twitter API to collect data for days or even longer. 
    searchCount = 0
    checkCreation = 0
    tweetCount = 0    

    # store into array
    searchArr = []

    # Get a sample of the public data following through Twitter
    while True:

        try:
            
            # connection tryout
            iterator = twitter_stream.statuses.filter(track=keyword, language="en", retry="true", stall_warnings = 'true', filter_level = 'none')
            print "-- Successfully connected to TwitterStream! --"
            arr = []
            count = 0

            # loop through the tweets
            for tweet in iterator:

                # catch ValueError and IO problems within the loop..    
                try:
                    
                    if datetime.datetime.now().minute % 30 == 0 and datetime.datetime.now().second >= 10 and datetime.datetime.now().second <= 30:
                        tweet_count -=1
                        time.sleep(5)
                        break

                    # if it gets timeout, continue..
                    if not tweet or tweet.get("timeout"):
                        continue

                    # if disconnects or hangup, just break from the for loop and re-issue connection
                    if tweet.get("disconnect") or tweet.get("hangup"):
                        print "WARNING Stream connection lost: %s" % (tweet)
                        break

                    # only proceed if iterator returns text
                    if tweet.get('text'):

                        # reopen the workbook with the corresponding worksheet, given that the workbook has been closed after wb.save
                       

                        # add JSON content into array
                        arr.append(json.dumps(tweet))
                    
                        # Read in one line of the file, convert it into a json object 
                        tweet = json.loads(arr[count])
  

                        # only considers non empty texts
                        if 'text' in tweet and not (tweet['text'] is None) and not (tweet['text'] == "") and tweet['retweeted'] is False: # only messages contains 'text' field is a tweet

                            # encode fix for unicode problems..
                            tempText = tweet['text'].encode('utf-8', errors='ignore')
                            tempText = removeNonEnglishWords(tempText).encode('utf-8', errors='replace')
                            #tweet['text'] = normalize(tweet['text'])
                            # extract tweet and apply tokenization with stop words
                            #parsedText = getTokenization(filterTweet(tweet['text']), stopwords)
                             
                            # save hashtags into an array, then convert into a string concatenated with commas
                            hashtags = []
                            for hashtag in tweet['entities']['hashtags']:
                                hashtag['text'] = removeNonEnglishWords(hashtag['text'])
                                hashtags.append(hashtag['text'])

                            datetimeStamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                            # print tweet info:
                            print "tweet #" + str(tweetCount + 1) + ":"
                            print "time: ", datetimeStamp
                            print tempText # content of the tweet
                            print "user: ", tweet['user']['name'] # id of user
                            print "user id: ", tweet['user']['id']
                            print "hashtag: " + ','.join(hashtags)
                            
                            # if we are looking for Bitcoin tweets, we store their price at the time of the search
                            results = json.loads(urlopen('https://www.bitstamp.net/api/v2/ticker/btcusd/').read())
                            #results = json.loads(requests.get('https://www.bitstamp.net/api/v2/ticker/btcusd/').content)
                            price, volume, bid, ask, vwap = Decimal(results['last']), Decimal(results['volume']), Decimal(results['bid']), Decimal(results['ask']), Decimal(results['vwap'])
			                # cursor.execute("INSERT INTO bitcoinParser (tweetID, userID, userName, tweetText, hashtags, btcPrice, btcBid, btcAsk, btcVwap, btcVolume, timeStamp) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                            #               (tweet['id_str'], tweet['user']['id'], tweet['user']['name'], tempText,','.join(hashtags), price, bid, ask, vwap, volume, datetimeStamp))
                
                            """

                            else:
                                
                                # USDJPY:CUR for USDJPY
                                if re.search(r'\busd/jpy\b', tweet['text'].lower()) or re.search(r'\busd jpy\b', tweet['text'].lower()) or re.search(r'\busd\b', tweet['text'].lower()):
                                    price = str(bbgPrice("USDJPY:CUR"))

                                # only get these info during market hours
                                else:

                                    #if currTime.hour >= 7 and currTime.minute >= 0 and currTime.second >= 0 and currTime.hour <= 19:
                                        
                                    # FB:US for facebook
                                    if re.search(r'\bfb\b', tweet['text'].lower()) or re.search(r'\bfacebook\b', tweet['text'].lower()):
                                        price = str(bbgPrice("FB:US"))

                                    # AAPL:US for AAPL
                                    elif re.search(r'\baapl\b', tweet['text'].lower()) or re.search(r'\bapple\b', tweet['text'].lower()):
                                        price = str(bbgPrice("AAPL:US"))

                                    # GOOG:US for GOOGLE
                                    elif re.search(r'\bgoog\b', tweet['text'].lower()) or re.search(r'\bgoogle\b', tweet['text'].lower()):
                                        price = str(bbgPrice("GOOG:US"))

                                    # SPY:US for SPY
                                    elif re.search(r'\bspy\b', tweet['text'].lower()):
                                        price = str(bbgPrice("SPY:US"))
                                        
                                    # SPX:US for SPX
                                    elif re.search(r'\bspx\b', tweet['text'].lower()):
                                        price = str(bbgPrice("SPX:IND"))
                                
                                    else:
                                        price = ""


                                ws.cell(column = 6, row = rowCount, value = price)
                                cursor.execute("INSERT INTO stocks (tweetID, userID, userName, tweetText, hashtags, price, timeStamp) VALUES (%s,%s,%s,%s,%s,%s,%s)",
                                                (tweet['id_str'], tweet['user']['id'], tweet['user']['name'], tweet['text'],','.join(hashtags), price, datetimeStamp))
                                    

                            """                  
                            # save into database    
                            # conn.commit()
                            print "price:  ", price
                            print "volume: ", volume
                            print ""
  

                except ValueError, err:
                    # read in a line is not in JSON format (sometimes error occured)
                    print str(err) + " time: " + str(datetime.datetime.now())
                    break

                except IOError, err:
                    print str(err) + " time: " + str(datetime.datetime.now())
                    break

                except IndexError as err:
                    print "list index out of range.."
                    continue


                # break..
                if tweet_count < 0:
                    break

                # counter iterations
                tweet_count -= 1
                count +=1
                tweetCount += 1

        # error handles
        except(TwitterHTTPError, httplib.BadStatusLine, URLError, SSLError, socket.error) as e:
            print("WARNING: Stream connection lost, reconnecting in a sec... (%s: %s)" % (type(e), e))
            continue 

        except urllib2.HTTPError,err:
            print str(err.code) + " time: " + str(datetime.datetime.now())
            continue    

        except KeyboardInterrupt:
            print ("closing streamer...")
            break


    # Finalize MySQL database
    # conn.commit()
    # cursor.close()
    # conn.close()

    # close workbook
    # wb.save(wbname)

    '''
    # wake me up fuck...
    speech_engine = pyttsx.init()
    iterate = 20

    while iterate > 0:
        speech_engine.say("ERROR")
        speech_engine.runAndWait()
        iterate -= 1
        continue
    '''	

def removeNonEnglishWords(tweet):

    newTweet = []

    # remove all non-unicode characters
    for i in range(len(tweet)):
        if tweet[i] != '':
            chk = re.match(r'([a-zA-z0-9 \+\?\.\*\^\$\(\)\[\]\{\}\|\\/:;\'\"><,.#@!~`%&-_=])+$', tweet[i])
            if chk:
                newTweet.append(tweet[i])

    #return as string
    return "".join(newTweet)

			
def main():    
    # define new keywords
    keywords = u"""bitcoin rise, bitcoin fall, bitcoin increase, bitcoin decrease, Bitcoin feel, $BTC feel, Bitcoin happy, $BTC happy, Bitcoin great, $BTC great, Bitcoin love, $BTC love, Bitcoin awesome, $BTC awesome,
                  Bitcoin lucky, $BTC lucky, Bitcoin good, $BTC good, Bitcoin sad, $BTC sad, BTCUSD, $BTCUSD, #bitcoin bearish, bitcoin bearish, btc bearish, btc bullish, bitcoin bullish, 
                  #bitcoin bullish, $btc bearish, bitcoin bear, btc bear, $btc bear, bitcoin bull, #bitcoin bull, bitcoin bearish, bitcoin bullish,
                  Bitcoin bad, $BTC bad, Bitcoin upset, $BTC upset, Bitcoin unhappy, $BTC unhappy, Bitcoin nervous, $BTC nervous, Bitcoin hope, $BTC hope,
                  Bitcoin fear, $BTC fear, Bitcoin worry, $BTC worry"""
    #$AAPL, $AAPL Apple, $FB, $FB Facebook, $GOOG, $GOOG google,$SPY, $SPX
    # run through the codes
    # spaces = AND, commas = OR
    twitterParseText(100000002, keywords)


main()
