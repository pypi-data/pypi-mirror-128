#!/usr/bin/env python3

import re
import requests
import bleach # no way in hell we trust element to not get pwned
import aiohttp, asyncio

def get_hashtags(input_string):
    """
    used to get #hastags from a inout string
    often you can find them in telegram chats
    """
    if len(input_string) > 0:
        hashtags = []
        r = re.compile("(#)+(\w{2,32})")
        for match in r.finditer(input_string):
            hashtags.append(match.group())
        return hashtags



def fix_up(str_in):
    """
    used to fix strings before being passed to the
    entity extractor
    """
    if str_in:
        no_ws = re.sub("\s+", " ", str_in)
        no_hashes = re.sub("(#)+(\w{2,32})", "", no_ws)
        no_hashes = re.sub('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))', '', no_hashes, flags=re.MULTILINE)
        no_hashes = re.sub('[\S]+\.(net|com|org|info|edu|gov|uk|de|ca|jp|fr|au|us|ru|ch|it|nel|se|no|es|mil)[\S]*\s?','', no_hashes, flags=re.MULTILINE)
        clean = no_hashes.lower()

    return clean


def send_alert(message, username, source, event_type, endpoint, path=None):
    data = {}
    data["source"] = source
    data["message"] = message
    data["type"] = event_type
    data["username"] = username
    if path:
        data["path"] = path
    try:
        requests.post(endpoint, json=data)
    except requests.exceptions.RequestException as e:
        print(e)


def safe(str_in):
    """
    used to clean up textbefore being sent.
    that way so targets can not mass ping in the
    alert destinations
    """
    clean = str_in.replace("@", ".@")
    clean = bleach.clean(clean)
    return clean


class Imgbb():
    """Used to upload files to imgbb"""
    def __init__(self, key, session=None):
        self.key = key
        self.url = "https://api.imgbb.com/1/upload"
        if session is None:
            self.session = aiohttp.ClientSession()
            self.close = True
        else:
            self.session = session

    async def post(self, filename, name):
        """post by filename"""
        with open(filename, "rb") as image:
            data = {"key": self.key,
                    "image": image.read(),
                    "name": name}
            async with self.session.post(self.url, data=data) as response:
                resp = await response.json()
                return resp

            if self.close:
                self.session.close()
