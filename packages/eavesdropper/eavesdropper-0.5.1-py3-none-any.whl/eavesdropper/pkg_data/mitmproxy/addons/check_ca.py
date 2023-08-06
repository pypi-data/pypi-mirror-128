import eavesdropper.pkg_data.mitmproxy
from eavesdropper.pkg_data.mitmproxy import ctx


class CheckCA:
    def __init__(self):
        self.failed = False

    def configure(self, updated):
        has_ca = (
            eavesdropper.pkg_data.mitmproxy.ctx.master.server and
            eavesdropper.pkg_data.mitmproxy.ctx.master.server.config and
            eavesdropper.pkg_data.mitmproxy.ctx.master.server.config.certstore and
            eavesdropper.pkg_data.mitmproxy.ctx.master.server.config.certstore.default_ca
        )
        if has_ca:
            self.failed = eavesdropper.pkg_data.mitmproxy.ctx.master.server.config.certstore.default_ca.has_expired()
            if self.failed:
                ctx.log.warn(
                    "The mitmproxy certificate authority has expired!\n"
                    "Please delete all CA-related files in your ~/.mitmproxy folder.\n"
                    "The CA will be regenerated automatically after restarting mitmproxy.\n"
                    "Then make sure all your clients have the new CA installed.",
                )
