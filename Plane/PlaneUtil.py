class ServerClient:

    def __init__(self, sock_obj, address):
        self.sock_obj = sock_obj
        self.address = address
        self.connection_type = None 