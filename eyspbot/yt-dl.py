from subprocess import call

command = "youtube-dl https://www.youtube.com/watch?v=wI7f4CgATiE -x --audio-format mp3 --id"
call(command.split(), shell=False)
