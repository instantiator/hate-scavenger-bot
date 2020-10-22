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
    return api.mentions_timeline()


def process_quote(api, tweet) -> str:
    explanatory_text = tweet.text
    quoted_message_id = tweet.quoted_status_id
    target_tweet = api.get_status(quoted_message_id)
    
    json_tweet = target_tweet._json
    json_tweet.update({"explantory_text": explanatory_text})
    return json.dumps(json_tweet)


def process_reply(api, tweet) -> str:
    explanatory_text = tweet.text
    reply_id: int = tweet.in_reply_to_status_id
    target_tweet = api.get_status(reply_id)

    json_tweet = target_tweet._json
    json_tweet.update({"explantory_text": explanatory_text})
    return json.dumps(json_tweet)


def process_mention(tweet) -> str:
    json_tweet = tweet._json
    return json.dumps(json_tweet)


def add_to_database(tweet, filepath):
    with open(filepath,"w+") as f:
        f.write(json.dumps(tweet))


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
        logging.info("Processing Tweet: {mention.id} sent from user: {mention.user} ...")

        if mention.is_quote_status:
            logging.info("Tweet {mention.id} is being processed as type 'quote'.")
            json_tweet = process_quote(api, mention)
        
        elif isinstance(mention.in_reply_to_status_id, int): 
            logging.info("Tweet {mention.id} is being processed as type 'reply'.")
            json_tweet = process_reply(api, mention)
            
        else:
            logging.info("Tweet {mention.id} is being processed as type 'other'.")
            json_tweet = process_mention(mention)

        json_string = json.dumps(json_tweet)

        logging.info(f"Extracting data from tweet: {mention.id} ...")
        filtered_data = parse_tweet_data(json_string)
        logging.info(f"Cleaning and anonymizing extracted data from tweet: {mention.id}")
        cleaned_data = cleanup_data(filtered_data)

        logging.info("Adding tweet: {mention.id} to the database ...")
        database_filename = os.path.join(OUTPUT_DIR, "database.txt")
        add_to_database(cleaned_data, database_filename)


    logging.info("======================================\n")
