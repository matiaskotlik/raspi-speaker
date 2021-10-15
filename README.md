# Raspberry Pi Spotify Speaker with Audio Visualizer

Spotify speaker + audio visualizer, with background and color scheme that matches the currently playing album art, running on a raspberry pi.

https://user-images.githubusercontent.com/20362627/137560865-0e242ffb-dafa-426e-aff7-dd9eda66cec3.mp4

Uses raspotify, pywal, cava, conky, openbox, and tilda.

- raspotify is for spotify-related things and playing music
- Both cava and conky display stuff onscreen (the visualizer and song info respectively)
- pywal is responsible for for changing the color of both of those according to album art
- Openbox because it stays out of my way
- Tilda because it's easy to set it up to be transparent and run my visualizer (cava)

The code is *really* bad but it works Good Enough™.

# How do I use this?

These instructions and the code in the repository are mostly guidelines. Someday I might make a script that will do this all for you or a disk image with everything already set up.

Anyway, here's a rough outline of what you need to do to get everything running:

- Install raspotify, pywal, cava, conky, openbox, tilda, unclutter, compton, and X11 if you don't already have it.
- Clone the repository to the raspberry pi.
- The files cava, conky.conf, xinitrc, profile, and openbox-autostart all need to be linked to from different places on the filesystem, check each individual file for more info.
- You'll need to install `tendo` and `spotipy` from `pip`. You can use a venv or be lazy and install them globally like me.
- Alot of files have hardcoded paths to `~/matias-speaker`. You'll want to change those to wherever you cloned this repository to. Sorry!
- Sign up for a spotify api key, and put your `CLIENT_ID`, and `CLIENT_SECRET` in a `.env` file in the project root.
- You will need to set up Tilda manually. Just go into the options and make it fullscreen, transparent, no animations, and set it to run `cava` instead of your shell.
- You can configure speaker options like the name and icon in spotify + more by editing the file at /etc/default/raspotify.conf. Options are documented here: https://github.com/dtcooper/raspotify
- Make sure autologin is enabled, then reboot. When the pi starts back up, it should autologin, run the ~/.profile script which will start X11 and run the ~/.xinitrc script. This will start openbox, and then openbox will start everything else that needs to be running. After this you should be good to connect to the pi from your phone or computer and play some music on it.

