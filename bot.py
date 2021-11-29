import praw
import random
import datetime
import time
import nltk
from textblob import TextBlob


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


# each iteration of this loop will post a single comment;
# since this loop runs forever, your bot will continue posting comments forever;
# (this is what makes it a deamon);
# recall that you can press CTRL-C in the terminal to stop your bot
#
# HINT:
# while you are writing and debugging your code, 
# you probably don't want it to run in an infinite loop;
# you can change this while loop to an if statement to make the code run only once
while True:

    # printing the current time will help make the output messages more informative
    # since things on reddit vary with time
    print()
    print('new iteration at:',datetime.datetime.now())
    print('submission.title=',submission.title)
    print('submission.url=',submission.url)
    submission.comments.replace_more(limit=None)
    # FIXME (task 0): get a list of all of the comments in the submission
    # HINT: this requires using the .list() and the .replace_more() functions
    
    #submission.comments.replace_more(limit=None)
    all_comments = submission.comments.list()
    
    # HINT: 
    # we need to make sure that our code is working correctly,
    # and you should not move on from one task to the next until you are 100% sure that 
    # the previous task is working;
    # in general, the way to check if a task is working is to print out information 
    # about the results of that task, 
    # and manually inspect that information to ensure it is correct; 
    # in this specific case, you should check the length of the all_comments variable,
    # and manually ensure that the printed length is the same as the length displayed on reddit;
    # if it's not, then there are some comments that you are not correctly identifying,
    # and you need to figure out which comments those are and how to include them.
    print('len(all_comments)=',len(all_comments))

    # FIXME (task 1): filter all_comments to remove comments that were generated by your bot
    # HINT: 
    # use a for loop to loop over each comment in all_comments,
    # and an if statement to check whether the comment is authored by you or not
    not_my_comments = []
    for comment in all_comments:
        #print('comment.author=', comment.author)
        #print(type(comment.author)) #redditor
        if str(comment.author) != 'botbotboot':
            not_my_comments.append(comment)


    # HINT:
    # checking if this code is working is a bit more complicated than in the previous tasks;
    # reddit does not directly provide the number of comments in a submission
    # that were not gerenated by your bot,
    # but you can still check this number manually by subtracting the number
    # of comments you know you've posted from the number above;
    # you can use comments that you post manually while logged into your bot to know 
    # how many comments there should be. 
    print('len(not_my_comments)=',len(not_my_comments))

    # if the length of your all_comments and not_my_comments lists are the same,
    # then that means you have not posted any comments in the current submission;
    # (your bot may have posted comments in other submissions);
    # your bot will behave differently depending on whether it's posted a comment or not
    has_not_commented = len(not_my_comments) == len(all_comments)
    print('has_not_commented=', has_not_commented)
   
    if has_not_commented:
        # FIXME (task 2)
        # if you have not made any comment in the thread, then post a top level comment
        #
        # HINT:
        # use the generate_comment() function to create the text,
        # and the .reply() function to post it to reddit;
        # a top level comment is created when you reply to a post instead of a message

        submission.reply(generate_comment())

    else:
        # FIXME (task 3): filter the not_my_comments list to also remove comments that 
        # you've already replied to
        # HINT:
        # there are many ways to accomplish this, but my solution uses two nested for loops
        # the outer for loop loops over not_my_comments,
        # and the inner for loop loops over all the replies of the current comment from the outer loop,
        # and then an if statement checks whether the comment is authored by you or not
        #comments_without_replies = not_my_comments
        # HINT:
        # this is the most difficult of the tasks,
        # and so you will have to be careful to check that this code is in fact working correctly

        comments_without_my_replies = []
        for comment in not_my_comments:
            if comment.author != 'botbotboot':
                response = False
                for reply in comment.replies:
                    if str(reply.author) == 'botbotboot':
                        response = True
                if response is False:
                    comments_without_my_replies.append(comment)
        print('Number of Comments Without My Replies: ', len(comments_without_my_replies))

        # FIXME (task 4): randomly select a comment from the comments_without_replies list,
        # and reply to that comment
        #
        # HINT:
        # use the generate_comment() function to create the text,
        # and the .reply() function to post it to reddit;
        # these will not be top-level comments;
        # so they will not be replies to a post but replies to a message

        for comments in comments_without_my_replies:
            selection = random.choice(comments_without_my_replies)
            generated_reply = generate_comment()
            try:
                selection.reply(generated_reply)
            except praw.exceptions.RedditAPIException as error:
                if "DELETED_COMMENT" in str(error):
                    print("Comment " + comment.id + " was deleted")
                else:
                    print('Error Found: ', error)


    # FIXME (task 5): select a new submission for the next iteration;
    # your newly selected submission should be randomly selected from the 5 hottest submissions
    randomnumber = random.random()
    allsubmissions = []
    if randomnumber >= 0.5:
        print('Original Submission')
        submission = reddit.submission(url='https://www.reddit.com/r/BotTown2/comments/r0yi9l/main_discussion_thread/')
        submission.reply(generate_comment())
    if randomnumber < 0.5:
        print('Top Subreddit Submission')
        for submission in reddit.subreddit('BotTown2').hot(limit=5):
            allsubmissions.append(submission)
        newsubmission = random.choice(allsubmissions)
        submission = reddit.submission(id=newsubmission)
        print('Submission ID: ', newsubmission)
        print(newsubmission.title)

        #Extra Credit 7:

    text = TextBlob(comment.body)
    if ("Obama" in text.lower() and text.sentiment.polarity>0.5) or ("trump" in text.lower() and text.sentiment.polarity<-0.5):
            comment.upvote()
    elif ("Obama" in text.lower() and text.sentiment.polarity<-0.5) or ("trump" in text.lower() and text.sentiment.polarity>0.5):
            comment.downvote()
    print ('len(text.lower())=', len(text.lower()))

    time.sleep(700)

