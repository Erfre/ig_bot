#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Okay now its time to follow people and unfollow them
# Maybe I  can work with tags and follow releated content
# what i will do is keep 2 different bots, one which uses api to post and
# one which uses different api for following and managing account
import sys

sys.path.insert(0, '/home/lqa/PycharmProjects/InstaPy/')
from instapy import InstaPy
from json_loader import get_account

user, pw = get_account()

session = InstaPy(username = user, password = pw)
session.login()



