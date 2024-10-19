import socket
import threading
import time
import json
from GroundControlUtil import ServerClient


class ThreadedServer(object):

    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.bind((self.host, self.port))
        self.client_ips = []

        print("Server ip: " + self.host)
        threading.Thread(target=self.listen).start()
        threading.Thread(target=self.client_check).start()

        self.pending_disconnect_clients = []

    def client_check(self):
        while True:
            print(self.client_ips)
            time.sleep(10)
            for client_ip in self.pending_disconnect_clients:
                self.close_client(client_ip)

            self.pending_disconnect_clients = []
            for client_ip in self.client_ips:
                self.server_socket.sendto(("{\"client_check\": \"challenge\"}").encode("UTF-8"), (client_ip, self.port))
                self.pending_disconnect_clients.append(client_ip)

    def listen(self):
        while True:
            data, address = self.server_socket.recvfrom(4096)
            client_ip = address[0]
            try:
                print(client_ip + " sent " + str(data))
                if data:
                    try:
                        received_packet = json.loads(data)
                        if received_packet.get("connected"):
                            # if the client is already registered, then  don't re-register
                            flag = False
                            for i in self.client_ips:
                                if self.client_ips == received_packet["connected"]:
                                    flag = True
                            if not flag:
                                self.client_ips.append(received_packet["connected"])
                        if received_packet.get("gps"):
                            print(str(address[0]) + ": " + str(received_packet["gps"]["lat"]) + " " + str(received_packet["gps"]["lon"]))
                        if received_packet.get("client_check"):
                            self.pending_disconnect_clients = self.remove_first_occurrence(self.pending_disconnect_clients, address[0])
                        if received_packet.get("server_check"):
                            self.server_socket.sendto("{\"server_check\": \"received\"}".encode("UTF-8"), (client_ip, self.port))

                    except Exception as e:
                        print("Json error?" + str(e))
            except Exception as e:
                print(e)
                break

    def close_client(self, address):
        print(f"Client Disconnected (client_check): {address}")
        try:
            self.client_ips = self.remove_first_occurrence(self.client_ips, address)
        except Exception as e:
            print(e)
            pass

    def send_packet_to(self, chosen_client_address, packet):
        try:
            self.server_socket.sendto(packet.encode(), (chosen_client_address, self.port))
        except Exception as e:
            print(e)
            print("Chosen Client does not exist")

    def remove_first_occurrence(self, my_list, string_to_remove):
        try:
            my_list.remove(string_to_remove)
        except ValueError:
            print(f"'{string_to_remove}' not found in the list.")
        return my_list





