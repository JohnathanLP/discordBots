import discord
import os.path
import asyncio
from random import randint

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
        await client.send_message(message.channel, 'Discord bot by Eysp - WIP')
        await client.send_message(message.channel, 'Please report any bugs or feature requests directly to me!')
        await client.send_message(message.channel, 'Commands are as follows:')
        await client.send_message(message.channel, (cmdtoken + 'chat [SOUNDNAME] - Plays a chatwheel sound.'))
        await client.send_message(message.channel, (cmdtoken + 'djplaylist [PLAYLISTNAME] - Loads a new playlist into the external musicbot. Musicbot must be running.'))
        await client.send_message(message.channel, (cmdtoken + 'bye - Dismisses the bot from voice chat'))
        await client.send_message(message.channel, 'Future planned/hoped for features:')
        await client.send_message(message.channel, 'Command to list all availible chatwheel sounds')
        await client.send_message(message.channel, 'Command to list all availible playlists')
        await client.send_message(message.channel, 'Ability to create/edit playlists from Discord chat')
        await client.send_message(message.channel, 'Better message cleanup')
        await client.send_message(message.channel, 'Direct integration of musicbot funcitonality')
        await client.send_message(message.channel, 'External webpage GUI (to control chatwheel, etc. from a phone or second monitor)')
        await client.send_message(message.channel, 'DOTA2 Timers and alerts')

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
        await client.send_message(message.channel, msg)
        if client.is_voice_connected(message.server):
            await voice.disconnect()

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

    #list availible chatwheel sounds

    #plays chatwheel sound    
    #elif message.content.startswith(cmdtoken + 'chat') or message.content.startswith(cmdtoken + 'cw'):
    elif message.content.startswith(cmdtoken):
        #test if connected to voice, connect if needed
        global voice
        if not client.is_voice_connected(message.server): 
            print ('Client is not currently voice connected, connecting...')
            channel = message.author.voice.voice_channel
            voice = await client.join_voice_channel(channel)
        else:
            print ('Client is voice connected, may not be correct channel...') 
        #gets whole command string, removes first word, leaving parameter
        sound = message.content[1:]
        #handles navi sounds
        if sound == 'navi':
            index = randint(0,28)
            filename = 'chatwheelsounds/navi' + index
            print (filename)
        else:
            filename = 'chatwheelsounds/' + sound
        print(filename)
        #checks if sound exists, tests for mp3 or wav, and plays sound
        if os.path.exists(filename + '.wav'): 
            player = voice.create_ffmpeg_player(filename + '.wav')
            player.start()
        elif os.path.exists(filename + '.mp3'):
            player = voice.create_ffmpeg_player(filename + '.wav')
            player.start()
        else:
            await client.send_message(message.channel, 'File not found!')
        await client.delete_message(message)

        #Leave this command ^ last for now

client.run('MzY2MTIwODU5NzEyMjI1Mjgx.DLoQLw.gRHtMi5FMPBcP7nRrtMO3NLTv_4')

