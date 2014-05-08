#!/bin/bash

# install mpg123

mpg123_path=$(which mpg123)
if [ -z $mpg123_path ]
then
    # install mpg123
    sudo apt-get install mpg123
fi

# install requests
sudo pip3 install requests