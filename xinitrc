#!/bin/sh

# link to this file from ~/.xinitrc

# invoke global X session script
. /etc/X11/Xsession

# xset s noblank
# xset s off
# xset s -dpms

exec openbox-session
