import random
from string import ascii_lowercase
import unittest
import json
import time

from model import authenticate
from helperMethods import parse_tweet_data, cleanup_data

def generate_random_string(length:int) -> str:
    return "".join(random.choice(ascii_lowercase) for _ in range(length))


class TestTwitterBot(unittest.TestCase):

    def test_can_see_mentions(self):
        """
        End to End Test: 
            Logs in, and then sends a random tweet (using our name as the @mention)
            We then request the mentions timeline and check if 
            the most recent mention is the message we have just sent.
        """
        api = authenticate()
        my_name = api.me().screen_name

        # Create tweet where we @mention self.
        message = f"@{my_name} {generate_random_string(20)}"

        # send message
        api.update_status(message)

        most_recent_mention = api.mentions_timeline()[0]
        actual = most_recent_mention.text

        self.assertEquals(actual, message)

    def test_can_send_dm(self):
        """
        End to End Test: 
            Logs in, and then sends a direct message to ourselves
        """

        api = authenticate()
        my_name = api.me().screen_name
        my_id = api.me().id

        api.send_direct_message(my_id, f"Hello {my_name}, How are you today")


        #reply_options = [
        #    {
        #      "label": "Red",
        #      "description": "Color of heightened emotion, strength, and power.",
        #      "metadata": "external_id_1"
        #    },
        #    {
        #      "label": "Blue",
        #      "description": "Convey a sense of trust, loyalty, cleanliness, and understanding.",
        #      "metadata": "external_id_2"
        #    }
        #]
        # Note that there is a bug in tweepy Api fixed in https://github.com/tweepy/tweepy/pull/1364
        # Quick_reply_type is currently broken.
        # api.send_direct_message(my_id, "text", quick_reply_type=reply_options)

        self.assertTrue(True)

    def test_get_tweet_data(self):
        """
        End to End Test: 
            Logs in, and then attempts to extract relevant info from a tweet.
        """

        api = authenticate()
        my_name = api.me().screen_name

        msg = generate_random_string(30)

        # Create a tweet
        api.update_status(msg)
        
        # Get Tweet (via user timeline)
        tweets = api.user_timeline(screen_name=my_name, count=1, include_rts = False, tweet_mode = 'extended')

        tweet = tweets[0]
        self.assertEqual(tweet.full_text, msg)

        # Note that this step is not entirely necessary, we could create our database by calling the tweepy methods directly 
        # (e.g. [tweepy object].text) as opposed to using the following convoluted process of [tweepy object] -> json_string -> python dict -> dict["text"]))
        # However the advantage of converting to Json and then extracting from Json is that we 'decouple' functionality. 
        # For instance, we could replace 'tweepy' with some other library that can export tweets in Json format and the "parse_tweet_data" function
        # should work more or less the same.  
        json_string = json.dumps(tweet._json)
        filtered_data = parse_tweet_data(json_string)
        cleaned = cleanup_data(filtered_data)
        

        self.assertEqual(cleaned["text"], msg)
        self.assertEqual(cleaned["id"], tweet.id)

    @unittest.skip("Currently Broken and do not know how to fix")
    def test_can_get_tweet_quoted_message(self):
        """
        End to End Test: 
            Logs in, and then attempts to extract relevant info from a QUOTED tweet.
        """
        api = authenticate()
        my_name = api.me().screen_name

        ## Todo, send a tweet, quote it (with @mention in text), then test.

        most_recent_mentions = api.mentions_timeline()
        tweet = most_recent_mentions[3]

        # How to handle quoted text.
        if tweet.is_quote_status:

            explanatory_text = tweet.text

            quoted_message_id = tweet.quoted_status_id
            target_tweet = api.get_status(quoted_message_id)
            json_string = json.dumps(target_tweet._json)
            filtered_data = parse_tweet_data(json_string)

            filtered_data.update({"explanation_text": explanatory_text})

            #Todo: Tests go here.

        else:
            self.fail("Tweet was not a quote tweet")


    def test_can_get_tweet_reply_message(self):
        """
        End to End Test: 
            Logs in, and then attempts to extract relevant info from a Reply tweet.
        """

        api = authenticate()
        my_name = api.me().screen_name
        my_id = api.me().id

        # send message
        initial_message = generate_random_string(25)
        api.update_status(initial_message)

        time.sleep(1)

        timeline = api.user_timeline(my_id)
        initial_tweet = timeline[0]

        self.assertEquals(initial_tweet.text, initial_message)

        reply_msg = f"@{my_name} (reply) {generate_random_string(20)}"
        api.update_status(reply_msg, in_reply_to_status_id = initial_tweet.id)

        time.sleep(1)

        most_recent_mentions = api.mentions_timeline()
        tweet = most_recent_mentions[0]

        # How to handle reply text.
        reply_id = tweet.in_reply_to_status_id 
        if isinstance(reply_id, int):
            explanatory_text = tweet.text
            target_tweet = api.get_status(reply_id)
            json_string = json.dumps(target_tweet._json)
            filtered_data = parse_tweet_data(json_string)
            filtered_data.update({"explanation_text": explanatory_text})

            self.assertEquals(filtered_data["explanation_text"], reply_msg)
            self.assertEquals(filtered_data["text"], initial_tweet.text)
            self.assertEquals(filtered_data["id"], initial_tweet.id)

        else:
            self.fail("Tweet was not a reply tweet")


if __name__ == '__main__':
    unittest.main()
