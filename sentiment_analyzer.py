#Textblob sentiment analysis tweepy
import os
from textblob import TextBlob
import pandas as pd
import tweepy

#----------------------------------------------------------------------
#Twitter API credentials
'''
access_token="1433202678818017283-Tz047y4zcoa9ivP7r0UHlmuko2MqKd"
access_token_secret="OeubpAnY4u0yPp0Pckcor6589hNB9gU06dojxRGf2jw8A"
API_key="qfOhwhutCVNW80q0C4WnXBdPn"
API_secret_key="HAmpbaSuZNWgaAoLi7092QjsH2wS6jsXH991e6fjAJGc4KnIaI"
'''

access_token = os.environ['access_token']
access_token_secret = os.environ['access_token_secret']
API_key = os.environ['API_key']
API_secret_key = os.environ['API_secret_key']

auth = tweepy.OAuthHandler(API_key, API_secret_key)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth, wait_on_rate_limit=True)


#----------------------------------------------------------------------
def user_tweets(twitter_handle):
    user_tweets = api.user_timeline(screen_name=twitter_handle,
                                    count=100,
                                    include_rts=False)

    tweet_ids = []
    tweet_dates = []
    tweet_texts = []

    for tweet in user_tweets:
        tweet_ids.append(tweet.id)
        tweet_dates.append(tweet.created_at)
        tweet_texts.append(tweet.text)

    tweet_user = [twitter_handle] * len(user_tweets)

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
        'Polarity Score': polarity_scores,
        'Subjectivity Score': subjectivity_scores,
    }

    user_tweets_df = pd.DataFrame(user_tweets_dict)
    print(user_tweets_df.head())
    #user_tweets_df.to_csv('/Users/fpriscoll/Desktop/ds3002/twitter_bot_project/textblob_sentiment_analysis/user_tweets_df.csv', index=False)
    return user_tweets_df


#returning tweets and sentiment analysis from a very opionionated person Dave Portnoy head of Barstool Sports

el_pres_tweets_df = user_tweets('@stoolpresidente')
print(el_pres_tweets_df)

#----------------------------------------------------------------------
'''
#BEGINNING APPLICATION OF SENTIMENT ANALYSIS TO TWEETS ABOUT THE US FROM CHINESE LEADERS 
relevant_to_US_words = ['US','U.S.','#US',"US'", 'United States','States',"States'",'America','Biden','NATO','#NATO',"#NATO's"]

test_words = ['Old', 'patrol','Expressways']

### Getting user tweets about the U.S. from user. Assembling the tweets and their seniment analysis in a df
def user_tweets_about_US(twitter_handle):
  user_tweets = api.user_timeline(screen_name= twitter_handle, count=100, include_rts = False)
  relevant_tweets = []
  for tweet in user_tweets:
    tweet_words_list = tweet.text.split() #CONTINUE WORK HERE 01:46 5/04. IS THE SPLIT NOT PROCESSING HASHTAGS AND APOSTROPHES CORRECTLY???
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

  #need to remove urls from text of tweets THIS NEEDS WORK

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
  relevant_tweets_df.to_csv('/Users/fpriscoll/Desktop/ds3002/twitter_bot_project/textblob_sentiment_analysis/relevant_tweets_df.csv', index=False)
  return relevant_tweets_df

#Producing sentiment analysis of China's Foreign Minister's tweets
#user_tweets_about_US('zlj517')

'''
