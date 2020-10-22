from typing import Dict, Any, Optional
import json
import re

TWEET_FIELDS = ['id', 'created_at', 'full_text', 'text', ('user', 'screen_name'), 'lang', 'retweet_count', 'favorite_count', 'geo', ('entities', 'hashtags'),
                'notify_text', 'notify_tweet_id', 'notify_is_reply', 'notify_is_retweet', 'notify_screen_name']

def parse_tweet_data(json_string: str, fields=TWEET_FIELDS) -> Dict[str, Any]:
    '''
    Takes a json string and extracts the fields we care about.
    '''

    raw_data = json.loads(json_string)

    filtered_data = dict()
    for f in fields:
        if isinstance(f, str):
            value = raw_data.get(f)
            filtered_data[f] = value

        elif isinstance(f, tuple):
            # If field is tuple, then data is nested.
            # for instance (x, y, z) => dict[x][y][z]
            # They maybe a more elegant way todo this. :)
            tmp = raw_data
            for sub_field in f:
                if isinstance(tmp, dict):
                    tmp = tmp.get(sub_field)

            key = f[-1]
            filtered_data[key] = tmp

    return filtered_data


def cleanup_data(data:Dict[str, Any]) -> Dict[str, Any]:
    # Remove 'full_text' key, add content to 'text' key
    if data['full_text'] is not None:
        data['text'] = data['full_text']
    data.pop('full_text')

    # Convert hashtag list to 'csv' style string
    data['hashtags'] = ','.join(data['hashtags'])

    return data


def remove_user_info_from_tweet(tweet:Optional[str]) -> str:
    '''
        '@Bot Hello World!'  => '@_ Hello World!'
        '@Bot I don't like @Bot2, he is mean' => '@_ I don't like @_, he is mean'
    '''
    if tweet is None: 
        return ''

    return re.sub(r'@[\w_]+', '@_', tweet)

def remove_url_from_tweet(tweet: Optional[str]) -> str:
    '''
        'here is a url https://t.co/MTKGymzfmf' => 'here is a url <url>'
    '''

    ## https://stackoverflow.com/questions/6038061/regular-expression-to-find-urls-within-a-string
    pattern = r'(http|ftp|https)://([\w_-]+(?:(?:\.[\w_-]+)+))([\w.,@?^=%&:/~+#-]*[\w@?^=%&/~+#-])?'

    if tweet is None:
        return ''

    return re.sub(pattern, '<url>', tweet)
