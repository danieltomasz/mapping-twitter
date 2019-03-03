# Twitter Ego-Network

* Setup  of Twitter credentials (developer acount): login to your twitter account and  to http://apps.twitter.com/
* more about limitations https://dev.twitter.com/rest/public/rate-limiting
* We will put scripts and notebooks to make this analysis reproducible
* We are using Pytjon and Tweepy to run analysis
## What actually makes a tweet?
* text content
* entites (user mentions, hashtags, URLs, and media) and places

## Getting started

Create config.py file where you will store your App keys
Create .gitignore file and include config.py file there

## Simple Visualization of the data

Visualization.ipynb in code/ invokes a simple scatter plot based on the number of shared followers.
It uses [Uniform Manifold Approximation and Projection](https://github.com/lmcinnes/umap) for dimensionality reduction.
You can play with the parameters and see what they do.

## Example jupyter notebook

* https://github.com/mikhailklassen/Mining-the-Social-Web-3rd-Edition
* https://github.com/bonzanini/Book-SocialMediaMiningPython

## Datasets
* NIPS circles http://snap.stanford.edu/data/egonets-Twitter.html
* HIGGS discovery http://snap.stanford.edu/data/higgs/web/twitter-higgs.html


## Example apps
https://www.proporti.onl/

# Example analysis
* https://perrystephenson.me/2018/09/29/the-r-twitter-network/
* https://towardsdatascience.com/@shahamfarooq
* https://towardsdatascience.com/information-flow-within-twitter-community-def9e939bb99
* https://towardsdatascience.com/information-flow-within-twitter-community-def9e939bb99


## Task for tomorrow:
*  Daniel: prepare data from json to  gephi matrix
