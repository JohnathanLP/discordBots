from subprocess import call

command = "youtube-dl https://www.youtube.com/watch?v=yOMj7WttkOA -x --audio-format wav --id"
call(command.split(), shell=False)
