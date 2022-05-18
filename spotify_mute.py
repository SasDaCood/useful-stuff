from pywinauto import Desktop
from pycaw.pycaw import AudioUtilities, ISimpleAudioVolume
from time import sleep


def mute_spotify(mute):
	sessions = AudioUtilities.GetAllSessions()
	for session in sessions:
		if session.Process and session.Process.name() == "Spotify.exe":
			adify = session._ctl.QueryInterface(ISimpleAudioVolume)
			adify.SetMasterVolume(0 if mute else 1, None)
	return mute


DELAY = 0.2
ad = False
while 1:
	sleep(DELAY)
	if not ad and "Advertisement" in [w.window_text() for w in Desktop(backend="uia").windows()]:		# ONLY searches for window w/ matching title! rip if you have a window containing "Advertisement" in the title while listening
		ad = mute_spotify(True)
	elif ad and "Advertisement" not in [w.window_text() for w in Desktop(backend="uia").windows()]:
		ad = mute_spotify(False)