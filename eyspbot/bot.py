import discord
import os.path
import asyncio
from random import randint
import time
from subprocess import call
import musicPlayer
import utils
from collections import deque
from flask import Flask, render_template
import threading
import math
import botHelper

client = discord.Client()
cmdtoken = '%'
playing = False
songQueue = deque('')
voice = ''

@client.event
async def on_ready():
     print('Logged in as')
     print(client.user.name)
     print(client.user.id)
     print('-------')

@client.event
async def on_message(message):
    #prevents bot from responding to itself
    if message.author == client.user:
        return

    #generic greeing command
    elif message.content.startswith(cmdtoken + 'hello'):
        await botHelper.replyAndDelete(client, message, 'Hello, ' + message.author.mention)

    #help command
    elif message.content.startswith(cmdtoken + 'help') or message.content.startswith(cmdtoken + 'about'):
        #sends help message as DM from file helpFile.txt
        helpFile = open('helpFile.txt', 'r')
        msg =''
        for line in helpFile:
            msg = msg + line + '\n'
        await client.send_message(message.author, msg)
        await botHelper.replyAndDelete(client, message, 'Check your inbox for help/about message')

    #disconnects from voice
    elif message.content.startswith(cmdtoken + 'bye') or message.content.startswith(cmdtoken + 'goodbye'):
        global voice
        #if client.is_voice_connected(message.server):
        await voice.disconnect()
        await botHelper.replyAndDelete(client, message, 'Bye everyone!')
      
    #list availible chatwheel sounds
    elif message.content.startswith(cmdtoken + 'listsounds') or message.content.startswith(cmdtoken + 'cwlist'):
        #lists all files contained in chatwheelsounds directory
        msg = 'Normal chatwheelsounds:\n' 
        filelist = [f for f in os.listdir('chatwheelsounds') if os.path.isfile(os.path.join('chatwheelsounds', f))]
        for filename in filelist:
            msg = msg + (filename[:len(filename)-4]) + '\n'
        #lists random sound commands
        msg = msg + '\nRandomized chatwheel sounds:\n'
        folderlist = [f for f in os.listdir('chatwheelsounds') if not os.path.isfile(os.path.join('chatwheelsounds', f))]
        for foldername in folderlist:
            msg = msg + (foldername) + '\n'
        await client.send_message(message.author, msg)
        await botHelper.replyAndDelete(client, message, 'Check your inbox for list of chatwheel sounds')
    
    #plays chatwheel sound    
    elif message.content.startswith(cmdtoken + 'cw'):
        temp = await botHelper.summonToVoice(client, message, voice)
        if temp == None:
            await botHelper.replyAndDelete(client, message, 'You and/or the bot must be connected to voice!')
            return
        else:
            voice = temp
        if message.content == (cmdtoken + 'cw'):
            await botHelper.replyAndDelete (client,message,'Bot Summoned!')
            return
        sound = utils.getArgs(message)[0]
        #handles navi sounds
        #TODO modularize randomized sounds
        if sound == 'navi':
            index = randint(0,28)
            filename = 'chatwheelsounds/navi/' + str(index)
            print (filename)
        else:
            filename = 'chatwheelsounds/' + sound
        print(filename)
        #checks if sound exists, tests for mp3 or wav, and plays sound
        if await botHelper.playSound(client, voice, filename):
            await client.delete_message(message)
        else:
            await botHelper.replyAndDelete(client, message, 'File not found!') 

    #finds and deletes invalid commands
    elif message.content.startswith(cmdtoken):
        await botHelper.replyAndDelete(client, message, "Invalid Command")
        #Leave this command ^ last for now

#Flask server for web interface
app = Flask(__name__)
@app.route('/')
def index():
    generateHTML()
    return render_template('index.html')

def generateHTML():
    file = open("templates/index.html","w")
    filelist = [f for f in os.listdir('chatwheelsounds') if os.path.isfile(os.path.join('chatwheelsounds', f))]
    fileNum = len(filelist)
    rows = math.ceil(fileNum/2)
    header = """<html>\n<body>\n<head>\n<meta></meta charset = "UTF-8"><title>Chatwheel Controls</title>\n<link rel="shortcut icon" href="{{ url_for('static', filename='favicon.ico') }}">\n</head>\n<h1 style= "text-align: center; background: blue; color:white;">Chatwheel Controls</h1>\n<p style= "text-align: center; font-size: 20px; color: blue;">Note: This page is optimized for a portrait view, such as a smartphone. If this is not an option, for best results, zoom out so the entire page is visible at once.</p>\n<table style= "width: 100%; font-size: 45px">\n """
    footer = "</table>\n</body>\n</html>\n"
    file.write(header)
    filelist.sort()
    for i in range(0,fileNum-1):
        if(i%2==0):
            file.write("<tr>\n")
        temp = (filelist[i][:len(filelist[i])-4])
        file.write("<td width=\"50%\"> <div style= \"background: powderblue; border-radius: 25px; text-align: center;\"><a href=\"/" + temp + "/\">" + temp + "</a></div></td>\n")
        if(i%2==1):
            file.write("</tr>\n")
    file.write(footer)
    file.close()

def flaskSound(sound):
    bot_connected = False
    for server in client.servers:
        bot_connected |= client.is_voice_connected(server)
    #cancel if bot is not connected to voice
    if not bot_connected:
        print ('attempted flask sound with disconnected bot, cancelling')
        return
    #handles navi sounds
    #TODO modularize randomized sounds
    if sound == 'navi':
        index = randint(0,28)
        filename = 'chatwheelsounds/navi/' + str(index)
    else:
        filename = 'chatwheelsounds/' + sound
    #checks if sound exists, tests for mp3 or wav, and plays sound
    if os.path.exists(filename + '.wav'): 
        player = voice.create_ffmpeg_player(filename + '.wav')
        player.start()
        while not player.is_done():
            time.sleep(.01)
    elif os.path.exists(filename + '.mp3'):
        player = voice.create_ffmpeg_player(filename + '.mp3')
        player.start()
        while not player.is_done():
            time.sleep(.01)
    else:
        print('attempted flask sound with invalid filename')

@app.route('/<sound>/')
def frog(sound):
    #player = voice.create_ffmpeg_player('chatwheelsounds/frog.wav')
    #player.start()
    flaskSound(sound)
    return render_template('index.html')

def startFlask():
    if __name__ == '__main__':
        app.run(debug=False, use_reloader=False, host='0.0.0.0')

t = threading.Thread(target = startFlask)
t.start()

file = open('token.txt')
token = file.read().splitlines()[0]
print(token)
client.run(token)
file.close()
