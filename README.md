# hate-scavenger-bot

## Last Update
5/11/2020

## Introduction

This project about collecting examples of HateSpeech on Twitter. The core idea is that a Twitter User sees a hateful tweet and mentions the bot. The bot then adds the tweet (and other relevant metadata) to a database.

The goal of the project is to provide researchers a large corpus of text with which to study *(and/or train machine learning models on)* Hate speech on Twitter.

At present, **we do nothing with the data** (i.e we do not notify police or any other agency). 

## How to use it

To use the bot, simply reply to a hateful tweet on Twitter mentioning the bot (i.e. @theHateHawk). The bot will then do the rest. 

## Request Data Access

If you are a researcher and would like access to the dataset, please contact one of the project contributors, briefly detailing your project. 

## Follow us on Twitter
@theHateHawk

# Technical Details

The code for this project is written in Python and we use the "Tweepy" library as a 'middleman' between us and the Twitter API. 

The code is hosted on AWS (lambda) and every 15mins we boot up the bot and add any new mentions to a Dynamo DB database. A copy of the code running on AWS can be found in the "lambdaFuncBackup" folder (The 'tweepy-layer' folder is everything we use for the AWS lambda's function layer). 

Note that the code can be run locally as well (this is mainly for testing) in which case the 'database' is replaced with text files. To run in this way, simply give 'auth.py' your Twitter dev keys and tokens and run 'model.py'

## Database

### Explanatory Notes

Please not that where "NULL" is a datatype this means that the value 'True' in the dataset means that the value is NULL *(this just seems to be a quirk of how DynamoDB operates)*.  

For Example, 'notify_text' has the type String/NULL which means in that dataset you will often see entries like this:
- notify_text: True  # <= this means notify text is NULL
- notify_text: "hello world"

### Database Columns

Format:

- **Column Name**: <DataType(s)> - *Explanation*

...

- **uid**: String - *Primary Key, a unique Identifier for each entry in the database.*
- **created_at**: String - *a datetime string in ISO 8601 format. The time the 'offensive tweet' was posted on Twitter.*
- **entry_added_by**: String - *Name of the bot/user that added this entry to the database.*
- **favorite_count**: Integer - *Number of times the 'offensive tweet' has been favorited.*
- **retweet_count**: Integer - *Number of times the 'offensive tweet' has been retweeted.*
- **geo**: ??/NULL - *Geographic data (if known)*
- **id**: Integer - *Tweet id of the 'offensive tweet'.*
- **lang**: String - *Two-Character codes (ISO 639) denoting the Language the 'offensive tweet' was written in.*
- **screen_name**: String - *Twitter username, author of the 'offensive tweet'.*
- **text**: String - *The 'offensive tweet' itself.*
- **was_reply_to_id**: Integer/NULL - *Tweet Id of the tweet the 'offensive tweet' was replying to.*
- **was_reply_to_text**: String/NULL - *If the 'offensive tweet' was a reply to another tweet, this is the text of tweet that was replied to.*
- **was_retweet_of_id**: Integer/NULL - *Twitter Id of the tweet the 'offensive tweet' was quoting.*
- **was_retweet_of_text**: String/NULL - *If the 'offensive tweet' quoted a tweet, this is the text of that quoted tweet.*
- **notify_is_reply**: Bool - *Has the notifier replied to the 'offensive tweet'.*
- **notify_is_retweet**: Bool - *Has the notifier 'quoted' the 'offensive tweet'.*
- **notify_screen_name**: String/NULL - *Twitter username, the person notifying us about the 'offensive tweet'.*
- **notify_text**: String/NULL - *The 'notifying tweet'. This may contain additional information/context about the 'offensive tweet'.*
- **notify_tweet_id**: Integer/NULL - *Tweet id of the 'notifying tweet'.*