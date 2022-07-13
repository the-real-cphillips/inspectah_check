#!/usr/bin/env python

import socket
import requests

from requests.exceptions import ConnectionError, ReadTimeout


class InvalidIPFormat(Exception):
    """Raised when Invalid IP is Passed"""

    def __init__(self, address, message):
        self.address = address
        self.message = message
        super().__init__(self.message)

    def __dict__(self):
        response = {
            "Input": self.address,
            "message": self.message,
        }
        return response


class HostScan:
    """HostScan
    Contains all necessary functions to determine if a target matches our criteria

    Takes Note of:
    - Is port open?
    - If open, does it respond to HTTP?
    - If it does respond to HTTP, does it have:
        - Headers?
        - Server Header?
        - Serve Header Equal to specific values?
        - Can we list the Directory Listing?
    """

    def __init__(self, **kwargs):
        self.target = kwargs.get("HostIp")
        self.start_port = kwargs.get("StartPort", 1)
        self.end_port = kwargs.get("EndPort", 65536)

        try:
            socket.inet_aton(self.target)
        except OSError as err:
            raise InvalidIPFormat(self.target, err)

    def open_ports(self):
        """Determins if sockets are open or not"""

        port_list = []

        for port_num in range(self.start_port, self.end_port):
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
                sock.settimeout(1)
                result = sock.connect_ex((self.target, port_num))

                if result == 0 and not None:
                    port_list.append(port_num)
                sock.close()

        return port_list

    def request(self, port):
        """Creates a Response Object to use going forward"""
        try:
            response = requests.get(f"http://{self.target}:{port}", timeout=3)
            return response
        except (ConnectionError, ReadTimeout, KeyError):
            pass

    def headers(self, response):
        """Validates headers in the Response object"""
        if response.headers:
            return True

    def server_header(self, response):
        """Confirms Server Header"""
        if "Server" in response.headers:
            return True

    def server_type(self, response):
        """Matches the type of server (this is ugly and basic)"""
        server_header = response.headers["Server"]
        if "nginx/1.2." in server_header or "Microsoft/IIS-7." in server_header:
            return True

    def can_list_directory(self, response):
        """Determines if we can list the directory listing (also ugly)"""
        if "Index of" in response.text or self.target in response.text:
            return True
