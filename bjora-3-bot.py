import discord
import name_search

client = discord.Client()

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')
    
    if message.content.startswith('$bungieme'):
        # trim command from message
        msgList = message.content.split(' ', 1)
        msgList = msgList[1]
        #split on the id number
        msgList = msgList.split('#')

        print("searching for " + '#'.join(msgList))

        # error checking
        if len(msgList) < 1:
            await message.channel.send('bad input')
        elif len(msgList) == 1:
            searchName = msgList[0]
            await message.channel.send(name_search.internal_search( searchName ))
        elif len(msgList) == 2:
            searchName = msgList[0]
            searchId = int(msgList[1])
            await message.channel.send(name_search.internal_search( searchName, searchId ))
        else:
            await message.channel.send('bad input')
        

client.run('OTU4ODQ1MTYzNTI5MTkxNTE0.YkTQJQ.ZiKS2FSkQ9yQtzgFY2PrRqCmw2Q') #bot token
