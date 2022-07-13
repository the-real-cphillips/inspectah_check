#!/usr/bin/env python

# Ascii Art From: https://textart.io/art/eOu6_na69sZhXxRlmwdytgeF/starwars-arakyd-viper-probe-droid

import sys
import time

from argparse import ArgumentParser, RawTextHelpFormatter
from tabulate import tabulate

from scann import *


def parse_args():
    """Parse argparse Arguments"""
    parser = ArgumentParser(
        description="\nWu-tang is Forever... Open ports (possibly) shouldn't be\n \
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⣤⣶⡀⠀⠀⠀\n \
⠀⢀⣶⣶⣤⣤⣀⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⣤⣶⣿⣿⣿⣿⣿⡄⠀⠀\n \
⠀⣼⣿⣿⣿⣿⣿⣿⣿⣷⣶⡤⠀⠀⠀⠀⢤⣶⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡄⠀\n \
⢰⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠀⠀⠀⢀⣀⠀⠙⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⠀\n \
⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⠀⠰⣾⣿⣿⣷⠀⣼⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇\n \
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣄⣿⣿⣿⣿⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿\n \
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿\n \
⢹⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿\n \
⠈⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠛⠛⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠇\n \
⠀⠈⢻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡁⠀⠀⠀⢻⣿⣿⣿⣿⣿⣿⣿⣿⣿⠏⠀\n \
⠀⠀⠀⠙⠿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣇⠀⠀⠀⣼⣿⣿⣿⣿⣿⣿⣿⡿⠃⠀⠀\n \
⠀⠀⠀⠀⠀⠈⠙⠻⠿⣿⣿⣿⣿⣿⣿⡄⠀⠀⣿⣿⣿⣿⣿⣿⠿⠋⠀⠀⠀⠀\n \
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠉⠉⠉⠉⠀⣸⣿⣿⣿⠿⠛⠁⠀⠀⠀⠀⠀⠀\n \
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠠⠟⠋⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀\n",
        formatter_class=RawTextHelpFormatter,
    )

    parser.add_argument(
        "-t",
        "--ip",
        action="store",
        dest="targets",
        nargs="+",
        required="true",
        help="IP Address to Scan",
    )
    parser.add_argument(
        "-s",
        "--start_port",
        action="store",
        dest="start_port",
        default=1,
        help="Start of Port Range to Scan"
    )
    parser.add_argument(
        "-e",
        "--end_port",
        action="store",
        dest="end_port",
        default=65536,
        help="End of Port Range to Scan. Note: Don't Forget to Add 1 if the last port you want is 8080, make sure you set this to 8081"
    )
    return parser.parse_args()


def has_all_attributes(host_scan_object, response):
    """
    Determine if response has all necessary attributes and return a dict
    """
    server_type_bool = False
    server_header = False
    server_type = None
    directory_list = False

    all_attributes = {
        "server_type_bool": server_type_bool,
        "server_type": server_type,
        "server_header": server_header,
        "directory_list": directory_list
    }

    hso = host_scan_object

    headers = hso.headers(response)

    if headers:
        server_header = hso.server_header(response)

    if server_header:
        all_attributes["server_header"] = server_header
        server_type = hso.server_type(response)

    if server_type:
        all_attributes["server_type"] = response.headers['Server']
        all_attributes["server_type_bool"] = server_type
        directory_list = hso.can_list_directory(response)

    if directory_list:
        all_attributes["directory_list"] = directory_list

    return all_attributes


def main():
    """main, where the magic happens"""
    total_toc = time.perf_counter()
    args = parse_args()
    all_attributes = {}

    for target_ip in args.targets:
        toc = time.perf_counter()
        table = []
        print(f'\n[I] Starting Scan {target_ip}')

        try:
            target = HostScan(
                    HostIp=target_ip,
                    StartPort=int(args.start_port),
                    EndPort=int(args.end_port)
                    )
        except InvalidIPFormat as err:
            print(f"[X] Input: {err.address} Error: {err.message}")
            sys.exit(2)

        open_ports = target.open_ports()

        for port in open_ports:
            response = target.request(port)

            if response:
                all_attributes = has_all_attributes(target, response)
                has_server_header = all_attributes["server_header"]
                has_server_type = all_attributes["server_type_bool"]
                server_type = all_attributes["server_type"]
                can_list_dir = all_attributes["directory_list"]

                table.append(
                    [port, has_server_header, has_server_type, server_type, can_list_dir] 
                )

        table_columns = [
            "Port",
            "Has Server Header",
            "Has Server Type",
            "Server Type",
            "Can List Dir",
        ]
        print(tabulate(table, headers=table_columns, tablefmt="grid"))
        tic = time.perf_counter()
        print(f'Scan Time: {tic - toc:.2f} seconds')

    total_tic = time.perf_counter()
    print(f'\n**** Total Run Time: {total_tic - total_toc:.2f} seconds ****')

if __name__ == "__main__":
    main()
