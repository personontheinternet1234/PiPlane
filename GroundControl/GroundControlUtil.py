import json


class ServerClient:

    def __init__(self, sock_obj, address):
        self.address = address


class Waypoint:

    def __init__(self, lat, lon):
        self.lat = lat
        self.lon = lon