from typing import Dict, Any
import json

TWEET_FIELDS = ["id", "created_at", "full_text", "lang", "retweet_count", "favorite_count", "geo", "place", ("entities", "hashtags")]

def parse_tweet_data(json_string: str, fields=TWEET_FIELDS) -> Dict[str, Any]:
    """
    Takes a json string and extracts the fields we care about.
    """

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