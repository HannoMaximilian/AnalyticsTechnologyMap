import sqlite3
import pdb
import multiprocessing
import json


# Create a view, in which we just put the content of posts
# and contents on top of each other. I will use this view if 
# I just want to get the content (with a minimal length of 15 characters)

conn = sqlite3.connect('C:\\MeinCode\\reddit_scraper\\reddit.db')
curs = conn.cursor()
curs.execute("""
        CREATE  VIEW IF NOT EXISTS all_content AS 
                SELECT post_id AS id, content FROM posts
                    WHERE LENGTH(content) > 15
                UNION
                SELECT comment_id, content FROM comments
                    WHERE LENGTH(content) > 15;
            """)
conn.commit()




# Create View for the comments, in which all comments of the same
# post are grouped together. The different comments are split by
# ';-;', which is just something that I thought nobody would
# include in his/her comment

curs.execute("""
        CREATE  VIEW IF NOT EXISTS comments_by_post AS 
            SELECT c.score as comment_score,
                c.id_of_post,
                COUNT(c.id_of_post) AS number_of_comments,
                GROUP_CONCAT(c.content, ';-;') AS list_of_comments
            FROM comments c
            GROUP BY c.id_of_post;

            """)
conn.commit()


###########################################################
### Create View which conatains both the original post as well
### as all the comments under the post (which have a score>1)

curs.execute("""
        CREATE  VIEW IF NOT EXISTS post_with_comments AS 
            SELECT c.*, p.*
            FROM comments_by_post c
            INNER JOIN posts p ON c.id_of_post = p.post_id
            ORDER BY year, month

            """)

conn.commit()
conn.close()