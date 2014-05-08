#!/usr/bin/python3
# -*- coding: utf-8 -*-

import requests

class Douban:
    """ Douban class, defines a bunch of operations
    """
    base_url = 'http://www.douban.com'
    app_name = 'radio_desktop_win'
    version = '100'

    def __init__(self):
        try:
            from . import config
        except ImportError:
            pass
        else:
            self.email = config.EMAIL
            self.password = config.PASSWORD

    # login() operation
    # params: {email: your email, password: your password}
    def login(self):
        # get password
        import getpass
        self.email = input("Please input your email: ")
        self.password = getpass.getpass('password: ')
    
    def test_login(self):
        if not (hasattr(self, 'email') and hasattr(self, 'password')):
            self.login()
        payload = {'email': self.email, 'password': self.password, 'app_name': self.app_name, 'version': self.version}
        r = requests.post(self.base_url + '/j/app/login', params=payload, headers={'Content-Type': 'application/x-www-form-urlencoded'})
        if r.json()['r'] == 0:
            self.user_id = r.json()['user_id']
            self.expire = r.json()['expire']
            self.user_token = r.json()['token']
            self.user_name = r.json()['user_name']
            return True
        else:
            return False

    # get the channels
    def channels(self):
        channels_url = self.base_url + '/j/app/radio/channels'
        r = requests.get(channels_url)
        return r.json()['channels']

    def get_type(self):
        return 'n'

    def song_list(self, channel_id):
        song_list_url = self.base_url + '/j/app/radio/people'
        if self.test_login():
            payload = {'app_name': self.app_name, 'version': self.version, 'user_id': self.user_id, 
                'expire': self.expire, 'token': self.user_token, 'channel': channel_id, 'type': self.get_type()}
        else:
            payload = {'app_name': self.app_name, 'version': self.version, 'channel': channel_id, 'type': self.get_type()}
        r = requests.get(song_list_url, params=payload)

        # 0: success, 1: error
        if r.json()['r'] == 0:
            songs = r.json()['song']
            return songs