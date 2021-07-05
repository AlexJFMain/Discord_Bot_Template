# Creator       : Alex Fedok
# Updated as of : 2021-07-05
# Purpose       : Built to create a quick template for other users to build discord bots.
# How to        : Fill in TODO forms where necessary, make sure you have a file ".env" in the same path to access secrets.

# Here is the .env file format. Put it in the same file path as this .py file, do not commit your .env file.
#------------------------------------------------------------------------------------------------
# API_TOKEN="your.token.here"
# DB_DRIVER="your.driver.here"
# DB_SERVER="your.server.here"
# DB_DATABASE="your.db.here"
# USER_ID="your.id.here"
# USER_SECRET="your.secret.here"
#------------------------------------------------------------------------------------------------

# Template necessary dependancies, also included in "requirements.txt".
#------------------------------------------------------------------------------------------------
import discord
import os
import datetime
import random
import pyodbc
from colorama import init, Fore, Back, Style
from dotenv import load_dotenv
from pytz import timezone
#------------------------------------------------------------------------------------------------

client = discord.Client()
load_dotenv()

#TODO--------------------------------------------------------------------------------------------
######################################VALUES-TO-FILL#############################################
#------------------------------------------------------------------------------------------------
# Give a custom name to your server, this will determine what the bot refers to your server as.
discordServerName = "My First Server" 
# Sets a default color for the discord server when it is needed, default is a light purple in hex.
discordPrimaryColor = 0xb781d6 
# Environmental Variables.
discordApiToken = os.getenv("API_TOKEN")
dbDriver = os.getenv("DB_DRIVER")  
dbServer = os.getenv("DB_SERVER")  
dbDatabase = os.getenv("DB_DATABASE")  
userId = os.getenv("USER_ID")  
userSecret = os.getenv("USER_SECRET")  
# Bot role access, if a user does not belong to one of these roles they will not have access to bot functions. Enter all role names which you would like to have access to bot functions. Use ["@everyone"] to give access to all.
discordPermittedRoles = ["vip", "admin"]
# Choose what timezone you would like to be localized in, default is in Eastern Standard Time.
discordTimeZone = timezone('US/Eastern')
#------------------------------------------------------------------------------------------------
#################################################################################################
#------------------------------------------------------------------------------------------------

# HELPER FUNCTIONS:
#------------------------------------------------------------------------------------------------
# Handles logging of events when needed.
def logMessageInfo(*inputs):
    stringToPrint = ""
    for inputData in inputs:
        stringToPrint += str(inputData)
    print("%s : EVENT - %s" % (datetime.datetime.now(discordTimeZone), stringToPrint))

# Checks if user's roles are in a permissions list.
def hasRole(userRoles, allowedRoles): 
    hasRole = False
    try:
        for roles in userRoles:
            if roles.name in allowedRoles:
                hasRole = True
                break
    except:
        hasRole = True
    return hasRole

# Return random choice from list.
def randomChoice(choiceList):
    return random.choice(choiceList)

# Creates an embed to print. Can have multiple dictionaries allocated to content parameter.
# "content" definition:
#   content = {
#       "title": "Result:",
#       "description": result
#   }
def createEmbed(description, username, icon, color, *content):
    embed_read = discord.Embed(description = "%s - %s" % (description, datetime.datetime.now(discordTimeZone).strftime("%Y-%m-%d %H:%M:%S")) , color = color)
    embed_read.set_author(name = username, icon_url = icon)
    for items in content:
        try:
            embed_read.add_field(name = items["title"], value = items["description"])
        except:
            logMessageInfo("BOT FAILURE    : createEmbed function could not add field")
    return embed_read

# Run queries against connection.
def queryDB (cursorConnection, needsToCommit, *queries):
    failureMode = 0
    try:
        for query in queries:
            try:
                cursorConnection.execute(query)
            except:
                failureMode += 1
        if(needsToCommit == True):
            try:    
                cursorConnection.commit()
            except:
                failureMode += 1
    except:
        failureMode += 1
    return failureMode

# Returns data in dictionary list, best used in conjunction with queryDB(...) when reading data.
def createQueryList(cursorconnection):
    results = []
    try:
        columns = [column[0] for column in cursorconnection.description]
        for row in cursorconnection.fetchall():
            results.append(dict(zip(columns, row)))
    except:
        pass
    return results

# Puts dictionary list into print(...) readable format.
def stringDictList(dictionaryList):
    stringList = []
    count = 0
    for line in dictionaryList:
        valueString = ""  
        keyString = "" 
        for key, value in line.items():
            if count == 0:
                keyString += "**" + str(key) + "** "
            valueString += str(value) + " "
        if count == 0:
            stringList.append(keyString)
        count += 1
        stringList.append(valueString)
    return stringList
#------------------------------------------------------------------------------------------------

# Database Connection.
#------------------------------------------------------------------------------------------------
databaseActive = False
init()
try:
    conn = pyodbc.connect("Driver={%s};SERVER=%s;DATABASE=%s;UID=%s;PWD=%s" % (dbDriver, dbServer, dbDatabase, userId, userSecret))
    cursor = conn.cursor()
    databaseActive = True
    logMessageInfo(f"DB CONNECTION  : Bot has \033[32mCONNECTED SUCCESSFULLY\033[39m to {dbDatabase}")
except:
    logMessageInfo(f"DB CONNECTION  : Bot has \033[31mFAILED TO CONNECT\033[39m to {dbDatabase}")   
#------------------------------------------------------------------------------------------------

# Logs connection time of bot to server.

@client.event
async def on_ready():
    logMessageInfo("BOT CONNECTION : Bot has \033[32mCONNECTED SUCCESSFULLY\033[39m to ", discordServerName)

# Performs actions on message in text channels.
@client.event
async def on_message(message):

    # Easy access dictionary for data from message.
    messageDict = {
        "channelID": message.channel.id,
        "channelName": message.channel.name,
        "messageID": message.author.id,
        "messageName": message.author.name,
        "messageNick": message.author.nick,
        "messageIcon": message.author.avatar_url,
        "messageRoles": message.author.roles,
        "messageContent": message.content,
        "hasAccess": hasRole(message.author.roles, discordPermittedRoles)
    }

    # ACCESS HANDLING:
    #------------------------------------------------------------------------------------------------
    # Will not reference self.
    if message.author == client.user:
        return

    # Logs entries in channel.
    logMessageInfo("MESSAGE INFO   : \"\033[36m", messageDict["messageContent"], "\033[39m\" said by ID= \033[33m", messageDict["messageID"], "\033[39m, NAME= \033[33m", messageDict["messageName"], "\033[39m, NICK= \033[33m", messageDict["messageNick"], "\033[39m")

    # Break off if not accessing a function.
    if not message.content.startswith('!'):
        return
    
    # Will not allow non permitted roles through.
    # Can also create a similar copy of this where "messageDict["hasAccess"] == True", if you want a list that looks for roles to exclude.
    if messageDict["hasAccess"] == False:
        return
    #------------------------------------------------------------------------------------------------
    
    # Picks how the user will be referenced if they do not have nickname will default to their username.
    referenceName = messageDict["messageName"]
    if messageDict["messageNick"] is not None:
        referenceName = messageDict["messageNick"]

    #TODO--------------------------------------------------------------------------------------------
    ######################################BOT-FUNCTIONS##############################################
    #------------------------------------------------------------------------------------------------
    if message.content.startswith('!'):
        # Lists off available public functions to users.
        if message.content.startswith('!info'):
            logMessageInfo("BOT FUNCTION   : \033[35mInformation function accessed\033[39m by ", messageDict["messageName"], " in ", messageDict["channelName"])
            functionList = ""

            # Place entries here to list off.
            #------------------------------------------------------------------------------------------------
            functionList += "**----------------------------------------------**\n"
            functionList += "**Current Server Functions**\n"
            functionList += "**----------------------------------------------**\n"
            functionList += "**!info**: Prints out list of available functions.\n"
            functionList += "**!hello**: Says hello to chat.\n"
            functionList += "**!8ball**: Gives you a magic eight ball response.\n"
            functionList += "**!read**: Reads data from table.\n"
            functionList += "**----------------------------------------------**\n"
            #------------------------------------------------------------------------------------------------

            try: 
                await message.channel.send(functionList)
                logMessageInfo("BOT FUNCTION   : \033[32mInformation function executed\033[39m in ", messageDict["channelName"])
            except:
                logMessageInfo("BOT FAILURE    : \033[31mInformation function could not print\033[39m to ",  messageDict["channelName"])
            return
            
        # Basic hello command.
        if message.content.startswith('!hello'):
            logMessageInfo("BOT FUNCTION   : \033[35mHello function accessed\033[39m by ", messageDict["messageName"], " in ", messageDict["channelName"])

            try:
                await message.channel.send(f'Hello, <@!{messageDict["messageID"]}>!')
                logMessageInfo("BOT FUNCTION   : \033[32mHello function executed\033[39m in ", messageDict["channelName"])
            except:
                logMessageInfo("BOT FAILURE    : \033[31mHello function could not print\033[39m to ",  messageDict["channelName"])
            return

        # Creates a magic eightball result, can be easily used to create a dice roller, a joke maker, or anything that relies on random results.
        if message.content.startswith('!8ball'):
            logMessageInfo("BOT FUNCTION   : \033[35mEight ball function accessed\033[39m by ", messageDict["messageName"], " in ", messageDict["channelName"])
            result = randomChoice(["It is Certain.", "You may rely on it.", "Better not tell you now.", "Concentrate and ask again.", "My sources say no.", "Very doubtful."])

            color = None

            # Sets embed color based on result.
            try:
                if result in ["It is Certain.", "You may rely on it."]:
                    color = 0x00f57a
                elif result in ["Better not tell you now.", "Concentrate and ask again."]:
                    color = 0xfffb08
                elif result in ["My sources say no.", "Very doubtful."]:
                    color = 0xff3700
                else:
                    color = 0x878787
            except:
                color = 0x878787

            choice = {
                "title": "Result:",
                "description": result
            }

            try: 
                await message.channel.send(embed = createEmbed("**Eight Ball**", referenceName, messageDict["messageIcon"], color, choice))
                logMessageInfo("BOT FUNCTION   : \033[32mEight ball function executed\033[39m in ", messageDict["channelName"])
            except:
                logMessageInfo("BOT FAILURE    : \033[31mEight ball function could not print\033[39m to ",  messageDict["channelName"])
            return

        #TODO Reads data from database, this is just a sample of what you can do.  Try to keep these short as to not overload the return string. (I.E. do sums, counts or TOP N * rows.)
        if message.content.startswith('!read') and databaseActive == True:
            logMessageInfo("BOT FUNCTION   : \033[35mRead function accessed\033[39m by ", messageDict["messageName"], " in ", messageDict["channelName"])
            
            query = "SELECT TOP 10 * FROM yourDatabase.dbo.yourTable;"

            if queryDB(cursor, False, query) > 0:
                pass
            else:
                try:
                    endString = ""
                    count = 0
                    for row in stringDictList(createQueryList(cursor)):
                        if count > 0:
                            endString += str(count)  + ". " + row + "\n"
                        else:
                            endString += row + "\n"
                            endString += "**----------------------------------------------**\n"
                        count += 1
                    endString += "**----------------------------------------------**\n"
                    await message.channel.send(endString)   
                    logMessageInfo("BOT FUNCTION   : \033[32mRead function executed\033[39m in ", messageDict["channelName"])
                except:
                    logMessageInfo("BOT FAILURE    : \033[31mRead function could not print\033[39m to ",  messageDict["channelName"])

            return
    #------------------------------------------------------------------------------------------------
    #################################################################################################
    #------------------------------------------------------------------------------------------------

client.run(discordApiToken)