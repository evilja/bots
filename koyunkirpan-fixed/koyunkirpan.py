from __future__ import unicode_literals
import praw
import os
import sys
import time
import random
from psaw import PushshiftAPI
from binary_comb import BinComb
from praw.models import Message
from prawcore.exceptions import ServerError
import secrets
import warnings
import numpy as np
from pathlib import Path
from difflib import SequenceMatcher
import evilparserdev


warnings.filterwarnings('ignore')

reddit = praw.Reddit("koyunkirpan",config_interpolation="basic")
def randomsel(len_of_list):
    return random.randint(0,len_of_list-1)
username = "ehl-ikalem"



class runner:
    def __init__(self):
        self.posts = []
        self.comments = []
        self.commented_on = []
        self.flairs = []
        self.keywords = []
        self.subreddit = reddit.subreddit('herseycokguzelolacak')
        self.forbidden_comments = ['[removed]', '[deleted]', '', ' ', None]
        self.abs_path = Path(__file__).parent
        self.search_limit = 20
        self.post_limit = 50
        self.alike_value = 1.37



    def reply_on_comment(self, keyws=""):

        api = PushshiftAPI(reddit)

        all_comments = []
        comments = []
        keywords = keyws.split()
        keywords.sort(key=lambda x: -len(x))
        keywords = keywords[:6] #max keywords
        x = BinComb(keywords)
        searches = x.get_combinations()

        print("Comment:", keyws)
        print("Searches:", len(searches))

        for search in searches[:2]: #searches:

            print("\nStarting search %s:" % (searches.index(search) + 1))
            comments.append([])

            gen = api.search_comments(q=search, subreddit='KGBTR',limit=1000)
            cache = []

            for comment in gen:
                if len(cache) > 1000:
                    break
                if comment.body == '[deleted]' or comment.body == '[removed]':
                    continue
                if len(comment.body.split()) >= len(keywords) * 3:
                    continue
                if comment not in all_comments:
                    cache.append(comment)

            comments[searches.index(search)] += cache
            all_comments += cache
            if len(cache) > 2:
                break

        print("\nENDED.")

        for result in comments:
            print("Length:", len(result))
            c = None
            if len(result) >= 1:
                tries = 0
                while True:
                    if len(result) == 0:
                        break
                    c = result[secrets.randbelow(len(result))]
                    c.refresh()
                    if len(c.replies) >= 1:
                        break
                    else:
                        result.remove(c)
                        c = None
            if c:
                break

        if c:
            to_comment = []
            for reply in c.replies:
                if reply.body not in self.forbidden_comments:
                    to_comment.append(reply.body)
            return to_comment[randomsel(len(to_comment))]


pulldata = runner()
subred = pulldata.subreddit
evilparser = evilparserdev.crystal()
config = evilparser.get("_kgbtr_for_flair.eparse")
def getRandomMessageByFlair(flair):
    if flair == None:
        return None
    flair = flair.lower()
    for flairx in list(config.keys()):
        if flair in flairx:
            return config[flairx][randomsel(len(config[flairx]))]
    return None
def setAsRepliedPost(post_id):
    with open("database.wx","a+") as f:
        f.write(post_id + "\n")
def checkIfReplied(post_id):
    with open("database.wx","r") as f:
        for line in f:
            line = line.strip()
            if post_id in line:
                return True
    return False
notReplied = True
print("Started...")
while True:
    for comment in reddit.inbox.unread(limit=15):
        commentx = comment.body.lower().replace("u/"+username,"")
        getCom = pulldata.reply_on_comment(commentx)
        comment.mark_read()
        print(getCom)
        if getCom == None:
            continue
        if len(getCom) == 0:
            continue
        comment.reply(body=getCom)
        print("C Replied to:", comment.id)
    countOfPosts = 0
    posts = []
    if notReplied:
        OneInPosts = random.randint(2,7)
        print("Selected Count: %s" % OneInPosts)
        notReplied = False
    else:
        for post in subred.new(limit=10):
            if checkIfReplied(post.id):
                continue
            if countOfPosts == OneInPosts:
                break
            posts.append(post)
            countOfPosts += 1
        if countOfPosts >= OneInPosts:
            notReplied = True
            getCom = pulldata.reply_on_comment(posts[0].title)
            if getCom == None:
                newCom = getRandomMessageByFlair(posts[0].link_flair_text)
                print("Flair Text : %s" % newCom)
                if newCom == None:
                    for post in posts:
                        setAsRepliedPost(post.id)
                    continue
                posts[0].reply(body=newCom)
            if len(getCom) == 0:
                continue
            posts[0].reply(body=getCom)
            for post in posts:
                setAsRepliedPost(post.id)
            print("P Replied to:", posts[0].id)
