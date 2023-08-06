#!/usr/bin/env python
from dataclasses import dataclass
from os import sync
from pathlib import Path
from shutil import move, which
from subprocess import run
from typing import Any

import click
from dataclasses_json import dataclass_json
from paho.mqtt.client import Client, MQTTMessage


@dataclass_json
@dataclass
class DomainMessage:
    domain: str
    ip: str


dns_records_file = Path("/etc/pihole/custom.list")


def read_old_dns() -> list[DomainMessage]:
    records = list(
        filter(
            lambda line: line != "",
            dns_records_file.read_text(encoding="utf-8").split("\n"),
        )
    )

    return [
        DomainMessage(ip=line.split()[0], domain=line.split()[1]) for line in records
    ]


def write_new_dns(old_records: list[DomainMessage], new_record: DomainMessage):
    new_list_file = Path("/tmp/custom.list.new")
    new_records = [*old_records, new_record]
    with new_list_file.open(mode="w", encoding="utf-8") as file:
        for record in new_records:
            file.write(f"{record.ip} {record.domain}\n")

    move(new_list_file, dns_records_file)
    sync()
    print(f"Wrote new pihole dns config {str(dns_records_file)}")


def on_message(client: Client, userdata: Any, msg: MQTTMessage):
    message: DomainMessage = DomainMessage.from_json(msg.payload)
    old_records = read_old_dns()
    if message in old_records:
        return

    write_new_dns(old_records, message)

    pihole = which("pihole")
    if pihole:
        proc = run([pihole, "restartdns", "reload"], capture_output=True)
        if proc.returncode == 0:
            print("Updated dns")
        else:
            print(proc.stderr)


@click.command(
    help="Connect to [HOST] and listen for domains to put in the pihole dns list"
)
@click.argument("host")
@click.option("-p", "--port", default=1883, help="The MQTT port to connect to")
@click.option("-t", "--topic", default="domains", help="The MQTT topic to listen on")
def main(host: str, port: int, topic: str):
    client = Client(client_id="pihole")
    client.connect(host, port)
    client.subscribe(topic=topic)
    client.on_connect = lambda c, userdata, flags, rc: print(f"Connected with rc: {rc}")
    client.on_message = on_message

    client.loop_forever()


if __name__ == "__main__":
    if not dns_records_file.exists():
        print(f"Not running on a pihole, couldn't locate {str(dns_records_file)}")
        exit(1)
    main()
