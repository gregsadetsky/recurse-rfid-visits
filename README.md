# recurse-rfid-visits

**TODO**: rename this as this project is "really" happening now with a bunch of hardware!!!!! maybe "octodoor"???

---

plan as of Sep 23:

ordered from amazon and [chicago electronics distributor](https://chicagodist.com/) ((only place where I found a raspi 4 for sale -- thanks to [rpilocator](https://rpilocator.com/)!)):
- [Raspberry Pi 4 Model B 1GB](https://chicagodist.com/products/raspberry-pi-4-model-b-1gb)
- [raspi case](https://chicagodist.com/products/raspberry-pi-4-case-red-white)
- [raspi power supply](https://chicagodist.com/products/raspberry-pi-4-psu-us-white)
- [raspi sd card w/pre-installed OS ](https://chicagodist.com/products/raspberry-pi-official-noobs-microsd-card)
- RECEIVED! [octopus plush toy](https://www.amazon.com/gp/product/B07WC3YWBB/)
- RECEIVED! TESTED / WORKS! [usb-powered speakers with 3.5mm (1/8') jack](https://www.amazon.com/gp/product/B07D7TV5J3/)
- RECEIVED! TESTED / WORKS! [rfid usb reader](https://www.amazon.com/gp/product/B07TMNZPXK/) -- seemingly compatible with H10301 HID fobs i.e. RC door knobs!! (TBD)

NEXT STEPS:
- sanity checks:
  - does the raspi boot/work? does basic wifi access work?
  - does the rfid usb reader work? try with macos, then raspi
    - I read something in the amzn comments about the rfid usb reader losing its settings on power off -- so hopefully can use its default mode i.e. "unconfigured"
  - does raspi sound work via the audio jack? need any weird alsa config? what CLI command works to play audio? aplay? works with mp3s?

then:
- write minimal raspi script/service that continuously 1. reads rfid tags 2. pings some server (TBD / see below) 3. receives response as to what to do (acknowledge, play audio, etc.)

then:
- write/finish/polish setup/main server. basic features:
  1. oauth sign up flow (sort of micro prototyped with flask/oauth) -->> sign in, scan badge ... 3 times?, then setup whether you want no sound/specific sound/community random sound
  2. respond to octodoor door scans i.e. check if known rc person ID + have oauth token for them, log, play back configured sound, ping hub visit API

where to host server? dokku + digital ocean...? render-ish?

-----------
for extremely later/not now/not me i.e. someone else can contrib: one of the Octopus leg could be a mic and button? To record new prompt

---
---
---

## what is this

a prototype for a hardware/software solution to let recursers sign in using their door tags by [kevan](https://github.com/khollbach) and greg

## plan

- [X] greg will check at home if his flipper zero is able to read the HID rfid tag (most probably)
  - confirmed! it's a standard H10301 HID format tag
- [ ] if so, greg will bring his flipper zero to the space on sep 22
- [ ] kevan and greg will do a quick sanity check - can the flipper zero read both of their tags, is the ID value unique for each? (or are they all programmed with the same recurse ID -- doubtful)
- [X] will we need to create a flipper app...? to read the tag? I think the flipper has a command-line serial port kind of thing to interface with it i.e. https://forum.flipper.net/t/cli-command-line-interface-examples/1874 ..? i.e. can we activate the flipper rfid reader not via its GUI...? otherwise create an app that reads tags and outputs their value over usb (and/or as a keyboard...? or serial port?)
  - all good and simple! -> when connected over usb, you can open a serial port to the flipper, and then issue `rfid read` to read the card. after that, you can issue `vibro 1` and a tiny bit later `vibro 0` as a way of giving feedback re: reading the tag (there's no way to play the speaker from the CLI unfortunately - but [maybe one day](https://github.com/xMasterX/all-the-plugins/issues/18)?)
- [ ] assuming that we can read info from the flipper (WE CAN), we need a device - a raspi? - that receives the read tags and ... communicates with the recurse hubs visit api directly?
- [ ] we'll need an oauth web app to let recursers scan their tag and associate their tag with themselves i.e. scan + pick a person. from that point on, we can store recurser person ID - tag ID and sign them any time in the future when they 'scan in'
- [ ] the raspi should host/serve its web server locally -- something like tagsignin.local in /etc/hostname? and then you'd go locally (while at the space) to that URL to do the setup?

## future

- [ ] if this works well, the best would be to use 2 dedicated hardware rfid readers and use 2 raspis - just like the two sign in ipads - to make it easy to sign in on the 4th and 5th floors.

## inspo/more info/reference

- https://github.com/RodEsp/V.A.L.E.T. -- uses wifi/fixed device MAC addresses to detect people in the space and auto sign them in
- [launch message re VALET](https://recurse.zulipchat.com/#narrow/stream/398504-397-Bridge/topic/V.2EA.2EL.2EE.2ET.2E/near/388175215)
- [info on the visits bot](https://recurse.zulipchat.com/#narrow/stream/398504-397-Bridge/topic/visits-bot!)
- [hub visits API](https://github.com/recursecenter/wiki/wiki/Recurse-Center-API#hub-visits) -- we'll use this to create a visit and to let people sign in using oauth so that we can associate their tag with them

## misc

- there's no way to check out - except by deleting your visit, as noted by Nick [here](https://recurse.zulipchat.com/#narrow/stream/398504-397-Bridge/topic/visits-bot!/near/384055535) -- we'll probably leave it as is i.e. this (just like V.A.L.E.T. and the ipad) will also be a check-in-only system

## nfc vs rfid:

- [super reference from flipper](https://blog.flipper.net/rfid/)
- from gpt-4:

---

A HID proximity tag (often used for access control in buildings and other secure environments) typically uses RFID (Radio-Frequency Identification) technology. More specifically, HID proximity tags commonly operate at the 125 kHz low-frequency range, which is a type of RFID.

NFC (Near Field Communication) is a subset of RFID and operates at the 13.56 MHz high-frequency range. NFC is typically used for short-range communication such as contactless payment systems, mobile phone interactions, and data transfers.

So, to answer your question: A HID proximity tag is an RFID tag, not an NFC tag.

---
