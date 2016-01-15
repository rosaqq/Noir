# Noir
### Python bot for discord

### Absolutly pre-alpha don't even try

# Requirements/Dependencies:  
**Python 3.4+**  
**ChatterBot by gunthercox**  
https://github.com/gunthercox/ChatterBot  
**Discord.py by Rapptz**  
https://github.com/Rapptz/discord.py  
**lxml**  
http://lxml.de/installation.html  

bot commands (type them in discord chat while bot is running):

#### special commands (Noir will always respond):  
'noir come'-----to bring noir to the current channel (Noir will answer to normal commands)>admin or mod rank  
'noir leave'----to get him out of the current channel (Noir won't answer to normal commands)>admin or mod rank  
'noir kill'-----stops Noir (ends the program)>admin rank only

#### normal commands (Noir will only answer if he's in the channel where they were sent):  
**admin only commands:**  
'noir add mod @someone'--adds @someone as a bot mod.  
'noir del mod @someone'--removes @someone as a bot mod.  
**mod and admin commands:** 
'noir status something'--Changes "Playing" status to 'Playing something'  
'noir status none'-------reverts 'Playing' status to none  
**regular user commands:**  
'!ping'----------------try and guess it  
'noir help'------------pretty self-explanatory  
'noir gimme game'------return the game user is currently playing  
'noir gimme id'--------returns the user's id  
'noir pepe'------------returns a random pepe to user  
'noir pepe @someone'---@someone a random pepe  
'noir haiku'-----------returns a haiku to user  
'noir haiku @someone'--@someone a haiku  
'noir rank'------------shows your level of permission to run the commands  
'noir rek'-------------insults you, based on http://www.insultgenerator.org/  
'noir rek @some1'------same as previous one but instults @some1  
'noir praise'----------compliments you, based http://www.madsci.org/cgi-bin/cgiwrap/~lynn/jardin/SCG  
'noir praise @some1'---same as previous one but instults @some1  

#### how to use chatbot:
'@Noir + message' and he will answer.  
He will learn when you talk with him, and the more you chat, the better he gets at speaking.  
Refer to the linked ChatterBot page to learn how it works.

## IMPORTANT NOTES 
**How to install & run:**  
Download from git or whatever, just put all that is here on github on a folder in your computer and run 'Noir.py' (pyhton 3.4+ needs to be installed)  
At the end of the program you have to put your discord user, pass as args to client.run('user', 'pass') for it to be able to connect to discord servers.  
It is common for people to create a second discord account for the bot.