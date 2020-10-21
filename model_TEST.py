from helperMethods import parse_tweet_data
import random
from string import ascii_lowercase
import unittest
import json

from model import authenticate
from helperMethods import parse_tweet_data

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

        self.assertEqual(filtered_data["full_text"], msg)
        self.assertEqual(filtered_data["id"], tweet.id)

if __name__ == '__main__':
    unittest.main()
