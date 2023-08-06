from eavesdropper.pkg_data.mitmproxy.addons import anticache
from eavesdropper.pkg_data.mitmproxy.addons import anticomp
from eavesdropper.pkg_data.mitmproxy.addons import block
from eavesdropper.pkg_data.mitmproxy.addons import browser
from eavesdropper.pkg_data.mitmproxy.addons import check_ca
from eavesdropper.pkg_data.mitmproxy.addons import clientplayback
from eavesdropper.pkg_data.mitmproxy.addons import command_history
from eavesdropper.pkg_data.mitmproxy.addons import core
from eavesdropper.pkg_data.mitmproxy.addons import cut
from eavesdropper.pkg_data.mitmproxy.addons import disable_h2c
from eavesdropper.pkg_data.mitmproxy.addons import export
from eavesdropper.pkg_data.mitmproxy.addons import onboarding
from eavesdropper.pkg_data.mitmproxy.addons import proxyauth
from eavesdropper.pkg_data.mitmproxy.addons import script
from eavesdropper.pkg_data.mitmproxy.addons import serverplayback
from eavesdropper.pkg_data.mitmproxy.addons import mapremote
from eavesdropper.pkg_data.mitmproxy.addons import maplocal
from eavesdropper.pkg_data.mitmproxy.addons import modifybody
from eavesdropper.pkg_data.mitmproxy.addons import modifyheaders
from eavesdropper.pkg_data.mitmproxy.addons import stickyauth
from eavesdropper.pkg_data.mitmproxy.addons import stickycookie
from eavesdropper.pkg_data.mitmproxy.addons import streambodies
from eavesdropper.pkg_data.mitmproxy.addons import save
from eavesdropper.pkg_data.mitmproxy.addons import upstream_auth


def default_addons():
    return [
        core.Core(),
        browser.Browser(),
        block.Block(),
        anticache.AntiCache(),
        anticomp.AntiComp(),
        check_ca.CheckCA(),
        clientplayback.ClientPlayback(),
        command_history.CommandHistory(),
        cut.Cut(),
        disable_h2c.DisableH2C(),
        export.Export(),
        onboarding.Onboarding(),
        proxyauth.ProxyAuth(),
        script.ScriptLoader(),
        serverplayback.ServerPlayback(),
        mapremote.MapRemote(),
        maplocal.MapLocal(),
        modifybody.ModifyBody(),
        modifyheaders.ModifyHeaders(),
        stickyauth.StickyAuth(),
        stickycookie.StickyCookie(),
        streambodies.StreamBodies(),
        save.Save(),
        upstream_auth.UpstreamAuth(),
    ]
