#! /usr/bin/env python3
# coding: UTF-8

import config
from twython import Twython, TwythonError, TwythonStreamer, TwythonStreamError
import datetime
import codecs
import time


twitter = Twython(config.TW_CONSUMER_KEY, config.TW_CONSUMER_SECRET,
                      config.TW_TOKEN, config.TW_TOKEN_SECRET)

error_text = ("エラーが発生しました．\n再起動します．")
twitter.update_status(status=tweet)
