---
layout: post
title: Simple web server with cgi-bin support using Python (no-code)
description: A no-code Python solution for a simple cgi-capable server.
categories: Web
tags: Python
author: Sl-Alex
image: 2021-08-11-simple_python_cgi_server_nocode/preview.png
--- 

During the FW development for my [WlanClock][1] project I decided to replace the default
web interface (which is in [onion-os package][2]) with my own. onion-os is run by [uhttpd][3],
an OpenWRT-specific http server. Unfortunately, uhttpd is not available in Ubuntu,
which means I could not run my web interface locally.

There is one [snap package][4], but it does not support cgi-bin folder for backend scripts,
which is actively used by onion-os and which I was also hoping to use.

There is also a PPA package with [uhttpd port][5] for Ubuntu, but the support was limited to
Ubuntu 18.04. In addition, I prefer to use PPA only if there is absolutely no other way
to solve the problem. Fortunately, I found a better way to solve the problem and run
everything on my laptop.

{% include image.html url="/assets/2021-08-11-simple_python_cgi_server_nocode/preview.png" %}



I bet you have Python installed. Does not matter which version, it will work with any.
Just go to your web server root folder and run the following for python2:

```bash
python2 -m CGIHTTPServer
```

or for python3:

```bash
python3 -m http.server --cgi
```

It will serve all files from the root of the server as-is, files from cgi-bin folder
will be processed as scripts.

Here is how a simple cgi-bin script might look like:

```bash
#!/bin/sh
echo "content-type: text/html; charset=UTF-8"
echo ""
echo "<html><head><title>Test page</title></head><body><h1>It works</h1><p>Sample output</p></body></html>"
```

[1]: https://github.com/Sl-Alex/WlanClock
[2]: https://github.com/OnionIoT/OpenWRT-Packages/tree/openwrt-18.06/onion-os
[3]: https://openwrt.org/docs/guide-user/services/webserver/http.uhttpd
[4]: https://snapcraft.io/uhttpd
[5]: https://launchpad.net/~stokito/+archive/ubuntu/openwrt
