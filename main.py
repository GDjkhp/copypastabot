import cv2
import os
import math
import facebook
import functools
import schedule
import time
import fnmatch
import sys

import praw
from psaw import PushshiftAPI
import datetime as dt
from itertools import tee

def catch_exceptions(cancel_on_failure=False):
    def catch_exceptions_decorator(job_func):
        @functools.wraps(job_func)
        def wrapper(*args, **kwargs):
            try:
                return job_func(*args, **kwargs)
            except:
                import traceback
                print(traceback.format_exc())
                if cancel_on_failure:
                    return schedule.CancelJob
        return wrapper
    return catch_exceptions_decorator

@catch_exceptions()
def newpost(msg, info):
    # Facebook token + api stuff
    with open('token.txt','r') as token:
        accesstoken = token.readline()
    graph = facebook.GraphAPI(accesstoken)
    
    # Info
    print("\n", info)
    
    # To post text only
    graph.put_object(parent_object = 'me', connection_name = 'feed', message = msg)
    
    # Info
    print("Submitted post successfully")
    
    # Increment item if no errors
    item+=1;

# Main counter    
item = 0;
if __name__ == '__main__':
    # Reddit token + api stuff
    r = praw.Reddit("bot1", user_agent="shitshow")
    api = PushshiftAPI(r)
    
    # TODO: Input date
    
    # Submissions
    submissions = api.search_submissions(subreddit='copypasta', 
        after= int(dt.datetime(2022, 3, 22).timestamp()), # (YYYY, MM, DD)
        before=int(dt.datetime(2022, 3, 23).timestamp()), # (YYYY, MM, DD)
        limit=1000)
    gen1, gen2 = tee(submissions)
    
    # Info
    count = 1
    for submission in gen2:
        test = str(count) + ". " + str(submission.title) + " by " + str(submission.author) + " (" + str(submission.shortlink) + ")"
        print(test)
        count+=1
    print("\n")
    
    # List
    testlist = []
    infolist = []
    
    # Confirm
    ans = input("Start posting about among us? (y/n) \n>")
    if 'n' in ans.lower():
        exit()
    else:
        pass
    
    # Convert
    count = 1
    for submission in gen1:
        test = str(submission.title) + " by " + str(submission.author) + " (" + str(submission.shortlink) + ")\n\n" + str(submission.selftext)
        info = str(count) + ". " + str(submission.title) + " by " + str(submission.author) + " (" + str(submission.shortlink) + ")"
        testlist.append(test)
        infolist.append(info)
        count+=1
        
    # Post
    while item < len(testlist):
        newpost(testlist[item], infolist[item])
        time.sleep(60) # the value was in seconds
    
    
#    for submission in gen2:
#        print("submission:", submission)
#        print("submission.title:", submission.title)
#        print("submission.author:", submission.author)
#        print("submission.shortlink:", submission.shortlink, "\n")
#        print("submission.selftext:", submission.selftext, "\n")