import socket

class HostName():
    def getLocalIp(self):
        return socket.gethostbyname(socket.gethostname())
    def getLocalHostName(self):
        return socket.gethostname()
    def getLocalHostNameByIp(self):
        return socket.gethostbyaddr(self.getLocalIp())
    def getPublicIp(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))  # google DNS 
        return s.getsockname()[0]