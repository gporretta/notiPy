# notiPy
python3 based command-line notification and reminder tool using notify-send.

Developed and tested on a GNOME desktop environment, compatability with
other desktop environments may vary.

notipy --list to see all active reminders

notipy --add 'Message' 'YYYY-MM-DD HH:MM:SS'

adding an additional --type flag with either single, daily, or weekly
if no type is given notipy defaults to single.

notipy --add 'test' '2024-11-05 17:00:00'
