# Final optimized bot
import tweepy
import time
import threading
import logging
from flask import Flask




print("this is my twitter bot \n ")

CONSUMER_KEY = 'x'
CONSUMER_SECRET = 'y'
ACCESS_KEY = 'y'
ACCESS_SECRET = 'a'

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
api = tweepy.API(auth)
print(api.rate_limit_status())


# Using a file to store and access the range of mentions to check

last_seen_id = ''


def store_last_seen_id():
    f = open('last_seen_id.txt', 'w+')
    f.write(str(last_seen_id))
    f.close()


def access_stored_id():
    global last_seen_id
    f = open('last_seen_id.txt', 'r+')
    last_seen_id = f.read()
    f.close()


# Defining the range
access_stored_id()
print('last_seen_id: ' + str(last_seen_id))


# Analysing mentions(from oldest to most recent)

def twit_bot():
    global last_seen_id
    if last_seen_id != '':
        mentions = api.mentions_timeline(last_seen_id)
        api.mentions_timeline(last_seen_id)
    else:  # FIRST RUN
        mentions = api.mentions_timeline()
        api.mentions_timeline()

    for mention in reversed(mentions):
        print('mention: ')
        print(str(mention.id) + ' -- ' + str(
            mention.user.screen_name) + ' - ' + mention.text)  # type tweepy models status
        last_seen_id = mention.id
        store_last_seen_id()
        user_screen_name = '@' + mention.user.screen_name
        user_id = mention.user.id
        # looking for keywords
        if '#helloworld' in mention.text.lower():
            print("#helloworld in text")
            print("responding..... \n")
            api.update_status(status=str(user_screen_name) + ' I Hope you\'re having a wonderful day!',
                              in_reply_to_status_id=str(mention.id), auto_populate_reply_metadata=True)
        if '#world' in mention.text.lower():
            print("#world in text")
            print("responding..... \n")
            api.send_direct_message(int(user_id), 'Hey ' + str(user_screen_name) + ', have a nice day!')
        if '#rt' in mention.text.lower():
            print('#rt in text')
            print('responding..... \n')
            api.retweet(mention.id)
        if '#friend' in mention.text.lower():
            print('#friend in text')
            print('responding..... \n')
            api.create_friendship(user_id, user_screen_name, follow=True)
        if '#like' in mention.text.lower():
            print('#rt in text')
            print('responding..... \n')
            api.create_favorite(mention.id)
        else:
            print("#helloworld not in text")
            print("no response \n")


# Trying to loop that shit


run_count = 0

def run_bot():
    run_count = 0
    while True:
        if run_count != 0:
            print('rerunning... iteration: ' + str(run_count) + '   |  time: ' + str(time.ctime()))
            twit_bot()
        else:
            print('first iteration: time: ' + str(time.ctime()))
            twit_bot()
        run_count += 1
        t = 60
        time.sleep(t)

run_bot()
