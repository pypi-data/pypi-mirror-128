from .pkg_data.mitmproxy.tools import _main as cli
from .pkg_data.mitmproxy.events import HttpEvents


class Dropper(HttpEvents):
    pass


class mitmproxy:
    def __init__(self):
        cli.mitmproxy()


class mitmdump:
    def __init__(self):
        cli.mitmdump()


class mitmweb:
    def __init__(self):
        cli.mitmweb()


