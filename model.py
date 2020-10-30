import tweepy
import logging
import os
import json
from datetime import datetime
from typing import List, Optional
from uuid import uuid4

from auth import API_KEY, API_SECRET_KEY, ACCESS_TOKEN, ACCESS_TOKEN_SECRET, BEARER_TOKEN
from helperMethods import parse_tweet_data, cleanup_data


def authenticate():
    """
    Sign in and return Api
    """

    auth = tweepy.OAuthHandler(API_KEY, API_SECRET_KEY)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

    api = tweepy.API(auth)
    return api

def get_mentions(api, since:int=None) -> List:
    if since is not None:
        return api.mentions_timeline(since_id=since,count=999)

    return api.mentions_timeline(count=999)


def process_quote(api, tweet) -> str:
    notify_text = tweet.text
    quoted_message_id = tweet.quoted_status_id
    target_tweet = api.get_status(quoted_message_id)

    notify = {"notify_text": notify_text, 
              "notify_tweet_id": tweet.id,
              "notify_is_reply": None,
              "notify_is_retweet": tweet.is_quote_status, 
              "notify_screen_name": tweet.user.screen_name }
    
    json_tweet = target_tweet._json
    json_tweet.update(notify)
    return json.dumps(json_tweet)


def process_reply(api, tweet) -> str:
    notify_text = tweet.text
    reply_id: int = tweet.in_reply_to_status_id
    target_tweet = api.get_status(reply_id)

    notify = {"notify_text": notify_text, 
              "notify_tweet_id": tweet.id,
              "notify_is_reply": reply_id,
              "notify_is_retweet": tweet.is_quote_status, 
              "notify_screen_name": tweet.user.screen_name }



    json_tweet = target_tweet._json
    json_tweet.update(notify)
    return json.dumps(json_tweet)


def process_mention(tweet) -> str:
    json_tweet = tweet._json
    return json.dumps(json_tweet)


def get_most_recent_tweet_id_from_database(file:str) -> Optional[int]:
    """
    Figure out the last tweet we added to the database, 
    return the id of that.

    Returns None for empty database
    """

    ## As a tmp measure, we are saving/reading this value from a file.
    if not os.path.exists(file):
        return None
    
    tweet_id = None
    with open(file, "r") as f:
        tweet_id = int(f.readline())

    return tweet_id

def set_most_recent_tweet_id_in_database(file:str, tweet_id:int):
    ## As a tmp measure, we are saving/reading this value from a file.
    with open(file, "w") as f:
        f.write(str(tweet_id))


def add_to_database(tweet, filepath):
    with open(filepath,"a") as f:
        f.write(json.dumps(tweet))
        f.write("\n")


if __name__ == '__main__':

    OUTPUT_DIR = os.path.join(os.path.dirname(os.path.realpath(__file__)), "output")
    if not os.path.exists(OUTPUT_DIR):
        os.mkdir(OUTPUT_DIR)

    log_filepath = os.path.join(OUTPUT_DIR, "model.log")
    logging.basicConfig(filename=log_filepath, level=logging.INFO) # DEBUG level also seems to get information from tweepy itself.

    logging.info(f"Running application at: {datetime.now()}")

    api = authenticate()
    my_name = api.me().screen_name
    logging.info("Authenticating as ({}): {}".format(my_name, "SUCCESS" if api is not None else "FAILURE"))

    ## Only attempt to process mentions we have not previously added to DB
    database_last_tweet_filename = os.path.join(OUTPUT_DIR, "last_tweet_id.txt")
    last_tweet_added_id = get_most_recent_tweet_id_from_database(database_last_tweet_filename)
    if last_tweet_added_id is not None:
        logging.info(f"Last Tweet added to database was {last_tweet_added_id}. Getting all mentions since then...")
        recent_mentions = get_mentions(api, last_tweet_added_id) 
    else:
        recent_mentions = get_mentions(api)

    logging.info(f"{len(recent_mentions)} Mentions found")

    for mention in reversed(recent_mentions): # mentions is effectively a queue where first is most recent. Best to feed in oldest first (hence reversed).
        logging.info(f"Processing Tweet: {mention.id} sent from user: {mention.user.screen_name} ...")

        if mention.is_quote_status:
            logging.info(f"Tweet {mention.id} is being processed as type 'quote'.")
            json_tweet = process_quote(api, mention)
        
        elif isinstance(mention.in_reply_to_status_id, int): 
            logging.info(f"Tweet {mention.id} is being processed as type 'reply'.")
            json_tweet = process_reply(api, mention)
            
        else:
            logging.info(f"Tweet {mention.id} is being processed as type 'other'.")
            json_tweet = process_mention(mention)

        logging.info(f"Extracting data from tweet: {mention.id} ...")
        filtered_data = parse_tweet_data(json_tweet)
        filtered_data["entry_added_by"] = my_name # add bot screen_name
        filtered_data["uid"] = str(uuid4()) # unique identifier
        cleaned_data = cleanup_data(filtered_data)

        logging.info(f"Adding tweet: {mention.id} to the database ...")
        database_filename = os.path.join(OUTPUT_DIR, "database.txt")
        add_to_database(cleaned_data, database_filename)

    if len(recent_mentions) >= 1:
        logging.info(f"Setting 'Last_tweet_id' to value: {recent_mentions[0].id}")
        set_most_recent_tweet_id_in_database(database_last_tweet_filename, recent_mentions[0].id)

    logging.info(f"All processing completed at: {datetime.now()}")
    logging.info("======================================\n")
    exit(0)
