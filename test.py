#! /usr/bin/env python3

import re
import config
from twython import Twython, TwythonError, TwythonStreamer, TwythonStreamError


class MyStreamer(TwythonStreamer):
    def on_success(self, data):
        if 'text' in data:
            print(data['text'])
            if len(re.findall('[0-9]+:[0-9]+', str(data['text']))):
                if len(re.findall('[0-9]+\/[0-9]+\s+[0-9]+:[0-9]+', str(data['text']))):
                    time = re.findall(
                        '[0-9]+\/[0-9]+\s+[0-9]+:[0-9]+', str(data['text']))
                    print(time)
                else:
                    time = re.findall(
                        '[0-9]+:[0-9]+', str(data['text']))
                    print(time, 'no date')
            elif len(re.findall('[0-9]+時[0-9]+分', str(data['text']))):
                if len(re.findall('[0-9]+月[0-9]+日*[0-9]+時[0-9]+分', str(data['text']))):
                    time = re.findall('[0-9]+時[0-9]+分', str(data['text']))
                    print(time)
                else:
                    time = re.findall('[0-9]+時[0-9]+分', str(data['text']))
                    print(time, 'jap_nodate')
            # twitter.update_status(status=data['text'])

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
