# Installation

1. install raspbian on a a raspberry pi
1. ssh to it and clone this repo
1. sudo ./install.sh
1. in install.sh there will be a prompt asking you from the API access token - put it in
    1. in case you configured this key already you can just press [ENTER] and skip this step
1. ???
1. profit

## Notes
be aware that everything runs without a virtualenv and with root permissions
### why root?
keyboard library requires us to use root in order to read from /dev/input

### why without venv?
because we install here a python and launch it from a service it will be harder to do it when there is a virtualenv

### how to overcome these problems in the future?
dockerize it. it will solve both problems
don't forget to pass the relevant device to the container