import csv


class TweetObject():
    def __init__(self):



    def getWords():
        # return all words after normalization
    

with open('../tweet1.csv', 'rb') as csvfile:
    # tweetreader = csv.reader(csvfile)
    tweetreader = csv.DictReader(csvfile)
    linectr = 0
    
    for row in tweetreader:
        linectr += 1
        # print', '.join(row)
        print row['tweetID'], row['tweetText']
        if linectr == 10:
            break
