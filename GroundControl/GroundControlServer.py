import socket
import threading
import time
import json
from GroundControlUtil import ServerClient


class ThreadedServer(object):

    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.bind((self.host, self.port))
        self.clients = {}

        self._stop_event = threading.Event()

        print("Server ip: " + self.host)
        threading.Thread(target=self.listen).start()
        threading.Thread(target=self.heartbeat).start()

    def heartbeat(self):
        while not self._stop_event.is_set():
            time.sleep(10)
            disconnected_clients = []
            for address, client in list(self.clients.items()):
                try:
                    client.sock_obj.sendall(("{\"HEARTBEAT\": 1}").encode("UTF-8"))
                except Exception as e:
                    disconnected_clients.append(client)
            for client in disconnected_clients:
                self.close_client(client)

    def listen(self):
        self.server_socket.listen(0)
        while not self._stop_event.is_set():
            client_sock_obj, address = self.server_socket.accept()
            # client.settimeout(60)
            print("Client Connected: " + str(address[0]))

            client = ServerClient(client_sock_obj, address[0])

            self.clients[client.address] = client
            threading.Thread(target=self.listenToClient, args=(client, address)).start()

    def listenToClient(self, client, address):
        while not self._stop_event.is_set():
            try:
                data = client.sock_obj.recv(1024)
                # print(data)
                # if data == b'':
                #
                #     self.close_client(client)
                #     break

                if data:
                    try:
                        received_packet = json.loads(data)
                        if received_packet.get("gps"):
                            print(str(received_packet["gps"]["lat"]) + " " + str(received_packet["gps"]["lon"]))
                    except Exception as e:
                        print("Json error?" + str(e))
            except Exception as e:
                print(e)
                break

    def close_client(self, client):
        print(f"Client Disconnected (Heartbeat): {client.address}")
        try:
            del self.clients[client.address]
            client.sock_obj.close()
        except Exception as e:
            print(e)
            pass

    def send_packet_to(self, chosen_client_address, packet):
        try:
            self.clients[chosen_client_address].sock_obj.send(packet.encode())
        except KeyError:
            print("Chosen Client does not exist")

    def stop(self):
        self._stop_event.set()




