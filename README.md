# hate-scavenger-bot

## Database

### Database Columns

- **uid**: String - *Primary Key, a unique Identifier for each entry in the database.*
- **created_at**: String - *a datetime string in ISO 8601 format. The time the 'offensive tweet' was posted on Twitter.*
- **entry_added_by**: String - *Name of the bot/user that added this entry to the database.*
- **favorite_count**: Integer - *Number of times the 'offensive tweet' has been favorited.*
- **retweet_count**: Integer - *Number of times the 'offensive tweet' has been retweeted.*
- **geo**: null *???*
- **id**: Integer - *Tweet id of the 'offensive tweet'.*
- **lang**: String - *Two-Character codes (ISO 639) denoting the Language the 'offensive tweet' was written in.*
- **screen_name**: String - *Twitter username, author of the 'offensive tweet'.*
- **text**: String - *The 'offensive tweet' itself.*
- **was_reply_to_id**: Integer/null - *Tweet Id of the tweet the 'offensive tweet' was replying to.*
- **was_reply_to_text**: String/null - *If the 'offensive tweet' was a reply to another tweet, this is the text of tweet that was replied to.*
- **was_retweet_of_id**: Integer/null - *Twitter Id of the tweet the 'offensive tweet' was quoting.*
- **was_retweet_of_text**: String/null - *If the 'offensive tweet' quoted a tweet, this is the text of that quoted tweet.*
- **notify_is_reply**: Bool - *Has the notifier replied to the 'offensive tweet'.*
- **notify_is_retweet**: Bool - *Has the notifier 'quoted' the 'offensive tweet'.*
- **notify_screen_name**: String - *Twitter username, the person notifying us about the 'offensive tweet'.*
- **notify_text**: String - *The 'notifying tweet'. This may contain additional information/context about the 'offensive tweet'.*
- **notify_tweet_id**: Integer - *Tweet id of the 'notifying tweet'.*
