import tweepy
import json
from typing import List, Optional, Dict, Any

from auth import API_KEY, API_SECRET_KEY, ACCESS_TOKEN, ACCESS_TOKEN_SECRET, BEARER_TOKEN


def authenticate():
    """
    Sign in and return Api
    """

    auth = tweepy.OAuthHandler(API_KEY, API_SECRET_KEY)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

    api = tweepy.API(auth)
    return api

def get_mentions(api, since:Optional[int]=None) -> List:
    num = 100
    if since is not None:
        return api.mentions_timeline(since_id=since,count=num)
    return api.mentions_timeline(count=num)


def process_quote(api, tweet) -> str:
    notify_text = tweet.text
    quoted_message_id = tweet.quoted_status_id
    target_tweet = api.get_status(quoted_message_id)

    notify = {"notify_text": notify_text, 
              "notify_tweet_id": tweet.id,
              "notify_is_reply": False,
              "notify_is_retweet": tweet.is_quote_status, 
              "notify_screen_name": tweet.user.screen_name }
    
    response = response_to(api, target_tweet)

    json_tweet = target_tweet._json
    json_tweet.update(notify)
    json_tweet.update(response)
    return json.dumps(json_tweet)


def process_reply(api, tweet) -> str:
    notify_text = tweet.text
    reply_id: int = tweet.in_reply_to_status_id
    target_tweet = api.get_status(reply_id)

    notify = {"notify_text": notify_text, 
              "notify_tweet_id": tweet.id,
              "notify_is_reply": True if reply_id else False,
              "notify_is_retweet": tweet.is_quote_status, 
              "notify_screen_name": tweet.user.screen_name }

    response = response_to(api, target_tweet)

    json_tweet = target_tweet._json
    json_tweet.update(notify)
    json_tweet.update(response)
    return json.dumps(json_tweet)


def process_mention(tweet) -> str:
    json_tweet = tweet._json

    notify = { "notify_is_reply": False,
               "notify_is_retweet": False }
    
    json_tweet.update(notify)
    return json.dumps(json_tweet)


def response_to(api, tweet) -> Dict[str, Any]:
    data: Dict[str, Any] = {"was_reply_to_id": None, "was_reply_to_text": None,
                            "was_retweet_of_id": None, "was_retweet_of_text": None}
    
    reply_id: int = tweet.in_reply_to_status_id
    if isinstance(reply_id, int): 
        data["was_reply_to_id"] = reply_id

        target_tweet = api.get_status(reply_id)
        data["was_reply_to_text"] = target_tweet.text

    if tweet.is_quote_status:
        quoted_message_id = tweet.quoted_status_id
        data["was_retweet_of_id"] = quoted_message_id

        target_tweet = api.get_status(quoted_message_id)
        data["was_retweet_of_text"] = target_tweet.text

    return data
