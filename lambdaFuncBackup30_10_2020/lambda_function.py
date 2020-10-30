import json
import logging
import sys
import os
from uuid import uuid4

from database_wrapper import Db
from model import *

DB_TABLE_NAME = "TEST_database"
LAST_TWEET_TABLE_NAME = "TEST_TweetId"
LAST_TWEET_KEY = "007"

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

def lambda_handler(event, context):
    logger.debug("Starting lambda, connecting to DynamoDB")
    database = Db(logger)
    
    api = authenticate()
    
    my_name = api.me().screen_name
    logger.debug("Authenticating as ({}): {}".format(my_name, "SUCCESS" if api is not None else "FAILURE"))
    
    
    logger.debug(f"Attempted to read last_tweet_id from table {LAST_TWEET_TABLE_NAME}")
    last_tweet_id = database.read_from_database("key", LAST_TWEET_KEY, LAST_TWEET_TABLE_NAME)
    last_tweet_id_item = {"key": LAST_TWEET_KEY, "value": last_tweet_id}
    logger.debug(f"last_tweet_id_item: {str(last_tweet_id_item)}")
    
    try:
        x = int(last_tweet_id_item["value"])
    except:
        x = None
    
    if x is not None:
        logging.debug(f"Last Tweet added to database was {x}. Getting all mentions since then...")
        recent_mentions = get_mentions(api, x) 
    else:
        recent_mentions = get_mentions(api)
    
    logger.debug(f"Getting Mentions: {len(recent_mentions)} found")

    tweet_list = [] # Tweets to 'batch write' to DB

    for mention in reversed(recent_mentions):
        logger.debug(f"Processing Tweet: {mention.id} sent from user: {mention.user.screen_name} ...")

        if mention.is_quote_status:
            logger.debug(f"Tweet {mention.id} is being processed as type 'quote'.")
            json_tweet = process_quote(api, mention)
        
        elif isinstance(mention.in_reply_to_status_id, int): 
            logger.debug(f"Tweet {mention.id} is being processed as type 'reply'.")
            json_tweet = process_reply(api, mention)
            
        else:
            logger.debug(f"Tweet {mention.id} is being processed as type 'other'.")
            json_tweet = process_mention(mention)

        logger.debug(f"Extracting data from tweet: {mention.id} ...")
        filtered_data = parse_tweet_data(json_tweet)
        filtered_data["entry_added_by"] = my_name # add bot screen_name
        filtered_data["uid"] = str(uuid4()) # unique identifier
        cleaned_data = cleanup_data(filtered_data)

        #logger.debug(f"Adding tweet: {mention.id} to table {DB_TABLE_NAME}")
        #database.add_to_database(cleaned_data, TABLE_NAME)
    
        tweet_list.append(cleaned_data)
        
    logger.debug(f"Adding {len(tweet_list)} tweets to table {DB_TABLE_NAME} as a 'batch write' process")
    database.add_to_database_as_batch(tweet_list, DB_TABLE_NAME)
    
    # Update last tweet variable...
    if len(recent_mentions) >= 1:
        last_mention = recent_mentions[0]
        last_tweet_id_item["value"] = last_mention.id
        logger.debug(f"Attempting to update {LAST_TWEET_TABLE_NAME} with value: {str(last_tweet_id_item)}")
        database.add_to_database(last_tweet_id_item, LAST_TWEET_TABLE_NAME)
    
    
    
    return {
        'statusCode': 200,
        'body': json.dumps('Successful execution of the bot lambda.')
    }

