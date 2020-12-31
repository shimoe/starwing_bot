#! /usr/bin/env python3
# coding: UTF-8

import re
import config
from twython import Twython, TwythonError, TwythonStreamer, TwythonStreamError
import datetime
import codecs
import time
import sys
import logging

logging.basicConfig(level=logging.DEBUG, format='%(levelname)s: %(message)s')
logging.disable(logging.CRITICAL)

class MyStreamer(TwythonStreamer):
    def on_success(self, data):
        # logging.debug('---------------------------------')
        time.sleep(3)
        if 'retweeted_status' in data:
            status = 'retweeted'
           # logging.debug('Retweeted tweet')
        elif data['user']['screen_name'] == 'SW_Timesignal':
            status = 'self_tweet'
           # logging.debug('self tweet')
        else:
           # logging.debug('target tweet')
            self.parse_tweet(data)

    def on_error(self, status_code, data):
        status = 'error'
      #  logging.debug(status_code)

    def serch_time_inline(self, text):
       # logging.debug(text)
       # logging.debug('*****************')
        dt_now = datetime.datetime.now()
        timesignal = []
        tweet_text = text.splitlines()
        # logging.debug(tweet_text)
        for line in tweet_text:
            if len(re.findall('[0-9]+:[0-9]+', line)) > 0:
                if len(re.findall('[0-9]+\/[0-9]+\s+[0-9]+:[0-9]+', line)):
                    timesignal.extend(re.findall(
                        '[0-9]+\/[0-9]+\s+[0-9]+:[0-9]+', line))
                else:
                    nodate = re.findall('[0-9]+:[0-9]+', line)
                    for i in nodate:
                        item = str(dt_now.month) + '/' + \
                            str(dt_now.day) + ' ' + i
                        timesignal.append(item)
            elif len(re.findall('[0-9]+分', line)) > 0 or len(re.findall('[0-9]+時', line)) > 0:
                # logging.debug('jap')
                if len(re.findall('[0-9]+分', line)) > 0 and len(re.findall('[0-9]+時', line)) < 1:
                    #logging.debug('no hour')
                    nohour = re.findall('[0-9]+分', line)
                    for i in nohour:
                        time_value = re.findall('[0-9]+', i)
                        if int(dt_now.minute) < int(time_value[0]):
                            item = str(dt_now.month) + '月' + str(dt_now.day) + \
                                '日' + ' ' + str(dt_now.hour) + '時' + i
                            timesignal.append(item)
                        else:
                            item = str(dt_now.month) + '月' + str(dt_now.day) + \
                                '日' + ' ' + str(int(dt_now.hour) + 1) + '時' + i
                            timesignal.append(item)
                elif len(re.findall('[0-9]+分', line)) < 1 and len(re.findall('[0-9]+時', line)) > 0:
                    #logging.debug('no minute')
                    nominute = re.findall('[0-9]+時', line)
                    for i in nominute:
                        item = str(dt_now.month) + '月' + str(dt_now.day) + \
                            '日' + ' ' + i + '00分'
                        timesignal.append(item)
                elif len(re.findall('[0-9]+時[0-9]+分', line)) > 0:
                    #logging.debug('time in line')
                    if len(re.findall('[0-9]+月[0-9]+日\s[0-9]+時[0-9]+分', line)):
                        timesignal.extend(re.findall(
                            '[0-9]+月[0-9]+日\s[0-9]+時[0-9]+分', line))
                    else:
                        nodate = re.findall('[0-9]+時[0-9]+分', line)
                        for i in nodate:
                            item = str(dt_now.month) + '月' + str(dt_now.day) + \
                                '日' + ' ' + i
                            timesignal.append(item)
            else:
                status = 'no_time_in_line'
               # logging.debug('no time in line')

        return timesignal

    def parse_tweet(self, data):

        if 'text' in data:
            username = data['user']['screen_name']
            tweet = []
            timesignal = []

            if 'quoted_status' in data:
               # logging.debug('Quoted tweet')
                base_text = data['text'].splitlines()
                quoted_text = data['quoted_status']['text'].splitlines()

                for base in base_text:
                    tag_in_base = True if len(
                        re.findall('#星翼時報', base)) > 0 else False
                for quote in quoted_text:
                    tag_in_quoted = True if len(
                        re.findall('#星翼時報', quote)) > 0 else False

                if tag_in_base == True and tag_in_quoted == False:
                    logging.debug('tag in base')
                    timesignal = self.serch_time_inline(
                        data['quoted_status']['text'])
                elif tag_in_base == False and tag_in_quoted == True:
                    logging.debug('tag in quote')
                    timesignal = self.serch_time_inline(
                        data['text'])
                else:
                    timesignal = self.serch_time_inline(data['text'])
                   # logging.debug('tag in both')
            else:
                timesignal = self.serch_time_inline(data['text'])

            for time_list in timesignal:
                tweet = ("【星翼時報速報】\n %s \n from @%s \n#星翼\n#星翼時報" %
                         (time_list, username))
                # logging.debug(tweet)
                twitter.update_status(status=tweet)
                # resources = twitter.get_application_rate_limit_status()

        else:
           # logging.debug('unkwon error')
           # logging.debug(data, sep='\n', end='------------------------------',file=codecs.open('log.json', 'w', 'utf-8'))
            self.disconnect()

class TweetEditor():
    def delete_tweet(self):
        response = twitter.get_mentions_timeline(count=1)
        if 'text' in response:
            logging.debug(response['id'])
            response_text = response['text'].splitlines()
            for line in response_text:
                if re.match('削除', line):
                   # twitter.destroy_status(id=response['id'])
                    
            
if __name__ == '__main__':
    
    # logging.debug('awakening...')
    twitter = Twython(config.TW_CONSUMER_KEY, config.TW_CONSUMER_SECRET,
                      config.TW_TOKEN, config.TW_TOKEN_SECRET)
    stream = MyStreamer(config.TW_CONSUMER_KEY, config.TW_CONSUMER_SECRET,
                        config.TW_TOKEN, config.TW_TOKEN_SECRET)

    # フォロワーのアカウントデータを取得
    follower_list = twitter.get_followers_ids(count=400)  # デフォルトで20
    follow_list = twitter.get_friends_ids(count=400)
    not_followed_list = set(follower_list['ids']) ^ set(follow_list['ids'])
    for follower in list(not_followed_list):
        try:
            twitter.create_friendship(user_id=follower)
        except TwythonError:
            continue
    # 時報監視
    stream.statuses.filter(track='#星翼時報')
        
