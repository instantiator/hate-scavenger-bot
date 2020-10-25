import tweepy
import logging
import os
import json
from datetime import datetime
from typing import List

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

def get_mentions(api) -> List:
    return api.mentions_timeline(count=100)


def process_quote(api, tweet) -> str:
    notify_text = tweet.text
    quoted_message_id = tweet.quoted_status_id
    target_tweet = api.get_status(quoted_message_id)

    notify = {"notify_text": notify_text, 
              "notify_tweet_id": tweet.id,
              "notify_is_reply": False,
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
    
    recent_mentions = get_mentions(api)
    logging.info(f"Getting Mentions: {len(recent_mentions)} found")

    for mention in recent_mentions:
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
        cleaned_data = cleanup_data(filtered_data)

        logging.info(f"Adding tweet: {mention.id} to the database ...")
        database_filename = os.path.join(OUTPUT_DIR, "database.txt")
        add_to_database(cleaned_data, database_filename)


    logging.info("======================================\n")
    exit(0)
