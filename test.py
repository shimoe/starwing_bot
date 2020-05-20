#! /usr/bin/env python3
#coding: UTF-8

import re
import config
from twython import Twython, TwythonError, TwythonStreamer, TwythonStreamError
import datetime


class MyStreamer(TwythonStreamer):
    def on_success(self, data):
        if 'text' in data:
            print(data['text'])
            if len(re.findall('[0-9]+:[0-9]+', str(data['text']))):
                if len(re.findall('[0-9]+\/[0-9]+\s+[0-9]+:[0-9]+', str(data['text']))):
                    time = re.findall(
                        '[0-9]+\/[0-9]+\s+[0-9]+:[0-9]+', str(data['text']))
                    print(time[0])
                else:
                    dt_now = datetime.datetime.now()
                    time = re.findall(
                        '[0-9]+:[0-9]+', str(data['text']))
                    time[0] = str(dt_now.month) + '/' + \
                        str(dt_now.day) + ' ' + str(time[0])
                    print(time[0])
            elif len(re.findall('[0-9]+時[0-9]+分', str(data['text']))):
                if len(re.findall('[0-9]+月[0-9]+日*[0-9]+時[0-9]+分', str(data['text']))):
                    time = re.findall(
                        '[0-9]+月[0-9]+日*[0-9]+時[0-9]+分', str(data['text']))
                    print(time[0])
                else:
                    time = re.findall('[0-9]+時[0-9]+分', str(data['text']))
                    time[0] = str(dt_now.month) + '月' + \
                        str(dt_now.day) + '日 ' + str(time[0])
                    print(time[0])
            username = data['user']['screen_name']
            tweet = ("【星翼時報速報】\n %s \n from @%s \n#星翼\n#星翼時報" %
                     (time[0], username))
            print(tweet)
#            twitter.update_status(status=tweet)

    def on_error(self, status_code, data):
        print(status_code)

        # Want to stop trying to get data because of the error?
        # Uncomment the next line!
        # self.disconnect()


twitter = Twython(config.TW_CONSUMER_KEY, config.TW_CONSUMER_SECRET,
                  config.TW_TOKEN, config.TW_TOKEN_SECRET)
stream = MyStreamer(config.TW_CONSUMER_KEY, config.TW_CONSUMER_SECRET,
                    config.TW_TOKEN, config.TW_TOKEN_SECRET)
stream.statuses.filter(track='#星翼時報')
