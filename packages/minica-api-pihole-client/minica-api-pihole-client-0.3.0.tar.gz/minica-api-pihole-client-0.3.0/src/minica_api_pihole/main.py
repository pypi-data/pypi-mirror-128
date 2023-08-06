#!/usr/bin/env python
from dataclasses import dataclass
from os import getuid, sync
from pathlib import Path
from shutil import move, which
from subprocess import run
from typing import Any, List

import click
from dataclasses_json import dataclass_json
from paho.mqtt.client import Client, MQTTMessage


@dataclass_json
@dataclass
class DomainMessage:
    domain: str
    ip: str


dns_records_file = Path("/etc/pihole/custom.list")


def read_old_dns() -> List[DomainMessage]:
    records = list(
        filter(
            lambda line: line != "",
            dns_records_file.read_text(encoding="utf-8").split("\n"),
        )
    )

    return [
        DomainMessage(ip=line.split()[0], domain=line.split()[1]) for line in records
    ]


def write_new_dns(old_records: List[DomainMessage], new_record: DomainMessage):
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


@click.command(
    help="Install and enable a systemd unit for the minica sync program with the given host, port and topic"
)
@click.argument("host")
@click.option("-p", "--port", default=1883, help="The MQTT port to connect to")
@click.option("-t", "--topic", default="domains", help="The MQTT topic to listen on")
def install(host: str, port: int, topic: str):
    systemd_unit_file = Path("/etc/systemd/system/minicasync.service")
    if systemd_unit_file.exists():
        print(f"Systemd unit service already installed at {str(systemd_unit_file)}")
        exit(1)

    if getuid() != 0:
        print("Can't install unless you're root, rerun the program with sudo")
        exit(2)

    bin = which("minica-pihole-sync")
    if not bin:
        print("minica-pihole-sync not found in $PATH, you need to install this as root")
        print("\t$ pip install minica-api-pihole-client")
        exit(3)

    unit_contents = f"""
    [Unit]
    Description=Sync traefik minica domain events to pihole dns
    After=network-online.target
    Wants=network-online.target
    
    [Service]
    User=root
    ExecStart={bin} --port {port} --topic {topic} {host}
    Restart=always
    
    [Install]
    WantedBy=multi-user.target
    """
    lines = list(map(lambda l: l.strip(), filter(None, unit_contents.split("\n"))))
    print(f"Installing the following to {systemd_unit_file}")
    print("\n".join(lines))

    with systemd_unit_file.open("w") as fp:
        fp.write("\n".join(lines))
    sync()
    print(f"Installed service file at {str(systemd_unit_file)}")

    proc = run(
        ["systemctl", "enable", "--now", systemd_unit_file.name], capture_output=True
    )
    if proc.returncode > 0:
        print(proc.stderr)
        exit(proc.returncode)
    else:
        print("Enabled service")


@click.command(help="Uninstall the systemd unit for the minica sync listener")
def uninstall():
    if getuid() != 0:
        print("Can't uninstall unless you're root, rerun the program with sudo")
        exit(1)

    systemd_unit_file = Path("/etc/systemd/system/minicasync.service")
    if not systemd_unit_file.exists():
        print("Systemd unit file not installed")
        exit(2)

    print("Disabling systemd service")
    run(["systemctl", "disable", "--now", systemd_unit_file.name], capture_output=True)
    print("Removing systemd service unit file")
    systemd_unit_file.unlink()
    print("Done")


if __name__ == "__main__":
    if not dns_records_file.exists():
        print(f"Not running on a pihole, couldn't locate {str(dns_records_file)}")
        exit(1)
    main()
