## what is this

a hardware & software project that lets people attending the [Recurse Center](https://www.recurse.com/) to sign in using their door fob

## how does it work

- an rfid reader is mounted on a plush octopus
- the rfid reader sends the door tag id over usb to a raspi
- the raspi pings the main web server (see source code [here](https://github.com/gregsadetsky/checkintopus))
- the web server responds with audio url(s) to play back. if the door tag is already known, the server signs in the person using the [hub visits api](https://github.com/recursecenter/wiki/wiki/Recurse-Center-API#hub-visits).
- the raspi plays the audio file(s) over speakers mounted on the plush octopus

### where is the code

- the oauth/web/UI server is [here](https://github.com/gregsadetsky/checkintopus)
- the hardware raspberry pi code is in this repo

## Production environment
We use a raspberry pi that is located at the hub and connected to the network via wifi
the pi hostname, ssh credentials, API token and physical location can be found in [recurse wiki](https://github.com/recursecenter/wiki/wiki/Checkintopus)

## Installation

1. install raspbian on a a raspberry pi
1. ssh to it and clone this repo
1. `sudo ./install.sh`
1. in install.sh there will be a prompt asking you from the API access token - put it in
   1. in case you configured this key already you can just press [ENTER] and skip this step
1. ???
1. profit

### Installation notes

be aware that everything runs without a virtualenv and with root permissions

### Update / deploy new code
1. ssh to the running rpi
1. go to the cloned repo
1. `git pull`
1. `sudo ./install.sh`
1. skip the API access token input by pressing enter (unless you need to change it)
1. that's it! -> the installation process reloads the code and restarts the service and therefore no more actions are needed

#### why root?

keyboard library requires us to use root in order to read from /dev/input

#### why without venv?

because we install here a python and launch it from a service it will be harder to do it when there is a virtualenv

#### how to overcome these problems in the future?

dockerize it. it will solve both problems
don't forget to pass the relevant device to the container

## Troubleshooting
1. check the service status:
`service octopus status`
1. restart the service in case something goes wrongs:
`service octopus restart`
1. read the logs easily
`journalctl -u octopus.service`
if you want to troubleshoot it in live you can use the -f flag to get changes:
`journalctl -u octopus.service -f`

### TODO rename project/repos

- based on [poll results](https://recurse.zulipchat.com/#narrow/stream/19042-.F0.9F.A7.91.E2.80.8D.F0.9F.92.BB-current-batches/topic/naming.20suggestion/near/394473437) + randomness

### additional docs

- [hardware parts](_docs/HARDWARE.md)
- [rfid scanner manual](_docs/eh301---manual-came-with-device.pdf)

## reference

- [V.A.L.E.T.](https://github.com/RodEsp/V.A.L.E.T.) -- uses wifi/fixed device MAC addresses to detect people in the space and auto sign them in
- [launch message re VALET](https://recurse.zulipchat.com/#narrow/stream/398504-397-Bridge/topic/V.2EA.2EL.2EE.2ET.2E/near/388175215)
- [info on the visits bot](https://recurse.zulipchat.com/#narrow/stream/398504-397-Bridge/topic/visits-bot!)
- [hub visits API](https://github.com/recursecenter/wiki/wiki/Recurse-Center-API#hub-visits) -- we'll use this to create a visit and to let people sign in using oauth so that we can associate their tag with them

## misc

- there's no way to check out from the hub - except by deleting your hub visit object, as noted by Nick [here](https://recurse.zulipchat.com/#narrow/stream/398504-397-Bridge/topic/visits-bot!/near/384055535). we'll probably leave it as is i.e. this (just like V.A.L.E.T. and the ipad) will be a check-in-only system. everyone gets checked out automatically at midnight by the 'Account Sync Bot'
- [what _is_ rfid/nfc/etc.?](https://blog.flipper.net/rfid/)

## contributors

This project is brought to you by [Kevan](https://github.com/khollbach), [Itay](https://github.com/itay-sho) and [Greg](https://github.com/gregsadetsky).
