import unittest

from helperMethods import parse_tweet_data, remove_user_info_from_tweet

class TestFilterData(unittest.TestCase):

    def test_can_extract_data_from_json_string(self):
        example_json_string = """{"created_at":"Wed Oct 21 12:55:06 +0000 2020","id":1318898605122617345,"id_str":"1318898605122617345","full_text":"bujdqcdkwaimymtffiozftobxtwdxr","truncated":false,"display_text_range":[0,30],"entities":{"hashtags":[],"symbols":[],"user_mentions":[],"urls":[]},"source":"","in_reply_to_status_id":null,"in_reply_to_status_id_str":null,"in_reply_to_user_id":null,"in_reply_to_user_id_str":null,"in_reply_to_screen_name":null,"user":{"id":1318099807228076032,"id_str":"1318099807228076032","name":"chris","screen_name":"chris48947141","location":"","description":"","url":null,"entities":{"description":{"urls":[]}},"protected":false,"followers_count":0,"friends_count":0,"listed_count":0,"created_at":"Mon Oct 19 08:01:07 +0000 2020","favourites_count":0,"utc_offset":null,"time_zone":null,"geo_enabled":false,"verified":false,"statuses_count":16,"lang":null,"contributors_enabled":false,"is_translator":false,"is_translation_enabled":false,"profile_background_color":"F5F8FA","profile_background_image_url":null,"profile_background_image_url_https":null,"profile_background_tile":false,"profile_image_url":"http://abs.twimg.com/sticky/default_profile_images/default_profile_normal.png","profile_image_url_https":"https://abs.twimg.com/sticky/default_profile_images/default_profile_normal.png","profile_link_color":"1DA1F2","profile_sidebar_border_color":"C0DEED","profile_sidebar_fill_color":"DDEEF6","profile_text_color":"333333","profile_use_background_image":true,"has_extended_profile":true,"default_profile":true,"default_profile_image":true,"following":false,"follow_request_sent":false,"notifications":false,"translator_type":"none"},"geo":null,"coordinates":null,"place":null,"contributors":null,"is_quote_status":false,"retweet_count":0,"favorite_count":0,"favorited":false,"retweeted":false,"lang":"et"}"""

        expected = {'id': 1318898605122617345,
                    'created_at': 'Wed Oct 21 12:55:06 +0000 2020',
                    'text': 'bujdqcdkwaimymtffiozftobxtwdxr',
                    'lang': 'et',
                    'retweet_count': 0,
                    'favorite_count': 0,
                    'geo': None,
                    'place': None,
                    'hashtags': []}

        keys =  ["id", "created_at", "text", "full_text", "lang", "retweet_count", "favorite_count", "geo", "place", ("entities", "hashtags")]
        actual = parse_tweet_data(example_json_string, fields=keys)

        self.assertEqual(actual, expected)

class Regex(unittest.TestCase):

    def test_remove_user_info_with_one_user(self):
        tweet = "@Bot Hello World!"
        expected = "@_ Hello World!"

        actual = remove_user_info_from_tweet(tweet)
        self.assertEquals(actual, expected)

    def test_remove_user_info_with_two_users(self):
        tweet =  "@Bot I don't like @Bot2, he is mean"
        expected =  "@_ I don't like @_, he is mean"

        actual = remove_user_info_from_tweet(tweet)
        self.assertEquals(actual, expected)

    def test_remove_user_info_returns_original_when_no_users(self):
        tweet =  "Ham and pineapple make for a great pizza"
        expected =  "Ham and pineapple make for a great pizza"

        actual = remove_user_info_from_tweet(tweet)
        self.assertEquals(actual, expected)


if __name__ == '__main__':
    unittest.main()
