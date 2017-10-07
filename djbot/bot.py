import discord
import os.path

client = discord.Client()

@client.event
async def on_message(message):
    # we do not want the bot to reply to itself
    if message.author == client.user:
        return

    if message.content.startswith('!hello'):
        msg = 'Hello {0.author.mention}'.format(message)
        #msg = '/play witchdoctor sings a song'.format(message)
        await client.send_message(message.channel, msg)

    if message.content.startswith('!testmusic'):
        msg = '!summon'.format(message)
        await client.send_message(message.channel, msg)

    if message.content.startswith('!wd'):
        msg = '!play witchdoctor sings a song'.format(message)
        await client.send_message(message.channel, msg)

    if message.content.startswith('!summondj'):
        channel = client.get_channel('226052669830070273')
        await client.join_voice_channel(channel)

    if message.content.startswith('!djplaylist') or message.content.startswith('!djpl'):
        filename = message.content
        #print(filename)
        filename = filename.split(' ',1)[1]
        #print(filename) 
        if not os.path.exists(filename + ".txt" ):
             await client.send_message(message.channel, 'File not found!')
        else:
             file = open(filename + ".txt","r")
             for line in file:
                  msg = '!play ' + line
                  await client.send_message(message.channel, msg) 

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

client.run('MzI3NjEzMzIxNjI2Nzc5NjQ4.DC39vA.QIsKaA78TN7yI9NTp0AAIPll-Wg')
