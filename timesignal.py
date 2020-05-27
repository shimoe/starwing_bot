#! /usr/bin/env python3
# coding: UTF-8

import re
import config
from twython import Twython, TwythonError, TwythonStreamer, TwythonStreamError
import datetime
import codecs


class MyStreamer(TwythonStreamer):
    def on_success(self, data):
        print('---------------------------------')
        if 'retweeted_status' in data:
            print('Retweeted tweet')
        elif data['user']['screen_name'] == 'SW_Timesignal':
            print('self tweet')
        elif 'quoted_status' in data:
            print('Quoted tweet')
        else:
            self.parse_tweet(data)

    def on_error(self, status_code, data):
        print(status_code)

    def parse_tweet(self, data):
        dt_now = datetime.datetime.now()
        if 'text' in data:
            username = data['user']['screen_name']
            tweet = []
            time = []

            if len(re.findall('[0-9]+\/[0-9]+\s+[0-9]+:[0-9]+', data['text'])) or len(re.findall(
                    '[0-9]+月[0-9]+日*[0-9]+時[0-9]+分', data['text'])):
                print('date exist')
                time.append(re.findall(
                    '[0-9]+\/[0-9]+\s+[0-9]+:[0-9]+', data['text']))
                time.append(re.findall(
                    '[0-9]+月[0-9]+日*[0-9]+時[0-9]+分', data['text']))
            else:
                print('date no exist')
                time.append(re.findall('[0-9]+:[0-9]+', data['text']))
                time.append(re.findall('[0-9]+時[0-9]+分', data['text']))

            print(time)
            print('*******************')

            if len(time):
                for index, item in enumerate(time):
                    if not len(re.findall('\/', str(item))):
                        time[index] = (str(dt_now.month) + '/' +
                                       str(dt_now.day) + ' ' + str(item))
                    elif not len(re.findall('日', str(item))):
                        time[index] = (str(dt_now.month) + '月' +
                                       str(dt_now.day) + '日' + ' ' + str(item))
                    # time[0] = str(dt_now.month) + '月' + \
                    #    str(dt_now.day) + '日 ' + str(time[0])
                print(time)

                tweet = ("【星翼時報速報】\n %s \n from @%s \n#星翼\n#星翼時報" %
                         (time[0], username))
                print(tweet)
                # twitter.update_status(status=tweet)
            else:
                print('Time is not including.')
                print(data['text'])
        else:
            print('unkwon error')
            print(data, sep='\n', end='------------------------------',
                  file=codecs.open('log.txt', 'w', 'utf-8'))

        # Want to stop trying to get data because of the error?
        # Uncomment the next line!
        # self.disconnect()


while True:
    twitter = Twython(config.TW_CONSUMER_KEY, config.TW_CONSUMER_SECRET,
                      config.TW_TOKEN, config.TW_TOKEN_SECRET)
    stream = MyStreamer(config.TW_CONSUMER_KEY, config.TW_CONSUMER_SECRET,
                        config.TW_TOKEN, config.TW_TOKEN_SECRET)
    stream.statuses.filter(track='#星翼時報')
