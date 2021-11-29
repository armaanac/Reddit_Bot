
#Extra Credit 4

'''
Make your bot create new submission posts instead of just new comments. You can easily automate this process by scanning the top posts in your favorite sub (e.g. /r/liberal or /r/conservative) and posting them to the class sub. I recommend creating a separate python file for creating submissions and creating comments.

For full credit, you must have at least 200 submissions, some of which should be self posts and some link posts. Duplicate submissions (i.e. submissions with the same title/selftext/url) do not count.

'''

import praw
import time
import prawcore

reddit = praw.Reddit('bot1', user_agent='cs40')

count=0
for submission in reddit.subreddit("conservative").hot(limit=None):
    a=submission.title
    b=submission.url
    try:
       reddit.subreddit('BotTown2').submit(a,url=b)
    except (praw.exceptions.RedditAPIException, prawcore.exceptions.NotFound) as e :
        pass
    count+=1
    print('reposted comments=',count)
    time.sleep(20)