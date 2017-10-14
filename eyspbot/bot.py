import discord
import os.path
import asyncio
from random import randint
import time
from subprocess import call

client = discord.Client()
voice = 0
cmdtoken = '%'

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
        msg = 'Hello {0.author.mention}'.format(message)
        await client.send_message(message.channel, msg)

    #help command
    elif message.content.startswith(cmdtoken + 'help'):
        #TODO Clean this mess up, maybe format it nice
        msg = 'Discord Bot by Eysp - WIP \n'
        msg = msg + 'Please report any bugs or feature requests directly to me!\nCommands are as follows:\n'
        msg = msg + (cmdtoken + 'chat [SOUNDNAME] - Plays a chatwheel sound\n')
        msg = msg + (cmdtoken + 'djplaylist [PLAYLISTNAME] - Loads a new playlist into the musicbot. Musicbot must be running\n')
        msg = msg + (cmdtoken + 'listsounds - Sends you a DM listing all available chat sounds\n')
        msg = msg + (cmdtoken + 'bye - Dismisses the bot from voice chat\n\n')
        msg = msg + 'Future planned features:\n'
        msg = msg + 'Command to list all availible playlists\n'
        msg = msg + 'Ability to create/edit playlists from Discord chat\n'
        msg = msg + 'Better message cleanup (especially for incorrectly typed commands)\n'
        msg = msg + 'Direct integration of musicbot\n'
        msg = msg + 'External (webpage) GUI to control chatwheel, etc. from a phone or second monitor\n'
        msg = msg + 'DOTA2 Timers and alerts'
        await client.send_message(message.author, msg)

    #loads music bot with a playlist - will be replaced when this bot becomes musical
    elif message.content.startswith(cmdtoken + 'djplaylist') or message.content.startswith('!djpl'):
        #gets entire command string, removes first word, leaving parameter
        filename = 'playlists/' + message.content.split(' ',1)[1]
        #checks if file exists
        if not os.path.exists(filename + ".txt" ):
             await client.send_message(message.channel, 'File not found!')
        #outputs playlist to chat
        else:
            file = open(filename + ".txt","r")
            for line in file:
                msg = '!play ' + line
                temp = await client.send_message(message.channel, msg)
                await client.delete_message(temp)

    #disconnects from voice
    elif message.content.startswith(cmdtoken + 'bye') or message.content.startswith(cmdtoken + 'goodbye'):
        global voice
        msg = 'Bye everyone!'
        reply = await client.send_message(message.channel, msg)
        #if client.is_voice_connected(message.server):
        await voice.disconnect()
        await client.delete_message(message)
        time.sleep(2)
        await client.delete_message(reply)

    #plays music from YouTube
    elif message.content.startswith(cmdtoken + 'play'):
        global voice
        if not client.is_voice_connected(message.server): 
            print ('Client is not currently voice connected, connecting...')
            channel = message.author.voice.voice_channel
            voice = await client.join_voice_channel(channel)
        else:
            print ('Client is voice connected, may not be correct channel...')
        #get whole command string, remove first word, leaving parameter
        url = message.content.split(' ',1)[1]
        #plays song - note that no queue has been implemented
        player = await voice.create_ytdl_player(url)
        player.start()


    #downloads and plays from YouTube
    elif message.content.startswith(cmdtoken + 'dlplay'):
        url = message.content.split(' ',1)[1]
        url_id = message.content.split ('=',1)[1]
        print(url)
        print(url_id)
        command = 'youtube-dl ' + url + ' -x --audio-format mp3 --id'
        call(command.split(), shell=False)
        command = 'mv ' + url_id + '.mp3 songcache'
        call(command.split(), shell=False)

    #list availible chatwheel sounds
    #TODO Clean this mess up, maybe format it nice
    elif message.content.startswith(cmdtoken + 'listsounds') or message.content.startswith(cmdtoken + 'cwlist'):
        #lists all files contained in chatwheelsounds directory
        await client.send_message(message.author, 'Normal chatwheel sounds:')
        filelist = [f for f in os.listdir('chatwheelsounds') if os.path.isfile(os.path.join('chatwheelsounds', f))]
        msg = ''
        for filename in filelist:
            msg = msg + (filename[:len(filename)-4]) + '\n'
            #print(msg)
        await client.send_message(message.author, msg)
        #lists random sound commands
        await client.send_message(message.author, 'Randomized chatwheel sounds:')
        folderlist = [f for f in os.listdir('chatwheelsounds') if not os.path.isfile(os.path.join('chatwheelsounds', f))]
        msg = ''
        for foldername in folderlist:
            msg = msg + (foldername) + '\n'
            #print(msg)
        await client.send_message(message.author, msg)
        await client.delete_message(message)

    #plays chatwheel sound    
    #elif message.content.startswith(cmdtoken + 'chat') or message.content.startswith(cmdtoken + 'cw'):
    elif message.content.startswith(cmdtoken):
        #test if bot and user are connected to voice
        user_connected = not (message.author.voice.voice_channel == None)
        bot_connected = client.is_voice_connected(message.server)
        #move or leave bot as needed
        if bot_connected and user_connected:
            print ('moving bot to user\'s channel')
            await voice.move_to(message.author.voice.voice_channel)
        if not bot_connected and user_connected:
            print ('connecting bot to user\'s channel')
            voice = await client.join_voice_channel(message.author.voice.voice_channel)
        if bot_connected and not user_connected:
            print ('leaving bot in place')
        if not bot_connected and not user_connected:
            print ('cancelling')
            await client.send_message(message.channel, 'You and/or the bot must be connected to a voice channel!')
            return 

        #gets whole command string, removes first word, leaving parameter
        sound = message.content[1:]
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
        if os.path.exists(filename + '.wav'): 
            player = voice.create_ffmpeg_player(filename + '.wav')
            player.start()
        elif os.path.exists(filename + '.mp3'):
            player = voice.create_ffmpeg_player(filename + '.mp3')
            player.start()
        else:
            await client.send_message(message.channel, 'File not found!')
        while not player.is_done():
            time.sleep(.01)
        await client.delete_message(message)
        

        #Leave this command ^ last for now

print('test')
client.run('MzY2MTIwODU5NzEyMjI1Mjgx.DLoQLw.gRHtMi5FMPBcP7nRrtMO3NLTv_4')

