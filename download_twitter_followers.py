import tweepy
import numpy as np
import json

#adapted from https://stackoverflow.com/a/42390494

def download_followers(user, api):
    all_followers = []
    try:
        for page in tweepy.Cursor(api.followers_ids, screen_name=user).pages():
            all_followers.extend(map(str, page))
        return all_followers
    except tweepy.TweepError:
        print('Could not access user {}. Skipping...'.format(user))


def get_screen_names_of_followers(user, api):
    '''Returns a list of screen names for user given tweepy api'''
    return [api.get_user(int(user_id)).screen_name for user_id in download_followers(user, api)]


def get_followers_of_followers(user, api):
    '''Returns a dictionary with every follower of user as a key and the followers of this follower as values'''
    followers_of_user = get_screen_names_of_followers(user, api)
    followers_of_followers = {follower: get_screen_names_of_followers(follower, api)
                              for follower in followers_of_user}
    return followers_of_followers


def compute_sparse_matrix_of_followers(follower_dict):
    '''Computes a scipy sparse matrix for follower dict with as many rows as there are keys in follower_dict (indicating the number of users)
       and as many columns as there are unique followers in the values of follower_dict.
       This matrix indicates if a user has this screen_name as a follower.
       OUT:
            sparse_matrix   --      the matrix described above
            vocabulary      --      vocabulary mapping follower name to column number'''
    from sklearn.feature_extraction.text import CountVectorizer
    cvectorizer = CountVectorizer()
    fake_documents = [' '.join(follower_dict[username]) for username in sorted(follower_dict)]
    sparse_matrix = cvectorizer.fit_transform(fake_documents)
    return sparse_matrix, cvectorizer.vocabulary_


# Include your keys below:
consumer_key = ''
consumer_secret = ''
access_token = ''
access_token_secret = ''

# Set up tweepy API, with handling of rate limits
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
main_api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

if __name__ == '__main__':
    # this should be a list of twitter handles
    # IF YOU WANT TO DOWNLOAD ALL FOLLOWERS OF THE FOLLOWERS OF THE BRAINHACK WARSAW ACCOUNT UNCOMMENT AND RUN
    # this takes some _time_
#    which_to_scrape = ['BrainhackW']
#    user_followers = {}
#    for username in which_to_scrape:
#        user_followers[username] = get_followers_of_followers(username, main_api)
#    with open('saved_followers.json', 'w+') as fl:
#        json.dump(user_followers, fl)
    which_to_scrape = ['danieltomasz']
    user_followers = {}
    for user in which_to_scrape:
        user_followers[user] = get_screen_names_of_followers(user, main_api)
