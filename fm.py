#!/usr/bin/python3

import os
from douban.cmd import CMD

__version__ = '0.9'

def main():
    print("#" * 80)
    print('{:.^80}'.format('Douban Fm version ' + __version__))
    print("#" * 80)
    # CMD.init()
    while True:
        CMD.main()

if __name__ == '__main__':
    main()