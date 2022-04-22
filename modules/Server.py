import socket, json

class Server():
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port

        self.listen(self.ip, self.port)
        self.connection, address = self.listener.accept()


    def listen(self, ip, port):
        self.listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.listener.bind((ip, port))
        self.listener.listen(0)


    def reliable_send(self, data):
        json_data = json.dumps(data)
        self.connection.send(json_data.encode())


    def reliable_recive(self):
        json_data = b""
        while True:
            try:
                json_data += self.connection.recv(1024)
                return json.loads(json_data)
            except ValueError:
                continue


            

def get_ip():
    hostname = socket.gethostname()
    return socket.gethostbyname(hostname)


    
