try:
    __import__('pkg_resources').declare_namespace(__name__)
except ImportError:
    __path__ = __import__('pkgutil').extend_path(__path__, __name__)

# from .bus.busclient import BusClient
# from .dns.dnsserver import DNSServer
# from .host.hostname import HostName
# from .proxy.proxyclient import ProxyClient
# from .proxy.proxyserver import ProxyServer
# from .vpn.client import VPNClient
# from .vpn.hub import VPNHub
from .mail import Sender
from naver_config import NaverConfig 
class NaverNet(NaverConfig):
    def __init__(self, myApp): 
        self.myConfig = NaverConfig(myApp) 
        # self.bus_client = BusClient(self.myConfig)
        # self.dns = DNSServer(self.myConfig)
        # self.host = HostName(self.myConfig)
        # self.proxy_client = ProxyClient(self.myConfig)
        # self.proxy_server = ProxyServer(self.myConfig)
        # self.vpn_client = VPNClient(self.myConfig)
        # self.vpn_hub = VPNHub(self.myConfig)
        self.sender = Sender(self.myConfig)