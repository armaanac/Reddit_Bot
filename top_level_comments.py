'''
Extra Credit 6: Instead of having your bot reply randomly to posts,
make your bot reply to the most highly upvoted comment in a thread
that it hasn't already replied to. Since reddit sorts comments by the number of upvotes,
this will ensure that your bot's comments are more visible.
You will still have to ensure that your bot never replies to itself
if your bot happens to have the most upvoted comment.
Total EC from this file: 2 points!
'''

import praw
import random
import datetime
import time


madlibs = [
    "[UNITED_STATES] is a [DEMOCRACY]. The [CURRENT] [PRESIDENT] is Biden. [MANY_PEOPLE] [SUPPORT] him.",
    "He  was [ELECTED] [THIS_YEAR].  He was [RAISED] in [SCRANTON]. He [STUDIED] at [UNI_OF_DELAWARE]",
    "He [WANTS] to [INVEST] in [RENEWABLE_FUELS].  [BIDEN] is [AMBITIOUS]. [HE] [WANTS] to [TAKE_ACTION] [THE_ISSUE] of [CLIMATE_CHANGE]",
    "He [BELIEVES_IN] Build Back Better. He [WANTS] to [FIGHT] [THE_PANDEMIC]. He [WANTS] to [SAVE] [THE WORLD]",
    "He [WANTS] to [REVERSE] [IMMIGRATION_POLICIES]. [HE] is [ADVOCATING] [FREE_PUBLIC_EDUCATION]. He [SUPPORTS] abortions",
    ]

replacements = {
    'UNITED_STATES' : ['USA', 'America', 'The United States', 'United States'],
    'DEMOCRACY' : ['democracy', 'democratic country', 'government for the people by the people'],
    'CURRENT' : ['current', 'new', '46th', 'newest'],
    'PRESIDENT'  : ['President', 'leader'],
    'MANY_PEOPLE' : ['Many people', 'People', 'Alot of people', 'People of the United States'],
    'SUPPORT' : ['support', 'believe in', 'like', 'value'],
    'ELECTED' : ['elected', 'assumed to office','appointed'],
    'THIS_YEAR' : ['this year', 'in 2021', 'in January'],
    'RAISED' : ['raised', 'born and brought up', 'born', 'brought up'],
    'SCRANTON' : ['Scranton', 'Pennsylvania', 'the East Coast'],
    'STUDIED':['was educated', 'studied', 'did his college', 'did his undergraduation'],
    'UNI_OF_DELAWARE': ['Univeristy of Delaware', 'Delaware', 'Uni of Delaware'],
    'WANTS' : ['wants', 'wishes', 'hopes', 'desires'],
    'INVEST': ['invest', 'spend money', 'put money'],
    'RENEWABLE_FUELS': ['renewable fuels', 'climate change', 'eco-friendly methods'],
    'BIDEN': ['Biden', 'The president', 'Joe Biden'],
    'AMBITIOUS': ['goal oriented', 'ambitious', 'smart'],
    'HE': ['He', 'Biden', 'the President', 'Joe Biden'],
    'TAKE_ACTION': ['take action on', 'work towards', 'help support the world on'],
    'THE_ISSUE': ['The issue', 'the problem'],
    'CLIMATE_CHANGE': ['Climate Change', 'global warming', 'climate crisis'],
    'BELIEVES_IN': ['believes in', 'supports', 'strongly advocates for'],
    'FIGHT': ['fight', 'battle'],
    'THE_PANDEMIC': ['the pandemic', 'covid-19', 'new covid strain', 'covid'],
    'SAVE': ['protect', 'save', 'help', 'rescue'],
    'THE_WORLD': ['USA', 'the world', 'his country', 'his people'],
    'REVERSE': ['reverse', 'remove', 'go against'],
    'IMMIGRATION_POLICIES': ['the previous immigration policies', 'Trumps immigration policies', 'Trumps policies'],
    'ADVOCATING': ['advocating for', 'supporting'],
    'FREE_PUBLIC_EDUCATION': ['free public education ', 'free education for the public', 'public education that is free'],
    'SUPPORTS' : ['supports', 'is not against', 'advocates for'],

    }


def generate_comment():
    '''
    This function generates random comments according to the patterns specified in the `madlibs` variable.
    To implement this function, you should:
    1. Randomly select a string from the madlibs list.
    2. For each word contained in square brackets `[]`:
        Replace that word with a randomly selected word from the corresponding entry in the `replacements` dictionary.
    3. Return the resulting string.
    For example, if we randomly seleected the madlib "I [LOVE] [PYTHON]",
    then the function might return "I like Python" or "I adore Programming".
    Notice that the word "Programming" is incorrectly capitalized in the second sentence.
    You do not have to worry about making the output grammatically correct inside this function.
    '''
    s = random.choice(madlibs)
    for k in replacements.keys():
        s = s.replace('['+k+']', random.choice(replacements[k]))
    return s

# connect to reddit 
reddit = praw.Reddit('bot1', user_agent='cs40bot')

# select a "home" submission in the /r/BotTown subreddit to post to,
# and put the url below
submission_url = 'https://www.reddit.com/r/BotTown2/comments/r0yi9l/main_discussion_thread/'
submission = reddit.submission(url=submission_url)

while True:
    
    # printing the current time will help make the output messages more informative
    # since things on reddit vary with time
    print()
    print('new iteration at:',datetime.datetime.now())
    print('submission.title=',submission.title)
    print('submission.url=',submission.url)

    # FIXME (task 0): get a list of all of the comments in the submission
    # HINT: this requires using the .list() and the .replace_more() functions

    submission.comments.replace_more(limit=None)
    all_comments = []
    not_my_comments = []

    for comment in submission.comments.list():
        if str(comment.author) != 'None':
            all_comments.append(comment)
        if str(comment.author) != 'botbotboot':
            not_my_comments.append(comment)


    print('len(all_comments)=',len(all_comments))

    # FIXME (task 1): filter all_comments to remove comments that were generated by your bot
  
    print('len(not_my_comments)=',len(not_my_comments))

    
    try:
        if len(not_my_comments) == len(all_comments):
            top_comment = not_my_comments[0]
            for tlc in submission.comments:
                if str(tlc.author) != 'botbotboot' and int(tlc.score) > top_comment.score:
                    top_comment = tlc
            text = generate_comment()
            top_comment.reply(text)

        else:
            comments_without_replies = []
            not_yet_commented = False
            for comment in not_my_comments:
                try:
                    comment.refresh()
                    for reply in comment.replies:
                        if str(reply.author) == 'botbotboot':
                            not_yet_commented = False
                            break
                        else:
                            not_yet_commented = True
                except(AttributeError, praw.exceptions.ClientException):
                    pass
                if not_yet_commented:
                    comments_without_replies.append(comment)
            print('len(comments_without_replies)=',len(comments_without_replies))

            if len(comments_without_replies) > 0:
                comment = random.choice(comments_without_replies)
                comment.reply(generate_comment())

        possible_new_subs = []
        for submission in reddit.subreddit("BotTown2").hot(limit=5):
            possible_new_subs.append(submission)
        submission = random.choice(possible_new_subs)
        while str(submission.author) == "imtherealcs40bot":
            submission = random.choice(possible_new_subs)
        submission.comments.replace_more()
    except praw.exceptions.RedditAPIException:
        time.sleep(100) 

