#! /usr/bin/env python3
# coding: UTF-8

import re
import config
from twython import Twython, TwythonError, TwythonStreamer, TwythonStreamError
import datetime
import codecs
import win32serviceutil
import logging


logging.basicConfig(
    filename='c:\dev\starwing_service.log',
    level=logging.DEBUG,
    format="%(message)s"
)


class StarwingService(win32serviceutil.ServiceFramework):
    _svc_name_ = 'StarwingBotService'
    _svc_display_name_ = 'Starwing_timesignal_bot'
    _svc_description_ = 'This is timesignal tweet service.'

    def SvcDoRun(self):
        self.run = True
        while self.run:
            stream = MyStreamer(config.TW_CONSUMER_KEY, config.TW_CONSUMER_SECRET,
                                config.TW_TOKEN, config.TW_TOKEN_SECRET)
            stream.statuses.filter(track='#星翼時報')

    def SvcStop(self):
        self.run = False


class MyStreamer(TwythonStreamer):
    def on_success(self, data):
        print('---------------------------------')
        logging.info('---------------------------------')
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
        logging.info(status_code)

    def parse_tweet(self, data):
        dt_now = datetime.datetime.now()
        if 'text' in data:
            username = data['user']['screen_name']
            tweet = []
            time = []

            # if len(re.findall('[0-9]+\/[0-9]+\s+[0-9]+:[0-9]+', data['text'])) or len(re.findall('[0-9]+月[0-9]+日*[0-9]+時[0-9]+分', data['text'])):
            tweet_text = data['text'].splitlines()
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
                    logging.info('no time in line')

            for time_list in time:
                tweet = ("【星翼時報速報】\n %s \n from @%s \n#星翼\n#星翼時報" %
                         (time_list, username))
                print(tweet)
                logging.info(tweet)
                twitter.update_status(status=tweet)
        else:
            print('unkwon error')

        # Want to stop trying to get data because of the error?
        # Uncomment the next line!
        # self.disconnect()


if __name__ == '__main__':
    twitter = Twython(config.TW_CONSUMER_KEY, config.TW_CONSUMER_SECRET,
                      config.TW_TOKEN, config.TW_TOKEN_SECRET)
    win32serviceutil.HandleCommandLine(StarwingService)
