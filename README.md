# Pokemon Showdown Battle Randomizer using Discord bot

## Commands

nd = national dex, no nd = s/v dex

**!sandBats [nd]** 
1v1 format with random teambuilding ruleset. Some rules allow for illegal sets; use Custom Game when challenging.

In opponent's Showdown chatbox:
`!challenge Custom Game @@@ !SLEEP CLAUSE`

**!snake [nd]**
A less unserious 1v1 snake draft format where each player gets at most 1 mon from OU, UU, RU and below.

**!mutations [nd]**
1v1 standard draft format where the lower the mon's tier, the higher the chance of mutating its level, IVs, moves and ability. Level, IV and ability mutations cannot be modified but missing moves can always be filled up to 4 slots.

**!stop** to stop the current battle. This stops any active teambuilding timer.

## How to run it yourself

**.env** file required in main directory to run. Contents of .env:
DISCORD_TOKEN (bot auth token, ask me for permission @GudStrat on discord)
DISCORD_SERVER (name of discord server)
MAIN_CHANNEL (channel used to input bot commands)
BATTLE_CHANNEL (channel used to output bot rules / gamemodes)