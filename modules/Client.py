import socket, json

class Client():
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port

        self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connection.connect((self.ip, self.port))
      
              
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

    





    

