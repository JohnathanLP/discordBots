#!/bin/bash

case "$(pidof python3 | wc -w)" in
0)
     echo "Restarting bot: $(date)" >> ~/discordBots/eyspbot/log.txt
     tmux send -t 0.0 sudo\ python3\ /home/pi/discordBots/eyspbot/bot.py ENTER
     ;;
1)
     #echo "Bot is already running: $(date)" >> ~/discordBots/eyspbot/log.txt
     ;;
*)
esac
     
