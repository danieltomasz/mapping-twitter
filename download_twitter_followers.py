#adapted from https://stackoverflow.com/a/42390494
import tweepy
import numpy as np

def download_followers(user, api):
    all_followers = []
    try:
        for page in tweepy.Cursor(api.followers_ids, screen_name=user).pages():
            all_followers.extend(map(str, page))
        return all_followers
    except tweepy.TweepError:
        print('Could not access user {}. Skipping...'.format(user))

# Include your keys below:
consumer_key = ''
consumer_secret = ''
access_token = ''
access_token_secret = ''

# Set up tweepy API, with handling of rate limits
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
main_api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

# this should be a list of twitter handles
brainhack_twitter_users = ['mjoboos']
user_followers = {}
for username in brainhack_twitter_users:
    user_followers[username] = [main_api.get_user(int(user_id)).screen_name for user_id in download_followers(username, main_api)]
