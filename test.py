#! /usr/bin/env python3

import re
import config
from twython import Twython, TwythonError, TwythonStreamer, TwythonStreamError

twitter = Twython(


)


class MyStreamer(TwythonStreamer):
    def on_success(self, data):
        if 'text' in data:
            print(data['text'])

    def on_error(self, status_code, data):
        print(status_code)

        # Want to stop trying to get data because of the error?
        # Uncomment the next line!
        # self.disconnect()


stream = MyStreamer(config.TW_CONSUMER_KEY, config.TW_CONSUMER_SECRET,
                    config.TW_TOKEN, config.TW_TOKEN_SECRET)
stream.statuses.filter(track='twitter')
