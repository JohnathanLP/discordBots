from subprocess import call

command = "youtube-dl https://www.youtube.com/watch?v=wI7f4CgATiE -x --audio-format wav --id"
call(command.split(), shell=False)
