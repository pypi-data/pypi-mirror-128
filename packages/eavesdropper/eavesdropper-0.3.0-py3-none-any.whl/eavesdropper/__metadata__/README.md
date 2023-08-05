# Eavesdropper

<badges>[![version](https://img.shields.io/pypi/v/eavesdropper.svg)](https://pypi.org/project/eavesdropper/)
[![license](https://img.shields.io/pypi/l/eavesdropper.svg)](https://pypi.org/project/eavesdropper/)
[![pyversions](https://img.shields.io/pypi/pyversions/eavesdropper.svg)](https://pypi.org/project/eavesdropper/)  
[![powered](https://img.shields.io/badge/Say-Thanks-ddddff.svg)](https://saythanks.io/to/foxe6)
[![donate](https://img.shields.io/badge/Donate-Paypal-0070ba.svg)](https://paypal.me/foxe6)
[![made](https://img.shields.io/badge/Made%20with-PyCharm-red.svg)](https://paypal.me/foxe6)
</badges>

<i>Eavesdropper, an application-level gateway firewall proxy, gives you control over all network traffic. Or simply use its integrated mitmproxy 5.3.0 which can be completely controlled with Python code.</i>

# Hierarchy

```
eavesdropper
|---- EAVESDROPPER()
|   |---- Dropper
|   |   |---- http_connect()
|   |   |---- requestheaders()
|   |   |---- request()
|   |   |---- responseheaders()
|   |   |---- response()
|   |   |---- error()
|   |   |---- clientconnect()
|   |   |---- clientdisconnect()
|   |   |---- serverconnect()
|   |   |---- serverdisconnect()
|   |   |---- next_layer()
|   |   |---- configure()
|   |   |---- done()
|   |   |---- load()
|   |   |---- log()
|   |   |---- running()
|   |   '---- update()
|   |---- configure()
|   |---- start()
|   '---- stop()
'---- pkg_data
    '---- mitmproxy # see https://docs.mitmproxy.org/archive/v5/
```

# Example

## python
See `test`.