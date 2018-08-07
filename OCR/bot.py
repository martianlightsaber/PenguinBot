import discord
import datetime
import subprocess
import time
from downloader import downloader

from runtesseract import runTesseract
from clonecapture import writeToSheets

TOKEN = 'NDMxOTg3MjM0MjUwNjg2NDY0.Dam0GQ.gS88wCzyA-WrHOXhYX1Gws-3QDM'
screenshotPath = 'screenshots\\'
outputPath = 'OCRoutputs\\'

client = discord.Client()
suffix = 'JST'
datatime = 'default'
lastMessageTime = datetime.datetime.now()
imageCount = 1
fileList = []

def get_time():
    return datatime

def set_time(newTime):
    global datatime
    datatime = newTime
    return

def get_message_time():
    return lastMessageTime

def set_message_time(newMessageTime):
    global lastMessageTime
    lastMessageTime = newMessageTime
    return

def get_image_count():
    return imageCount

def set_image_count(newCount):
    global imageCount
    imageCount = newCount
    return

def get_file_list():
    return fileList

def add_to_file_list(newFile):
    global fileList
    fileList.append(newFile)
    return

def reset_file_list():
    global fileList
    fileList = []
    return

@client.event
async def on_message(message):
    # we do not want the bot to reply to itself
    if message.author.bot:
        return

    currentMessageTime = message.timestamp
    timeElapsed = currentMessageTime - get_message_time()
    if timeElapsed.seconds > 30*60:
        set_time('default')
        set_image_count(1)
        reset_file_list()
        duration = 'Time since last message was '+str(timeElapsed.seconds//60)+' minutes'
        msg = duration.format(message)
        await client.send_message(message.channel, msg)
    
    if message.content.endswith(suffix):
        try:
            timestamp,suff = message.content.split(' ')
        except:
            msg = 'please enter a time in the format "XX:00 JST"'.format(message)
            await client.send_message(message.channel, msg)
            set_message_time(currentMessageTime)
            return
        hour = str(int(timestamp.split(':')[0]+timestamp.split(':')[1])//100)+'00'
        if len(hour) < 4:
            hour = '0'+hour
        response = 'Closest hour is '+hour
        set_time(hour)
        msg = response.format(message)
        await client.send_message(message.channel, msg)

    #if len(message.attachments) == 0:
    #    msg = 'No attachments'.format(message)
    #    await client.send_message(message.channel, msg)

    if len(message.attachments) > 0:
        if get_time() == 'default':
            msg = 'please enter a time in the format "XX:00 JST" then reattach your image'.format(message)
            await client.send_message(message.channel, msg)
            set_message_time(currentMessageTime)
            return
        for attachment in message.attachments:
            url = attachment['url']
            #msg = url.format(message)
            #await client.send_message(message.channel, msg)
            #trim_file_name = get_time.split(':')[0]+get_time.split(':')[1]
            #file_name = trim_file_name+'_'+str(get_image_count())
            file_name = str(get_image_count())
            file_path = screenshotPath+file_name
            downloader(url,file_path)
            add_to_file_list(file_name+'.png')
            set_image_count(get_image_count()+1)

    if message.content.startswith('reset Timer'):
        set_time('default')
        set_image_count(1)
        reset_file_list()
        await client.send_message(message.channel, 'Timer reset')

    if message.content.startswith('!chart please'):
        chartImg = 'https://docs.google.com/spreadsheets/d/e/2PACX-1vRdimqALMXUEY5TiqUO9nLR1AwlT_4kVCYVRbJ48cAnplZTXQe8FqmOHPCq0ClCLwhtrmKHBPPhBlfG/pubchart?oid=621491566&format=image'
        msg = chartImg.format(message)
        await client.send_message(message.channel, msg)

    if message.content.startswith('run OCR'):
        #print(screenshotPath+', '+outputPath)
        #print(get_file_list()[0]+','+get_file_list()[3])
        runTesseract(screenshotPath,outputPath,get_file_list(),'merged.txt')
        didItWork = writeToSheets(outputPath+'merged.txt',datatime)
        
        process = subprocess.Popen(['del','/f',outputPath+'*.txt'], shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        output = process.communicate()[0]
        print(output)

        process = subprocess.Popen(['del','/f',screenshotPath+'*.png'], shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        output = process.communicate()[0]
        print(output)
        
        set_time('default')
        set_image_count(1)
        reset_file_list()

        msg = didItWork.format(message)
        await client.send_message(message.channel, msg)

        #if didItWork == 'OCR success! Please check the graph for anomalies.':
        #    time.sleep(30)
        #    chartImg = 'https://docs.google.com/spreadsheets/d/e/2PACX-1vRdimqALMXUEY5TiqUO9nLR1AwlT_4kVCYVRbJ48cAnplZTXQe8FqmOHPCq0ClCLwhtrmKHBPPhBlfG/pubchart?oid=621491566&format=image'
        #    msg = chartImg.format(message)
        #    await client.send_message(discord.Object(id='416466893352992769'), msg)
            
           
    set_message_time(currentMessageTime)
    return

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

client.run(TOKEN)
