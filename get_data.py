import datetime
import sqlite3
import pdb
import time
import requests



###########################################################
################# SETTINGS
beginning_timestamp = int(datetime.datetime(year=2018, month=1, day=1).timestamp())
end_timestamp = int(datetime.datetime(year=2020, month=5, day=1).timestamp())
# subreddits = ['MaschineLearning', 'webdev', 'bigdata', 'datascience', 'analytics', 'ArtificialInteligence']
subreddit = 'ArtificialInteligence'
path_to_db = 'C:\\MeinCode\\reddit_scraper\\reddit.db'

###########################################################
################# Connect to or create database
conn = sqlite3.connect(path_to_db)
#conn = sqlite3.connect(':memory:')
curs = conn.cursor()

###########################################################
################# GET POSTS

with conn:
    curs.execute("""CREATE TABLE IF NOT EXISTS posts (
    post_id TEXT PRIMARY KEY,
    title TEXT,
    score INTEGER,
    author TEXT,
    author_fullname TEXT,
    content TEXT,
    num_comments INTEGER,
    subreddit TEXT,
    subreddit_id TEXT,
    url TEXT,
    created_utc TEXT,
    eu_time TEXT,
    year INTEGER,
    month INTEGER,
    week INTEGER
    )""")


def get_post_batch(subreddit, beginning_timestamp, end_timestamp):
    """
    Gets posts from the given subreddit for the given time period
    :param subreddit: the subreddit to retrieve posts from
    :param beginning_timestamp: The unix timestamp of when the posts should begin
    :param end_timestamp: The unix timestamp of when the posts should end (defaults to right now)
    :return:
    """
    print("New pushshift API call")
    url = "https://api.pushshift.io/reddit/search/submission/" \
            "?subreddit={0}" \
            "&limit=500" \
            "&after={1}" \
            "&before={2}" \
            "&score=%3E0".format(subreddit, beginning_timestamp, end_timestamp)

    response = requests.get(url)
    if response.status_code != 200:
        print("""A request did not get any data returned. This can happen if we had exactly 500 posts left to query with our last request
                or more likely because you made some mistake""")
        return []
        
    resp_json = response.json()
    return resp_json['data']

def add_posts(posts):
    """Takes a batch of posts and adds them to our SQL database
    args:
    posts: A list of posts. Each item is a dictionary containing all information
            given by pushlift
    """
    with conn:
        for post in posts:
            #Everything related to time
            raw_time = datetime.datetime.fromtimestamp(post.get('created_utc'))
            year = raw_time.strftime("%Y")
            month = raw_time.strftime("%m")
            week = raw_time.strftime("%W")
            # eu_time is the time in european standard (day before month)
            eu_time = raw_time.strftime("%d.%m.%Y %H:%M:%S")

            curs.execute("""INSERT OR IGNORE INTO posts VALUES (:post_id, :title, :score, :author, :author_fullname,
            :content, :num_comments, :subreddit, :subreddit_id, :url, :created_utc, :eu_time, :year, :month, :week)""",
            {'post_id': post.get('id'), 
            'title': post.get('title'), 
            'score': post.get('score'), 
            'author': post.get('author'),
            'author_fullname': post.get('author_fullname'),
            'content': post.get('selftext'),
            'num_comments': post.get('num_comments'),
            'subreddit': post.get('subreddit'),
            'subreddit_id': post.get('subreddit_id'),
            'url': post.get('url'),
            'created_utc': post.get('created_utc'),
            'eu_time': eu_time,
            'year': year,
            'month': month,
            'week': week}  
            )

def get_posts(subreddit, beginning_timestamp, end_timestamp):
    """Responsible for requesting all posts from given subreddit in given time window

    Will call function get_post_batch several times, because the pushlift API restricts
    the number of posts returned for every call to 500

    args:
    beginning_timestamp: Beginning of time window
    end_timestamp: End of time window
    subreddit: Subreddit we are requesting posts from

    """
    data = get_post_batch(subreddit, beginning_timestamp, end_timestamp)
    add_posts(data)
    post_count = len(data)
    while len(data) >= 500:
        # go back for more data
        last_one = data[499]
        beginning_timestamp = last_one['created_utc'] + 1
        data = get_post_batch(subreddit, beginning_timestamp, end_timestamp)
        print('{0} items fetched'.format(len(data)))
        post_count = post_count + len(data)
        add_posts(data)

    return post_count

post_count = get_posts(subreddit, beginning_timestamp, end_timestamp)
print("We got {0} posts from pushlift".format(post_count))


###########################################################
################# GET COMMENTS

with conn:
    curs.execute("""CREATE TABLE IF NOT EXISTS comments (
    comment_id TEXT PRIMARY KEY,
    score INTEGER,
    author TEXT,
    author_fullname TEXT,
    content TEXT,
    subreddit TEXT,
    subreddit_id TEXT,
    link TEXT,
    id_of_post TEXT,
    parent_id TEXT,
    created_utc TEXT,
    eu_time TEXT,
    year INTEGER,
    month INTEGER,
    week INTEGER
    )""")


def get_comment_batch(subreddit, beginning_timestamp, end_timestamp):
    """
    Gets comments from the given subreddit for the given time period
    :param sub: the subreddit to retrieve posts from
    :param beginning: The unix timestamp of when the posts should begin
    :param end: The unix timestamp of when the posts should end (defaults to right now)
    :return:
    """
    print("Querying pushshift")
    url = "https://api.pushshift.io/reddit/comment/search/" \
            "?subreddit={0}" \
            "&limit=500" \
            "&after={1}" \
            "&before={2}" \
            "&score=%3E0".format(subreddit, beginning_timestamp, end_timestamp)
        
    response = requests.get(url)
    if response.status_code != 200:
        print("""A request did not get any data returned. This can happen if we had exactly 500 posts left to query with our last request
                or more likely because you made some mistake""")
        return []
    resp_json = response.json()
    return resp_json['data']

def add_comments(comments):
    with conn:
        for comment in comments:
            #The ID of the original post, under which the comment is written, is only accessible through the url
            id_of_post = comment['permalink'].split("/")[4]

            #Everything related to time
            raw_time = datetime.datetime.fromtimestamp(comment.get('created_utc'))
            year = raw_time.strftime("%Y")
            month = raw_time.strftime("%m")
            week = raw_time.strftime("%W")
            # eu_time is the time in european standard (day before month)
            eu_time = raw_time.strftime("%d.%m.%Y %H:%M:%S")
            curs.execute("""INSERT OR IGNORE INTO comments VALUES (:comment_id, :score, :author, :author_fullname,
            :content, :subreddit, :subreddit_id, :link, :id_of_post, :parent_id, :created_utc, :eu_time, :year, :month, :week)""",
            {'comment_id': comment.get('id'), 
            'score': comment.get('score'), 
            'author': comment.get('author'),
            'author_fullname': comment.get('author_fullname'),
            'content': comment.get('body'),
            'subreddit': comment.get('subreddit'),
            'subreddit_id': comment.get('subreddit_id'),
            'link': comment.get('permalink'),
            'id_of_post': id_of_post,
            'parent_id' : comment.get('parent_id'),
            'created_utc': comment.get('created_utc'),
            'eu_time': eu_time,
            'year': year,
            'month': month,
            'week': week
            }  
            )


def get_comments(subreddit, beginning_timestamp, end_timestamp):
    """Responsible for requesting all comments from given subreddit in given time window

    Will call function get_comment_batch several times, because the pushlift API restricts
    the number of posts returned for every call to 500

    args:
    beginning_timestamp: Beginning of time window
    end_timestamp: End of time window
    subreddit: Subreddit we are requesting posts from

    """
    data = get_comment_batch(subreddit, beginning_timestamp, end_timestamp)
    add_comments(data)
    comment_count = len(data)
    while len(data) >= 500:
        # go back for more data
        last_one = data[499]
        beginning_timestamp = last_one['created_utc'] + 1
        data = get_comment_batch(subreddit, beginning_timestamp, end_timestamp)
        print('{0} items fetched'.format(len(data)))
        comment_count = comment_count + len(data)
        add_comments(data)

    return comment_count

comment_count = get_comments(subreddit, beginning_timestamp, end_timestamp)
print("We got {0} comments from pushlift".format(comment_count))


conn.commit() #Should be obsolete since we are using "with conn" the whole time but let's be safe
conn.close()