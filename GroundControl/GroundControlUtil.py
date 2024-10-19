import json


class ServerClient:

    def __init__(self, sock_obj, address):
        self.sock_obj = sock_obj
        self.address = address
        self.connection_type = None


class MotionPacket:

    def __init__(self, delta_pitch, delta_yaw, delta_roll):
        self.delta_pitch = delta_pitch
        self.delta_yaw = delta_yaw
        self.delta_roll = delta_roll
        self.data = ("{\"motion\": {\"delta_pitch\": " + str(self.delta_pitch) + ",\"delta_yaw\": " + str(self.delta_yaw) + ",\"delta_roll\": " + str(self.delta_roll) + "}}").encode("utf-8")


class TestPacket:

    def __init__(self):
        self.data = ("{\"test\": {\"e\": " + str(1) + "}}").encode("utf-8")


class Waypoint:

    def __init__(self, lat, lon):
        self.lat = lat
        self.lon = lon