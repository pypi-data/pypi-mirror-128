import Pyro4


class ProxyClient():
    def __init__(self, *args):
        self.BSM = Pyro4.Proxy(f'PYRONAME:{args.cls}')
