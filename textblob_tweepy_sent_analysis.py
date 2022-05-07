'''
This program uses the twitter API to gather tweets from a particular user, and then it conducts sentiment analysis on the tweets using TextBlob and returns the tweets and their sentiment analysis scores in a dataframe.

This program was inspired by a project I worked on last semester with a scholar from a foreign affairs think tank as he was trying to scrape tweets for understanding the opinions of politicians.
There are two functions in this program
1. user_tweets() gathers tweets (excluding retweets) in a user's timeline and returns them in a dataframe with sentiment analysis scores attached (polarity and subjectivity scores.)


2. user_tweets_about_US() is more targeted towards my application of submitting to my former manager at the thinktank as this function specifically examines tweets that mention the United States. I have set this function to examine the tweets from China's state media Frontline twitter account


When the program is run, I have programmed it to produce a dataframe of sentiment analysis of Dave Portnoy, the CEO of Barstool Sports, and then I included a line that will allow the user to input an account that they want to see sentiment analysis conducted on. For demonstrating the general sentiment analysis function, I picked Dave Portnoy, the CEO of Barstool Sports as he is one of the most opinionated people I could think of. 

The program will also use the user_tweets_about_US() function to conduct sentiment analysis on tweets from China's state media Frontline twitter account

Within each function, I have provided a line of code that will save the df to a csv file on the user's local device if they edit the line and provide a specific filepath. Sometimes, it is easier to view the dataframes on excel.
'''



#----------------------------------------------------------------------

#Textblob sentiment analysis tweepy
import os
from textblob import TextBlob
import pandas as pd
import tweepy
  
#----------------------------------------------------------------------
#Twitter API credentials

access_token="1433202678818017283-8XmwhxjUB3ua7GrSWpAHfDxDR3FpjI"
access_token_secret="HHl97TpgQ1QziKNiQHa7zMDRQbWfnGbbdHX91TWDij5de"
API_key="aw3pjPT5u0DcB6NJi9GNqsQkM"
API_secret_key="vFM4fIqYvV1DUfZRQdFzfnDKtUQQeGT5zZwdu3ecUWdZ0lFJJP"
'''

access_token = os.environ['access_token']
access_token_secret = os.environ['access_token_secret']
API_key = os.environ['API_key']
API_secret_key = os.environ['API_secret_key']
'''

auth = tweepy.OAuthHandler(API_key, API_secret_key)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth, wait_on_rate_limit=True)

#----------------------------------------------------------------------
def user_tweets(twitter_handle):
  user_tweets = api.user_timeline(screen_name= twitter_handle, count=100, include_rts = False)
  
  tweet_ids = []
  tweet_dates = []
  tweet_texts = []

  for tweet in user_tweets:
    tweet_ids.append(tweet.id)
    tweet_dates.append(tweet.created_at)
    tweet_texts.append(tweet.text)
  
  tweet_user = [twitter_handle]*len(user_tweets)

  #need to remove urls from text of tweets THIS NEEDS WORK

  ### conducting sentiment analysis on text of each tweet
  # initializing lists of each score type
  polarity_scores = []
  subjectivity_scores = []

  for tweet in user_tweets:
    analysis_text = TextBlob(tweet.text)
    
    polarity_scores.append(analysis_text.sentiment.polarity)
    subjectivity_scores.append(analysis_text.sentiment.subjectivity)


  #Producing df with these values
  user_tweets_dict = {
    'Tweet ID': tweet_ids,
    'Tweet Poster': tweet_user,
    'Tweet Date': tweet_dates,
    'Tweet Text': tweet_texts,
    'Polarity Score' : polarity_scores,
    'Subjectivity Score' : subjectivity_scores,
    }
    
  user_tweets_df = pd.DataFrame(user_tweets_dict)
  print(user_tweets_df.head())
  #user_tweets_df.to_csv('/Users/fpriscoll/Desktop/ds3002/twitter_bot_project/textblob_sentiment_analysis/user_tweets_df.csv', index=False)
  return user_tweets_df

#returning tweets and sentiment analysis from a very opionionated person Dave Portnoy head of Barstool Sports

stool_presidente_tweets_df = user_tweets('@stoolpresidente')
print(stool_presidente_tweets_df)

#----------------------------------------------------------------------

#BEGINNING APPLICATION OF SENTIMENT ANALYSIS TO TWEETS ABOUT THE US
relevant_to_US_words = ['US','U.S.','#US',"US'", 'United States','States',"States'",'America','Biden','NATO','#NATO',"#NATO's"]

test_words = ['Old', 'patrol','Expressways']

### Getting user tweets about the U.S. from user. Assembling the tweets and their seniment analysis in a df
def user_tweets_about_US(twitter_handle):
  user_tweets = api.user_timeline(screen_name= twitter_handle, count=100, include_rts = False)
  relevant_tweets = []
  for tweet in user_tweets:
    tweet_words_list = tweet.text.split() 
    for word in tweet_words_list:
      if word in relevant_to_US_words:
      #if word in test_words:
        relevant_tweets.append(tweet)
  tweet_ids = []
  tweet_dates = []
  tweet_texts = []

  for tweet in relevant_tweets:
    tweet_ids.append(tweet.id)
    tweet_dates.append(tweet.created_at)
    tweet_texts.append(tweet.text)
  
  tweet_user = [twitter_handle]*len(relevant_tweets)


  ### conducting sentiment analysis on text of each tweet
  # initializing lists of each score type
  polarity_scores = []
  subjectivity_scores = []

  for tweet in relevant_tweets:
    analysis_text = TextBlob(tweet.text)
    
    polarity_scores.append(analysis_text.sentiment.polarity)
    subjectivity_scores.append(analysis_text.sentiment.subjectivity)


  #Producing df with these values
  relevant_tweets_dict = {
    'Tweet ID': tweet_ids,
    'Tweet Poster': tweet_user,
    'Tweet Date': tweet_dates,
    'Tweet Text': tweet_texts,
    'Polarity Score' : polarity_scores,
    'Subjectivity Score' : subjectivity_scores,
    }
    
  relevant_tweets_df = pd.DataFrame(relevant_tweets_dict)
  print(relevant_tweets_df.head())

print('In order to view the full user_tweets_about_US() df, I think it is easiest to view it as an excel file, so there is a to_csv() function included. If you would like to view csv file in excel please edit the filepath in the line below.')
print('If the .to_csv() line remains commented out and no filepath is provided, the function will just return the new df' )
#relevant_tweets_df.to_csv('ENTER USER SPECIFIC FILEPATH HERE', index=False)
return relevant_tweets_df



#Producing sentiment analysis of China's state media Frontline twitter account
user_tweets_about_US('Frontlinestory')

