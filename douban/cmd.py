import sys
import functools
from . import parse
import random
from .player import Player
import readline
import requests
import time
from multiprocessing import Process
import os
import subprocess
import re

RESET_COLOR = "\033[0m"
 
COLOR_CODES = {                                                                     
    "blue" : "\033[1;34m", # blue                                                  
    "green" : "\033[1;32m", # green                                                  
    "yellow" : "\033[1;33m", # yellow                                              
    "red" : "\033[1;31m", # red                                                   
    "background_red" : "\033[1;41m", # background red                                     
}                                                                                   
 
def color_msg(color, msg):                                                          
    return COLOR_CODES[color] + msg + RESET_COLOR

def output(text):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            print(color_msg('green', text))
            print('-' * 80)
            func(*args, **kwargs)
            print('-' * 80)
        return wrapper
    return decorator

# Custom completer
class MyCompleter():  

    def __init__(self, options):
        self.options = sorted(options)

    def complete(self, text, state):
        if state == 0:  # on first trigger, build possible matches
            if text:  # cache matches (entries that start with entered text)
                self.matches = [s for s in self.options 
                                    if s and s.startswith(text)]
            else:  # no text entered, all matches possible
                self.matches = self.options[:]

        # return match indexed by state
        try: 
            return self.matches[state]
        except IndexError:
            return None

class _GetchUnix:
    def __init__(self):
        import tty, sys

    def __call__(self):
        import sys, tty, termios
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch

g = _GetchUnix()

class CMD:
    commands = {
        'help':     'Show help',
        'login':    'Login to douban.fm',
        'channel':  'Show channel list',
        'play':     'Format: play <channel_id>. Play a channel. or play a random channel',
        'quit':     'quit from the app'
    }

    p = None
    play_pid = None
    douban = parse.Douban()
    channels = douban.channels()
    completer = MyCompleter(["help", "login", "channel", "play", "quit"])
    channel_id = random.randint(1, len(channels))
    songs = douban.song_list(channel_id)

    @classmethod
    def init(cls):
        if cls.douban.test_login():
            print(color_msg('background_red', "welcome " + cls.douban.user_name))

    @classmethod
    def main(cls):
        sys.stdout.write('>> ')
        readline.set_completer(cls.completer.complete)
        readline.parse_and_bind('tab: complete')
        command = input()
        if command == '':
            pass
        elif command == 'help':
            CMD.help()
        elif command == 'login':
            CMD.login()
        elif command == 'logout':
            CMD.logout()
        elif command == 'channel':
            CMD.channel()
        elif command.startswith('play'):
            if command == 'play':
                print("waiting...")
                cls.play()
                #cls.p = Process(target=cls.play())
                #cls.p.start()
            elif re.match(r'\d+', command.split(' ')[1]):
                cls.channel_id = command.split(' ')[1]
                cls.play()
                print("waiting...")
                #cls.p = Process(target=cls.play)
                #cls.p.start()
            else:
                print(color_msg('red'), 'Please try another channel')
            
        elif command == 'stop':
            CMD.stop()
        elif command == 'pause':
            CMD.pause()
        elif command == 'resume':
            CMD.resume()
        elif command == 'loop':
            CMD.loop()
        elif command == 'next':
            pass
        elif command == 'prev':
            CMD.prev()
        elif command == 'delete':
            CMD.delete()
        elif command == 'like':
            CMD.like()
        elif command == 'mute':
            CMD.mute()
        elif command == 'up':
            CMD.up()
        elif command == 'down':
            CMD.down()
        elif command == 'quit':
            CMD.stop()
        else:
            print(color_msg('background_red', "Wrong choice, please try <help>"))

    @classmethod
    def login(cls):
        while not cls.douban.test_login():
            cls.douban.login()
        print(color_msg('background_red', "welcome " + cls.douban.user_name))

    @classmethod
    # help
    @output('Available Commands')
    def help(cls):
        for key, value in cls.commands.items():
            print(color_msg('red', key + ' ----> ' + value))

    @staticmethod
    def stop():
        Player.stop()
        print("Bye")
        sys.exit()

    @classmethod
    def play(cls):
        # song_length = len(cls.songs)
        n = -1
        cls.play_pid = os.getpid()
        while True:
            n += 1
            t_minutes, t_seconds = divmod(cls.songs[n]['length'], 60)
            picture = 'images/' + cls.songs[n]['picture'].split('/')[4]
            if not os.path.exists(picture):
                subprocess.Popen([
                    'wget',
                    '-P',
                    'images',
                    cls.songs[n]['picture']], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            subprocess.Popen([
                'notify-send',
                '-i',
                os.getcwd() + '/' + picture,
                cls.songs[n]['title'],
                cls.songs[n]['artist'] + '\n' + cls.songs[n]['albumtitle']])

            @output('Now playing: ')
            def __print_song():
                print(color_msg('blue', "song title: " + cls.songs[n]['title']))
                print(color_msg('blue', "artist: " + cls.songs[n]['artist']))
                print(color_msg('blue', "album: " + cls.songs[n]['albumtitle']))
                print(color_msg('blue', "song length: " + str(t_minutes) + ":" + str(t_seconds)))
            __print_song()
            p = Process(target=cls._play, args=(cls.songs[n]['url'],))
            p.start()
            p.join()
    
    @staticmethod         
    def _play(url):
        Player.play(url)

    @classmethod
    @output("Available channels: ")
    def channel(cls):
        channels = cls.douban.channels()
        for c in channels:
            print(color_msg('green', 'channel ' + str(c['channel_id']) + '\t' + c['name']))