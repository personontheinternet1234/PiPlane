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
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.client_socket.bind(('', self.port))
        self.plane_ip = "192.168.1.7"

        self.server_response = False
        self.connected_to_server = False

        self.rate = 2

        self.servoController = servoController

        self.latitude = 0
        self.longitude = 0

        self.connect()

    def start_threads(self):
        threading.Thread(target=self.listen).start()
        threading.Thread(target=self.server_check).start()

    def server_check(self):
        while True:
            self.client_socket.sendto(("{\"server_check\": \"challenge\"}").encode("UTF-8"),
                                      (self.server_ip, self.port))
            self.server_response = False
            time.sleep(10)
            if self.server_response == False:
                print("[PlaneReceiver] No response from server - disconnected")
                self.connected_to_server = False
                self.connect()

    def connect(self):
        try:
            self.client_socket.sendto(("{\"connected\": \"" + self.plane_ip + "\"}").encode("UTF-8"),
                                      (self.server_ip, self.port))
            print("[PlaneReceiver] Binded To Socket")
        except (ConnectionRefusedError, OSError) as e:
            print("[PlaneReceiver] Not Connected")
            return False
        return True

    def listen(self):
        while True:
            try:
                data, _ = self.client_socket.recvfrom(4096)

                # if "check" not in str(data):
                print("[PlaneReceiver] received: " + str(data))

                packet = json.loads(data)

                if (packet.get("motion")):
                    self.servoController.apply_motion_packet(packet["motion"]["delta_pitch"],
                                                             packet["motion"]["delta_yaw"],
                                                             packet["motion"]["delta_roll"])
                if (packet.get("client_check")):
                    self.client_socket.sendto(("{\"client_check\": \"received\"}").encode("UTF-8"),
                                              (self.server_ip, self.port))
                if (packet.get("server_check")):
                    self.server_response = True
            except Exception as e:
                print(e)
                pass

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
                    self.client_socket.sendall(gps_packet.encode("utf-8"))
            except:
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
    server_ip = "192.168.1.14"
    planeReceiver = PlaneReceiver(server_ip, 5559, servoController)
    # planeReceiver.listen()

