# useful-stuff
Small useful scripts.

**spotify_mute.py:** Mutes desktop Spotify when an advertisement plays. Very rudimentary, however: if there's any other window with "Advertisement" in the name, Spotify'll be muted!

**ffmpeg_track_merger.py:** Produces video(s) with merged audio tracks, taking video(s) as input (each having multiple audio tracks, e.g. one for system sounds and another for mic, as is common for screen recorders), . Bitrate's mostly preserved

**tuitionterminal:** Regularly checks tuitionterminal.com for new jobs matching filters, and posts to Discord in _discord_send.py_ using webhooks. Might try making an async _discord_send.py_ to post to multiple channels at once.
_TT_api.py_ is the old version using requests, but it keeps getting blocked by Cloudflare after days of working perfectly...
