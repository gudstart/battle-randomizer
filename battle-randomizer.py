import time
import os
import discord
from dotenv import load_dotenv

from ruleGen import getBattleRules, TIME_LIMIT_MINUTES

battleInProgress = False

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
GUILD = os.getenv("DISCORD_GUILD")
MAIN_CH = int(os.getenv("MAIN_CHANNEL"))
BATTLE_CH = int(os.getenv("BATTLE_CHANNEL"))
client = discord.Client(intents=discord.Intents.all())

@client.event
async def on_ready():
    for guild in client.guilds:
        if guild.name == GUILD:
            break
    print(f"{client.user} has connected to the server:"f"{guild.name}(id: {guild.id})")

@client.event
async def on_message(message):
    global battleInProgress
    if message.author == client.user:
        return

    if message.content == "!battle":
        if (battleInProgress):
            channel = client.get_channel(MAIN_CH)
            await channel.send("Battle already in progress!")
        else:
            channel = client.get_channel(BATTLE_CH)
            battleInProgress = True  
            await channel.send(getBattleRules())
            t = TIME_LIMIT_MINUTES*60
            mins, secs = divmod(t, 60) 
            timer = "**Teambuilding: {:02d}:{:02d}**".format(mins, secs)
            timerMessage = await channel.send(timer)
            while t: 
                if (not battleInProgress): break
                time.sleep(1)
                t -= 1
                mins, secs = divmod(t, 60) 
                timer = "**Teambuilding: {:02d}:{:02d}**".format(mins, secs)
                await timerMessage.edit(content=timer)
            await timerMessage.delete()
            battleInProgress = False

    elif message.content == "!draft":
        if (battleInProgress):
            channel = client.get_channel(MAIN_CH)
            await channel.send("Battle already in progress!")
            # await channel.send(getDraftMons())

        else:
            channel = client.get_channel(BATTLE_CH)
            battleInProgress = True
    elif message.content == "!stop":
        channel = client.get_channel(MAIN_CH)
        await channel.send("Battle stopped.")
        battleInProgress = False
    elif message.content == "!purge":
        channel = client.get_channel(BATTLE_CH)
        async for mes in channel.history():
            await mes.delete()
        channel = client.get_channel(MAIN_CH)
        await channel.send("All past battle text removed.")
client.run(TOKEN)
