import socket


class LcoInstrLink:
    def __init__(self, ip: str = "localhost", port: int = 52801):
        self.ip = ip
        self.port = port
        self._socket = None
        self._connected = False

    def connect(self) -> bool:
        if self._connected:
            return True
        try:
            self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self._socket.connect((self.ip, self.port))
            self._connected = True
        except Exception as e:
            print(f"Error connecting to {self.ip}:{self.port} - {e}")
            self._connected = False
        return self._connected

    def ping(self) -> bool:
        if self._connected:
            try:
                self._socket.sendall(b"ping")
                response = self._socket.recv(1024)
                return "ping" in response.decode()
            except Exception as e:
                print(f"Error pinging {self.ip}:{self.port} - {e}")
                self._connected = False
        return False

    def close(self) -> bool:
        if self._connected:
            try:
                self._socket.close()
                self._connected = False
            except Exception as e:
                print(f"Error closing connection to {self.ip}:{self.port} - {e}")
                self._connected = False
        return not self._connected

    def get(self, command: str) -> str:
        if self._connected:
            try:
                self._socket.sendall(command.encode())
                response = self._socket.recv(1024)
                return response.decode()
            except Exception as e:
                print(f"Error sending command to {self.ip}:{self.port} - {e}")
                self._connected = False
        else:
            raise Exception("Not connected")
        
    def get_float(self, command: str) -> float:
        return float(self.get(command))
