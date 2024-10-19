#!/usr/bin/env python

# Author: Isaac Verbrugge - isaacverbrugge@gmail.com
# Since: July 9, 2024
# Project: FOD Dog
# Purpose: bridge for ot -> waypointing

import socket
import threading
import json
import os
import sys
import time


class PlaneReceiver:

    def __init__(self, server_ip, port, servoController):
        self.server_ip = server_ip
        self.port = port
        self.socket = None

        self.listen_thread = None
        self.rate = 2

        self.servoController = servoController

        self.latitude = 0
        self.longitude = 0

        self.connect()

    def start_threads(self):
        self.listen_thread = threading.Thread(target=self.listen).start()

    def connect(self):
        try:

            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.settimeout(5)
            self.socket.connect((self.server_ip, self.port))
            self.socket.settimeout(None)
            print("[PlaneReceiver] Connected To Ground Control!")
        except (ConnectionRefusedError, OSError) as e:
            print("[PlaneReceiver] Not Connected")
            return False
        return True

    def send_gps(self):
        while True:
            try:
                # time.sleep(2)
                ifconfig_result = str(os.popen("ifconfig").read())
                self.connection_type = "NO CONNECTION"
                if (self.is_connected_to_wifi()):
                    self.connection_type = "Wifi"

                if (self.connection_type == "Wifi"):
                    gps_packet = "{\"gps\": {\"lat\": " + str(self.latitude) + ",\"lon\": " + str(self.longitude) + "}}"
                    self.socket.sendall(gps_packet.encode("utf-8"))

                # connection_packet = "{\"connection\": \"" + str(self.connection_type) + "\"}"
                # self.socket.sendall(connection_packet.encode("utf-8"))
            except:
                pass

    def listen(self):
        while True:
            try:
                data = self.socket.recv(1024)
                if (data != ""):

                    if data == "{\"HEARTBEAT\": 1}":
                        continue

                    print("[PlaneReceiver] Received: {}".format(data))

                    packet = json.loads(data)

                    if (packet.get("motion")):
                        # self.servoController.change_pitch(packet["motion"]["delta_pitch"])
                        # self.servoController.change_yaw(packet["motion"]["delta_yaw"])
                        # self.servoController.change_roll(packet["motion"]["delta_roll"])
                        ...
                    if (packet.get("test")):
                        print("test packet received")

                else:
                    self.connect()
            except Exception as e:
                # print(e)
                self.connect()
                pass

    def is_connected_to_wifi(self, check_rate=5):
        try:
            socket.create_connection(("8.8.8.8", 53), timeout=check_rate)
            return True
        except OSError:
            pass
        except Exception:
            return False
        return False


if __name__ == "__main__":
    server_ip = input("Server's ip: ")
    OpenThreadClient(server_ip=server_ip, port=5559)
