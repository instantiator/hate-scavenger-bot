import tweepy

from auth import API_KEY, API_SECRET_KEY, ACCESS_TOKEN, ACCESS_TOKEN_SECRET, BEARER_TOKEN


def authenticate():
    """
    Sign in and return Api
    """

    auth = tweepy.OAuthHandler(API_KEY, API_SECRET_KEY)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

    api = tweepy.API(auth)
    return api


if __name__ == '__main__':

    api = authenticate()
    
    # Create a tweet
    api.update_status("Hello World!")

    print("done")
