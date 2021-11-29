#Extra Credit 7

'''

Have your bot upvote any comment or submission that mentions your favorite candidate (or downvote submission mentioning a candidate you do not like). I recommend creating a separate python file for performing the upvotes, and you must be able to upvote comments contained within any submission in the class subreddit.

You may earn an additional two points if you use the TextBlob sentiment analysis library to determine the sentiment of all the posts that mention your favorite candidate. If the comment/submission has positive sentiment, then upvote it; if the comment/submission has a negative sentiment, then downvote it.

This extra credit is "grayhat" since it may violate reddit's TOS if not done correctly.

You must up/downvote at least 100 submissions and 500 comments for the full extra credit.
'''


import praw
import random
import datetime
import time
import nltk
from textblob import TextBlob

reddit = praw.Reddit('bot1', user_agent='cs40')

submission_url = 'https://www.reddit.com/r/BotTown2/comments/r0yi9l/main_discussion_thread/'
submission = reddit.submission(url='https://www.reddit.com/r/BotTown2/comments/r0yi9l/main_discussion_thread/')
 

while True:
    submission_text = TextBlob(submission.title)
    if ("Obama" in submission_text.lower() and submission_text.sentiment.polarity>0.5):
        submission.upvote()
