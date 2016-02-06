import random
import re

import requests

from plugin_base import GladosPluginBase

# JESUS CHRIST GIPHY IS ACTUALLY AWFUL ABORT ABORT
# TIME TO USE IMGUR API
GIPHY_API_URL_TPL = 'http://api.giphy.com/v1/gifs/search?q={query}&limit=10&api_key=dc6zaTOxFJmzC'

query_re = re.compile(r'glados,?\s+giff?(?:\s+me)?\s+(.*)', re.I)

HELP_TEXT = 'I regret everything.'


class GifMe(GladosPluginBase):
    consumes_message = True

    def can_handle_message(self, msg):
        if msg['type'] != 'message' or 'message' in msg:
            return None
        return query_re.match(msg['text'])

    def handle_message(self, msg):
        query_str = query_re.match(msg['text']).group(1)

        query_url = GIPHY_API_URL_TPL.format(query=query_str)

        r = requests.get(query_url)

        def send_fail_msg(err=None):
            if err:
                print(err)
            self.send('No results found for "{}"'.format(query_str), msg['channel'])

        if r.status_code != requests.codes.ok:
            send_fail_msg()
            return

        response = r.json()
        if not response['data']:
            send_fail_msg()
            return

        img_url = random.choice(response['data'])['images']['downsized']['url']
        attachments = [{
            'fallback': '[inline image]',
            'image_url': img_url
        }]

        self.send('', msg['channel'], attachments)

    @property
    def help_text(self):
        return HELP_TEXT
