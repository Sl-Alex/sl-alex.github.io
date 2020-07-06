---
layout: post
title: Simple Deluge WebUI login
categories: Internet
tags: Deluge
author: Sl-Alex
---
If you use Deluge WebUI then from time to time you have to enter your password and select default connection in the connection manager. It could be a bit annoying, especially if you use your own local server (e.g. OpenMediaVault) and do not expose WebUI to the external world. Of course, you can use a workaround and avoid direct interaction with WebUI. For example, [Transdrone](https://play.google.com/store/apps/details?id=org.transdroid.lite) is a good Android interface, which can connect to Deluge using your WebUI password. Looks good, but it's much better just to remove these annoying windows. In this post you'll find a step-by-step instruction.




# Disclaimer
> This instruction was tested in OpenMediaVault 3 (Deluge version 1.13.10). Although I don't expect it, it could be that your particular Deluge version could not be patched using this instruction. Anyway, you have to understand what you do and at least hide your Deluge WebUI behind the firewall.

# 1. Stop Deluge daemon and WebUI
You have to stop both Deluge daemon and WebUI before applying some changes:
```bash
systemctl stop deluged
```
or just
```bash
killall deluged
```
Then kill Deluge WebUI:
```bash
killall deluge-web
```
# 2. Disable "Login" window
Now let's do a dirty work and disable "Login" window. Information is taken from [The Dukrat's Lair](https://dukrat.net/124/deluge-webui-1-3-6-autologin-disable-password)

Open ```/usr/lib/python2.7/dist-packages/deluge/ui/web/js/deluge-all.js``` in editor, find section ```deluge.LoginWindow``` and replace the ```onShow``` function (it is located near the end of the minified line) in the following way:
```javascript
onShow:function(){this.onLogin();}
```
Now open ```/usr/lib/python2.7/dist-packages/deluge/ui/web/auth.py``` and comment out the ```if``` statement and add ```return True```, like this:
```python
            #if s.hexdigest() == config["pwd_sha1"]:
            #    return True
            return True
```
# 3. Disable "Connection manager" window
If you plan to use WebUI only with a single Deluge instance (e.g. 127.0.0.1:58846) then you probably would like to disable connection manager window. If so, then select a proper connection in the connection manager and open ```auth``` file in the deluge configuration folder. By default it is located in "&lt;home_of_deluge_user&gt;/.config/deluge". You will see something like this:
```bash
localclient:3f9ca10d6dbda1c317ffda93d8bbae018523d0abef5:10
```
Copy the long string between two colons. Open "web.conf", which is also located in the deluge configuration folder and paste this string to the "default_daemon" field, so your configuration string will look like this:
```bash
"default_daemon"="3f9ca10d6dbda1c317ffda93d8bbae018523d0abef5"
```
Save configuration file and restart your server. Now you can log in without any annoying windows. Enjoy!