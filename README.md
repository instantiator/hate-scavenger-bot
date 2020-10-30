# hate-scavenger-bot

## Database

### Database Columns

- **uid**: String - *Primary Key, a unique Identifier for each entry in the database.*
- **created_at**: String - *a datetime string in ISO 8601 format. The time the 'offensive tweet' was posted on Twitter.*
- **entry_added_by**: String - *Name of the bot/user that added this entry to the database.*
- **favorite_count**: Integer - *Number of times the 'offensive tweet' has been favorited.*
- **retweet_count**: Integer - *Number of times the 'offensive tweet' has been retweeted.*
- **geo**: *???*
- **id**: Integer - *Tweet id (from Twitter) of the 'offensive tweet'.*
- **lang**: String - *Two-Character codes (ISO 639) denoting the Language the 'offensive tweet' was written in.*
- **screen_name**: String - *Twitter username, author of the 'offensive tweet'.*
- **text**: String - *The 'offensive tweet' itself.*
- **notify_is_reply**: *??*
- **notify_is_retweet**: *??*
- **notify_screen_name**: String - *Twitter username, the person notifying us about the the 'offensive tweet'.*
- **notify_text**: String - *The 'notifying tweet'. This may contain additional information/context about the 'offensive tweet'.*
- **notify_tweet_id**: Integer - *Tweet id (from Twitter) of the 'notifying tweet'.*