import tweepy
import complimentScrape
import csv
import time
import json
import secrets


def appendToFile(filename, message):
	with open(filename, 'a') as f:
		f.write(message + '\n')


def printTweetInfo(data):
	content = data.text
    username = data.user.screen_name
    tweet_id = str(data.id)
    print "tweet: \"" + content + "\" by user: " + username + " tweet_id: " + tweet_id


def printTweetResponse(message):
    print "response: " + message


#Extract compliments from web page
complimentScrape.parseCompliments()


#Authorization steps
C_KEY = secrets.C_KEY
C_SECRET = secrets.C_SECRET
A_TOKEN = secrets.A_TOKEN
A_SECRET = secrets.A_SECRET

auth = tweepy.OAuthHandler(C_KEY, C_SECRET)
auth.set_access_token(A_TOKEN, A_SECRET)

api = tweepy.API(auth)


#Process and respond to tweets tracked by stream
class MyStreamListener(tweepy.StreamListener):

	def on_status(self, data):
		
		printTweetInfo(data)

		compliment = complimentScrape.getRandCompliment()

		try:
			if(data.user.screen_name != "bot2mouth"):
				message = '@' + data.user.screen_name + " " + compliment.lower() + " #haveacompliment"
				printTweetResponse()

				api.update_status(message, in_reply_to_status_id = data.id)

				log = "Responded to user " + data.user.screen_name + " on " + time.strftime('%a, %d %b %H:%M:%S', time.localtime())
				appendToFile('statusreport.txt', log)

		except tweepy.TweepError as e: #tweepy.error.TweepError
			print e
			print e.response.message

	def on_error(self, error_code):
		if error_code == 420:
			print "Yo ass gettin rate limited"
			return False


#Instantiate stream listener and track tweets containing #sad
mystreamListener = MyStreamListener();

stream = tweepy.Stream(auth = api.auth, listener = MyStreamListener())

stream.filter(track=['#sad'])

message = "Script crashed at " + time.strftime('%a, %d %b %H:%M:%S', time.localtime())
appendToFile('statusreport.txt', message)



