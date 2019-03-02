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

<<<<<<< HEAD
# this should be a list of twitter handles
brainhack_twitter_users = ['danieltomasz']
user_followers = {}
for username in brainhack_twitter_users:
    user_followers[username] = download_followers(username, main_api)
=======
if __name__=='__main__':
    twitter = Twython(app_key=APP_KEY, app_secret=APP_SECRET, oauth_version=2)
    access_token = twitter.obtain_access_token()
    twitter = Twython(app_key=APP_KEY, access_token=access_token)
    followers = concatenate_ids([followers for followers in generate_followers('neuroconscience', APP_KEY, access_token)])


# %%
>>>>>>> 92f91bc6192be70030db05d169458411f77f96f6
