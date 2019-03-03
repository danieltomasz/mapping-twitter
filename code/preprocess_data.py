import json

fields_to_keep = ['text', 'user', 'timestamp']

def get_interesting_parts(tweet):
    return {field: cont for field, cont in tweet.items() if field in fields_to_keep}

def format_tweets(json_file):
    '''Formats tweets from json_file into list that can be further used'''
    with open(json_file, 'r') as fl:
        content = json.load(fl)
    filtered_content = [get_interesting_parts(tweet) for tweet in content]
    return filtered_content

def parse_mentions(text):
    '''Returns all matched mentions in text
    a mention starts with @ then a username follows
    Returns only username'''
    import re
    username_regex = r"(?<=^|(?<=[^a-zA-Z0-9-_\.]))@([A-Za-z]+[A-Za-z0-9-_]+)"
    matches = re.findall(username_regex, text)
    return [m.strip('@') for m in matches if m is not None]

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


def load_brainhack_warsaw_data(filename='saved_followers.json'):
    '''Loads the content of filename (if you ran everything as in the script that's the followers of followers of the brainhack warsaw account)'''
    with open(filename, 'r') as fl:
        warsaw_dict = json.load(fl)
    return warsaw_dict


def get_follower_name_from_number(number, vocabulary):
    '''Helper function to get the name of a follower from the number of its column in the sparse matrix'''
    return list(vocabulary.keys())[list(vocabulary.values()).index(number)]
