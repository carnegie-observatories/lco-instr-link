import socket


class LcoInstrLink:
    def __init__(self, ip="localhost", port=52801):
        self.ip = ip
        self.port = port
        self._socket = None
        self._connected = False

    def connect(self):
        if self._connected:
            return
        try:
            self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self._socket.connect((self.ip, self.port))
            self._connected = True
        except Exception as e:
            print(f"Error connecting to {self.ip}:{self.port} - {e}")
            self._connected = False

    def ping(self):
        if self._connected:
            try:
                self._socket.sendall(b"ping")
                response = self._socket.recv(1024)
                return "unknown" in response.decode()
            except Exception as e:
                print(f"Error pinging {self.ip}:{self.port} - {e}")
                self._connected = False
        return False

    def close(self):
        if self._connected:
            try:
                self._socket.close()
                self._connected = False
            except Exception as e:
                print(f"Error closing connection to {self.ip}:{self.port} - {e}")
                self._connected = False

    def get(self, command):
        if self._connected:
            try:
                self._socket.sendall(command.encode())
                response = self._socket.recv(1024)
                return response.decode()
            except Exception as e:
                print(f"Error sending command to {self.ip}:{self.port} - {e}")
                self._connected = False
        return None
