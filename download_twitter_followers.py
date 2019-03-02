from twython import Twython
import numpy as np
import time

def generate_followers(screen_name, app_key, access_token):
    '''Given the screen name of the user generates (i.e. you can iterate over it) a list of all twitter API chunks'''
    twitter = Twython(app_key=app_key, access_token=access_token)
    next_cursor = 1
    while next_cursor > 0:
        try:
            followers = twitter.get_followers_ids(screen_name=screen_name)
            next_cursor = followers['next_cursor']
        # this should be changed to the right exception
        except Exception:
            remainder = float(twitter.get_lastfunction_header(header='x-rate-limit-reset')) - time.time()
            del twitter
            print('Sleeping for {}'.format(remainder))
            time.sleep(remainder)
            twitter = Twython(app_key=app_key, access_token=access_token)
            continue
        yield followers

def concatenate_ids(list_of_id_dicts):
    return np.concatenate([followers['ids'] for followers in list_of_id_dicts])

APP_KEY = 'YOUR APP KEY'
APP_SECRET = 'YOUR APP SECRET'

if __name__=='__main__':
    twitter = Twython(app_key=APP_KEY, app_secret=APP_SECRET, oauth_version=2)
    access_token = twitter.obtain_access_token()
    twitter = Twython(app_key=APP_KEY, access_token=access_token)
    followers = concatenate_ids([followers for followers in generate_followers('neuroconscience', APP_KEY, access_token)])
