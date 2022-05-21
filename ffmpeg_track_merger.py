try:
	import sys
	import subprocess
	from os import remove,getcwd

	BITRATE = 300 											# audio bitrate; 300kbps is way more than enough
	TRACK_COUNT = 2

	def exec(cmd): subprocess.call(cmd)

	filenames = sys.argv[1:] if len(sys.argv) > 1 else input("Filenames (separate files with spaces): ").split()		# input mp4 files to split into tempo mp3 tracks
	for file in filenames:
		if len(sys.argv)>1:
			file = file.replace(getcwd()+"\\","")
		filec = f'"{file}"'
		
		for track in range(TRACK_COUNT):					# extracts then merges the individual audio tracks
			exec(f"ffmpeg -i {filec} -codec:a libmp3lame -b:a {str(BITRATE)}k -map 0:a:{track} {track}.mp3")

		input_files = " ".join([f"-i {x}.mp3" for x in range(TRACK_COUNT)])
		exec(f"ffmpeg {input_files} -codec:a libmp3lame -b:a {str(BITRATE)}k -filter_complex amix=inputs={TRACK_COUNT}:duration=longest merged.mp3")

		newfilec = f'"merged{file}"'
		exec(f"ffmpeg -i {filec} -i merged.mp3 -c:v copy -codec:a libmp3lame -b:a {str(BITRATE)}k -map 0:v:0 -map 1:a:0 {newfilec}")

		for track in range(TRACK_COUNT):
			remove(f"{str(track)}.mp3")
		remove("merged.mp3")

except Exception as e:
	input(e)
