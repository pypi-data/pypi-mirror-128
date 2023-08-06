# Minica API pihole client
A program for listening to domain discoveries published by [minica-api](https://github.com/bjornsnoen/minica-api)
and injecting them into the custom DNS list used by pihole.

## Installation
`$ pip install minica-api-pihole-client`

You will probably want to install this package as root, as the DNS list at `/etc/pihole/custom.list` is owned
by root. Alternatively chown that file so this program is allowed to overwrite it as the running user.

## Usage
`$ minica-pihole-sync MQTT-HOST [-p mqttport] [-t domaintopic]`
