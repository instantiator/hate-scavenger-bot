from typing import Dict, Any
import json
import dateutil.parser as parser

TWEET_FIELDS = ['id', 'created_at', 'full_text', 'text', ('user', 'screen_name'), 'lang', 'retweet_count', 'favorite_count', 'geo',
                "was_reply_to_id", "was_reply_to_text", "was_retweet_of_id", "was_retweet_of_text",
                'notify_text', 'notify_tweet_id', 'notify_is_reply', 'notify_is_retweet', 'notify_screen_name'] 
                
# Other fields in DB:  'entry_added_by', "uid"

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
    
    data["created_at"] = parse_date(data["created_at"])
    
    return data
    
    
def parse_date(date:str) -> str:
    """
    Takes a string of the form:
        Mon Oct 19 23:11:47 +0000 2020
    And returns:
        2020-10-19T23:11:47+00:00
    
    Which is a datestring in ISO 8601 format (a format which is supported by dynamoDB)
    """
    #https://stackoverflow.com/questions/4460698/python-convert-string-representation-of-date-to-iso-8601    
    return parser.parse(date).isoformat()