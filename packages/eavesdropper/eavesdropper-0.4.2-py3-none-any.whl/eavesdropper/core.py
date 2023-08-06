from .pkg_data.mitmproxy.net.http import Request, Response
from .pkg_data.mitmproxy.proxy.server import ProxyServer
from .pkg_data.mitmproxy.proxy.config import ProxyConfig
from .pkg_data.mitmproxy.tools.dump import DumpMaster
from .pkg_data.mitmproxy.options import Options
from .pkg_data.mitmproxy.http import HTTPFlow
from .utils import *
import asyncio


class EAVESDROPPER:
    Dropper = Dropper

    def __init__(self, *, listen_host: str = "127.0.0.1", listen_port: int = 8080, **kwargs):
        self.proxy = "{}:{}".format(listen_host, listen_port)
        options = Options(listen_host=listen_host, listen_port=listen_port)
        self.mitmproxy = DumpMaster(options)
        self.mitmproxy.options.update(**kwargs)
        self.mitmproxy.server = ProxyServer(ProxyConfig(options))

    def configure(self):
        self.mitmproxy.addons.add(self.Dropper())

    def pause(self):
        self.mitmproxy.addons.remove(self.Dropper())

    def resume(self):
        self.configure()

    def start(self):
        asyncio.set_event_loop(self.mitmproxy.channel.loop)
        self.mitmproxy.run()

    def __del__(self):
        self.stop()

    def stop(self):
        self.mitmproxy.shutdown()




