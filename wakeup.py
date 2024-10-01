#!/usr/bin/python3

import re
import socket
import yaml
import argparse

with open('config.yaml', 'r') as f:
    CONFIG = yaml.safe_load(f)


def sanitize_mac(macaddress: str) -> str:
    # remove everything which is not hexadecimal / make the script independent of given MAC-Address format since we
    # don't need a specific format anyway
    return re.sub(r"[^0-9A-Fa-f]", "", macaddress)


def create_magic_packet(macaddress: str) -> bytes:
    # From Wake On LAN Specificaiton:
    # 6x "FF" sync-bytes followed by 16x the mac address
    return bytes.fromhex('FF' * 6 + sanitize_mac(macaddress) * 16)


def send_magic_packet(macaddress: str) -> None:
    packet = create_magic_packet(macaddress)

    # create IPv4 UDP socket
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        # bind socket to interface specified in config.yaml
        # if interface=='', then the socket will be binded to each interface
        sock.bind((CONFIG["interface"], 0))

        # set socket in broadcast mode and send packet
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        sock.connect((CONFIG["broadcast_ip"], CONFIG["default_port"]))
        sock.send(packet)


def main() -> int:
    parser = argparse.ArgumentParser(prog='Wake-on-LAN Skript', description='Weckt Hosts auf')
    parser.add_argument('-l', '--list', required=False, action='store_true',
                        help='Listet alle Hosts in der config.yaml auf')
    group = parser.add_mutually_exclusive_group()
    group.add_argument('-n', '--name', type=str, help='Hostname (muss vorher in der config.yaml eingetragen werden!')
    group.add_argument('-m', '--mac', type=str, help='MAC-Adresse')
    args = parser.parse_args()

    if args.mac:
        send_magic_packet(args.mac)
        return 0

    if args.list:
        print(yaml.dump(CONFIG["hosts"], default_flow_style=False))
        return 0

    if args.name and args.name in CONFIG['hosts']:
        send_magic_packet(CONFIG["hosts"][args.name])
    elif args.mac:
        send_magic_packet(args.mac)
    return 0


if __name__ == '__main__':
    main()
