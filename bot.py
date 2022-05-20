from numpy import maximum
import telebot
import random
import qrcode
from khayyam import JalaliDatetime
from datetime import datetime
from gtts import gTTS

nazanin_bot = telebot.TeleBot('5326330811:AAGxKEJIH8KIkqZPqBV7Q9HU2cODGFpUOHk')
markup = telebot.types.ReplyKeyboardMarkup()

game_btn = telebot.types.KeyboardButton('New Game')
markup.add(game_btn)


@nazanin_bot.message_handler(commands=['start'])
def welcome_func(message: str):
    user_firs_name = str(message.chat.first_name)
    nazanin_bot.reply_to(message, 'Hello '+ user_firs_name + ' ,Welcome to my bot')

@nazanin_bot.message_handler(commands=['game'])
def game_func(message):
    nazanin_bot.reply_to(message, 'guess a number between 0 and 50:')
    global num
    num = random.randint(0,50)
    nazanin_bot.register_next_step_handler(message, game_func2)

def game_func2(message):
    if int(message.text) == num :     
        nazanin_bot.reply_to(message, 'exactly, you won!',reply_markup = markup)
        nazanin_bot.register_next_step_handler(message, game_func)

    elif int(message.text) < num :
        msg = nazanin_bot.reply_to(message, 'go upper ')
        nazanin_bot.register_next_step_handler(msg, game_func2)
    elif int(message.text) > num :     
        msg = nazanin_bot.reply_to(message, 'go lower')
        nazanin_bot.register_next_step_handler(msg, game_func2)    

@nazanin_bot.message_handler(commands=['age'])
def age_func1(message):
    nazanin_bot.reply_to(message, 'Enter your Date of Birth! \nex: 1373-10-24')
    nazanin_bot.register_next_step_handler(message, age_func2)

def age_func2(message):
    date = message.text
    list = str(date).split('-')
    difference = JalaliDatetime.now() - JalaliDatetime(list[0],list[1],list[2])
    nazanin_bot.send_message(message.chat.id , 'your age: ' + str(difference.days//365))


@nazanin_bot.message_handler(commands=['voice'])
def voice_func1(message):
    nazanin_bot.reply_to(message,'i am Echo bot,Just type anything...')
    nazanin_bot.register_next_step_handler(message , voice_func2)
def voice_func2(message):    
    str = message.text
    myobj = gTTS(text=str, lang='en', slow=False)
    #saving the audio in a mp3 file
    myobj.save('voice.mp3')
    mp3_file = open('voice.mp3', 'rb')
    nazanin_bot.send_audio(message.chat.id, mp3_file)


@nazanin_bot.message_handler(commands=['max'])
def call_max(message):
    msg = nazanin_bot.reply_to(message, 'Enter numbers: 13,56,45,...')
    nazanin_bot.register_next_step_handler(msg , max_func)

def max_func(message):  
    text = str(message.text)
    list1 = text.split(',')
    max = list1[0]
    for i in range(1,len(list1)):
        if int(max) < int(list1[i]):
            max = list1[i]    
    nazanin_bot.send_message(message.chat.id , max)    

@nazanin_bot.message_handler(commands=['argmax'])
def argmax_func(message):
    msg = nazanin_bot.reply_to(message, 'Enter numbers: 10,20,73,.. ')
    nazanin_bot.register_next_step_handler(msg, maxindex_func)

def maxindex_func(message):  
    text = message.text
    list1 = str(text).split(',')
    max = list1[0]
    for i in range(1,len(list1)):
        if int(max) < int(list1[i]):
            max = list1[i]
    i = list1.index(max) 
    nazanin_bot.send_message( message.chat.id , 'index of maximum number: '+ str(i) ) 


@nazanin_bot.message_handler(commands=['qrcode'])
def qrcod(message):
    nazanin_bot.reply_to(message, 'enter a text for converting to qrcode...')
    nazanin_bot.register_next_step_handler(message, qrcod_func)
def qrcod_func(message):    
    text = message.text
    image = qrcode.make(text)
    image.save('qrcode.png')
    file = open('qrcode.png', 'rb')
    nazanin_bot.send_photo(message.chat.id, file)

@nazanin_bot.message_handler(commands= ['help'])
def help_func(message):
    nazanin_bot.reply_to(message, '/game (guess a number with game)\n/age (it show your age with date of birth) \n/voice (it convert string to audio)  \n/max (find the maximum number in a list)\n/argmax (find index of the maximum number in a list)\n/qrcode')


nazanin_bot.polling()