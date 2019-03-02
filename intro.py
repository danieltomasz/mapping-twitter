#!/usr/bin/env python
import twitterconfig as cfg
connect(cfg.mysql['host'], cfg.mysql['user'], cfg.mysql['password'])

# %%
import json
from flask import Flask, request
from threading import Timer
from IPython.display import IFrame
from IPython.display import display
from IPython.display import Javascript as JS

import twitter
from twitter.oauth_dance import parse_oauth_tokens
from twitter.oauth import read_token_file, write_token_file

OAUTH_FILE = "/tmp/twitter_oauth"

# XXX: Go to http://twitter.com/apps/new to create an app and get values
# for these credentials that you'll need to provide in place of these
# empty string values that are defined as placeholders.
# See https://dev.twitter.com/docs/auth/oauth for more information 
# on Twitter's OAuth implementation and ensure that *oauth_callback*
# is defined in your application settings as shown below if you are 
# using Flask in this IPython Notebook

# Define a few variables that will bleed into the lexical scope of a couple of 
# functions below
CONSUMER_KEY = ''
CONSUMER_SECRET = ''
oauth_callback = 'http://127.0.0.1:5000/oauth_helper'
    
# Setup a callback handler for when Twitter redirects back to us after the user authorizes the app

webserver = Flask("TwitterOAuth")
@webserver.route("/oauth_helper")
def oauth_helper():
    
    oauth_verifier = request.args.get('oauth_verifier')

    # Pick back up credentials from ipynb_oauth_dance
    oauth_token, oauth_token_secret = read_token_file(OAUTH_FILE)
    
    _twitter = twitter.Twitter(
        auth=twitter.OAuth(
            oauth_token, oauth_token_secret, CONSUMER_KEY, CONSUMER_SECRET),
        format='', api_version=None)

    oauth_token, oauth_token_secret = parse_oauth_tokens(
        _twitter.oauth.access_token(oauth_verifier=oauth_verifier))

    # This web server only needs to service one request, so shut it down
    shutdown_after_request = request.environ.get('werkzeug.server.shutdown')
    shutdown_after_request()

    # Write out the final credentials that can be picked up after the blocking
    # call to webserver.run() below.
    write_token_file(OAUTH_FILE, oauth_token, oauth_token_secret)
    return "%s %s written to %s" % (oauth_token, oauth_token_secret, OAUTH_FILE)


# To handle Twitter's OAuth 1.0a implementation, we'll just need to implement a custom
# "oauth dance" and will closely follower the pattern defined in twitter.oauth_dance.

def ipynb_oauth_dance():
    
    _twitter = twitter.Twitter(
        auth=twitter.OAuth('', '', CONSUMER_KEY, CONSUMER_SECRET),
        format='', api_version=None)

    oauth_token, oauth_token_secret = parse_oauth_tokens(
            _twitter.oauth.request_token(oauth_callback=oauth_callback))

    # Need to write these interim values out to a file to pick up on the callback from Twitter
    # that is handled by the web server in /oauth_helper
    write_token_file(OAUTH_FILE, oauth_token, oauth_token_secret)
    
    oauth_url = ('http://api.twitter.com/oauth/authorize?oauth_token=' + oauth_token)
    
    # Tap the browser's native capabilities to access the web server through a new window to get
    # user authorization
    display(JS("window.open('%s')" % oauth_url))


# After the webserver.run() blocking call, start the oauth dance that will ultimately
# cause Twitter to redirect a request back to it. Once that request is serviced, the web
# server will shutdown, and program flow will resume with the OAUTH_FILE containing the
# necessary credentials
Timer(1, lambda: ipynb_oauth_dance()).start()

webserver.run(host='0.0.0.0')

# The values that are read from this file are written out at
# the end of /oauth_helper
oauth_token, oauth_token_secret = read_token_file(OAUTH_FILE)

# These 4 credentials are what is needed to authorize the application
auth = twitter.oauth.OAuth(oauth_token, oauth_token_secret,
                               CONSUMER_KEY, CONSUMER_SECRET)
    
twitter_api = twitter.Twitter(auth=auth)

print(twitter_api)
