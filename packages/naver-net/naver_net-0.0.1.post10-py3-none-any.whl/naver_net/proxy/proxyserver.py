import Pyro4


class ProxyServer():
    def __init__(self, *args):
        self.daemon = Pyro4.Daemon()
        self.cls = args.cls
        pass

    def main(self):
        ns = Pyro4.locateNS()
        uri = self.daemon.register(self.cls)
        ns.register("IBS", uri)
        self.daemon.requestLoop()
