#! /usr/bin/env python3
# coding: UTF-8

import re
import config
from twython import Twython, TwythonError, TwythonStreamer, TwythonStreamError
import datetime
import codecs
import time


class MyStreamer(TwythonStreamer):
    def on_success(self, data):
        print('---------------------------------')
        time.sleep(5)
        if 'retweeted_status' in data:
            print('Retweeted tweet')
        elif data['user']['screen_name'] == 'SW_Timesignal':
            print('self tweet')
        else:
            self.parse_tweet(data)

    def on_error(self, status_code, data):
        print(status_code)

    def serch_time_inline(self, text):
        dt_now = datetime.datetime.now()
        time = []
        tweet_text = text.splitlines()
        # print(tweet_text)
        for line in tweet_text:
            if len(re.findall('[0-9]+:[0-9]+', line)) > 0:
                if len(re.findall('[0-9]+\/[0-9]+\s+[0-9]+:[0-9]+', line)):
                    time.extend(re.findall(
                        '[0-9]+\/[0-9]+\s+[0-9]+:[0-9]+', line))
                else:
                    nodate = re.findall('[0-9]+:[0-9]+', line)
                    for i in nodate:
                        item = str(dt_now.month) + '/' + \
                            str(dt_now.day) + ' ' + i
                        time.append(item)
            elif len(re.findall('[0-9]+時[0-9]+分', line)) > 0:
                if len(re.findall('[0-9]+月[0-9]+日\s[0-9]+時[0-9]+分', line)):
                    time.extend(re.findall(
                        '[0-9]+月[0-9]+日\s[0-9]+時[0-9]+分', line))
                else:
                    nodate = re.findall('[0-9]+時[0-9]+分', line)
                    for i in nodate:
                        item = str(dt_now.month) + '月' + str(dt_now.day) + \
                            '日' + ' ' + i
                        time.append(item)
            else:
                print('no time in line')

        return time

    def parse_tweet(self, data):

        if 'text' in data:
            username = data['user']['screen_name']
            tweet = []
            time = []

            if 'quoted_status' in data:
                print('Quoted tweet')
                base_text = data['text'].splitlines()
                quoted_text = data['quoted_status']['text'].splitlines

                for base in base_text:
                    tag_in_base = True if len(
                        re.findall('#星翼時報', base)) > 0 else False
                for quote in quoted_text:
                    tag_in_quoted = True if len(
                        re.findall('#星翼時報', quote)) > 0 else False

                if tag_in_base == True and tag_in_quoted == False:
                    time = self.serch_time_inline(data['text'])
                elif tag_in_base == False and tag_in_quoted == True:
                    time = self.serch_time_inline(
                        data['quoted_status']['text'])
                else:
                    print('hash tag in both')
            else:
                time = self.serch_time_inline(data['text'])

            for time_list in time:
                tweet = ("【星翼時報速報】\n %s \n from @%s \n#星翼\n#星翼時報" %
                         (time_list, username))
                print(tweet)
                twitter.update_status(status=tweet)
                # resources = twitter.get_application_rate_limit_status()

        else:
            print('unkwon error')
            print(data, sep='\n', end='------------------------------',
                  file=codecs.open('log.json', 'w', 'utf-8'))
            self.disconnect()

    # Want to stop trying to get data because of the error?
    # Uncomment the next line!
    # self.disconnect()


print('awakening...')
while True:
    twitter = Twython(config.TW_CONSUMER_KEY, config.TW_CONSUMER_SECRET,
                      config.TW_TOKEN, config.TW_TOKEN_SECRET)
    stream = MyStreamer(config.TW_CONSUMER_KEY, config.TW_CONSUMER_SECRET,
                        config.TW_TOKEN, config.TW_TOKEN_SECRET)
    stream.statuses.filter(track='#星翼時報')
