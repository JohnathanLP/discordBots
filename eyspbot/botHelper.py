import time
import os.path

async def replyAndDelete(client, message, reply):
   temp = await client.send_message(message.channel, reply)
   time.sleep(3)
   await client.delete_message(message)
   await client.delete_message(temp)

async def playSound(client, voice, filename):
    playing = False
    if os.path.exists(filename + '.wav'):
        player = voice.create_ffmpeg_player(filename + '.wav')
        playing = True
    elif os.path.exists(filename + '.mp3'):
        player = voice.create_ffmpeg_player(filename + '.mp3')
        playing = True
    if playing:
        player.start()
        print('sound playing')
        while not player.is_done():
            time.sleep(.01)
    else:
        print('invalid name')
    return playing

async def summonToVoice(client, message, voice):    
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
            return None
        return voice
