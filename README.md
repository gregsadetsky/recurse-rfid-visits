## what is this

a hardware/software things that lets people attending the [Recurse Center](https://www.recurse.com/) to sign in using their door fob

## how does it work

- rfid reader mounted on/around octopus
- rfid reader sends door tag id over usb to raspi
- raspi pings oauth/main web server
- web server responds with audio url to play and if the tag is already known, signs in the person using the hub visits api
- raspi plays audio file over speakers mounted on/around octopus

### TODO main tasks

- write/finish/polish setup/main oauth (django?) server. basic features:

  1. oauth sign up flow (sort of micro prototyped with flask/oauth) -->> sign in, scan badge ... 3 times?, then setup whether you want no sound/specific sound/community random sound
  2. respond to octodoor door scans i.e. check if known rc person ID + have oauth token for them, log, play back configured sound, ping hub visit API

- host server - where? dokku + digital ocean...? render-ish?

### TODO rename project/repo

- rename this as this project is really happening now!! maybe "octodoor"??
- but it's not a door management system... octovisit? octohub...??? put it up to the community & see?

### FWUP hardware to be received (as of sep 29 -- currently dealing with usps)

- [Raspberry Pi 4 Model B 1GB](https://chicagodist.com/products/raspberry-pi-4-model-b-1gb)
- [raspi case](https://chicagodist.com/products/raspberry-pi-4-case-red-white)
- [raspi power supply](https://chicagodist.com/products/raspberry-pi-4-psu-us-white)
- [raspi sd card w/pre-installed OS ](https://chicagodist.com/products/raspberry-pi-official-noobs-microsd-card)

### TODO hardware checks

- sanity raspi tests upon receiving:
  - does the raspi boot/work? does basic wifi access work?
  - does raspi sound work via the audio jack? need any weird alsa config? what CLI command works to play audio? aplay? works with mp3s?

## reference

- https://github.com/RodEsp/V.A.L.E.T. -- uses wifi/fixed device MAC addresses to detect people in the space and auto sign them in
- [launch message re VALET](https://recurse.zulipchat.com/#narrow/stream/398504-397-Bridge/topic/V.2EA.2EL.2EE.2ET.2E/near/388175215)
- [info on the visits bot](https://recurse.zulipchat.com/#narrow/stream/398504-397-Bridge/topic/visits-bot!)
- [hub visits API](https://github.com/recursecenter/wiki/wiki/Recurse-Center-API#hub-visits) -- we'll use this to create a visit and to let people sign in using oauth so that we can associate their tag with them

## misc

- there's no way to check out - except by deleting your visit, as noted by Nick [here](https://recurse.zulipchat.com/#narrow/stream/398504-397-Bridge/topic/visits-bot!/near/384055535) -- we'll probably leave it as is i.e. this (just like V.A.L.E.T. and the ipad) will also be a check-in-only system
- [what _is_ rfid/nfc/etc.?](https://blog.flipper.net/rfid/)

## contributors

This project is brought to you by [Kevan](https://github.com/khollbach), [Itay](https://github.com/itay-sho) and [Greg](https://github.com/gregsadetsky).
