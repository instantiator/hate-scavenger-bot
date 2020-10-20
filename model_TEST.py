import random
from string import ascii_lowercase
import unittest


from model import authenticate


def generate_random_string(length:int) -> str:
    return "".join(random.choice(ascii_lowercase) for _ in range(length))

class TestMentions(unittest.TestCase):

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


if __name__ == '__main__':
    unittest.main()
