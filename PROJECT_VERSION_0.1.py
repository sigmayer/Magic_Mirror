import subprocess
from subprocess import Popen, PIPE
import sys,os
import asyncio
import telepot
import telepot.aio
from tkinter import messagebox
from telepot.namedtuple import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove, ForceReply
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton
from telepot.namedtuple import InlineQueryResultArticle, InlineQueryResultPhoto, InputTextMessageContent
from datetime import datetime,  timezone, tzinfo, timedelta
import time
from tkinter import *
import tkinter.font
import locale
import threading
import time
import requests
import json
import traceback
import feedparser
import pygame
from pytz import timezone
import pytz
from contextlib import contextmanager
from PIL import Image, ImageTk
LOCALE_LOCK = threading.Lock()
utc = pytz.utc
utc.zone

@contextmanager
def setlocale(name): #thread proof function to work with locale
    with LOCALE_LOCK:
        saved = locale.setlocale(locale.LC_ALL)
        try:
            yield locale.setlocale(locale.LC_ALL, name)
        finally:
            locale.setlocale(locale.LC_ALL, saved)

def readTimeZone():
    with open("timezone.txt", "r") as f:
        line = f.readline()
    return line

def setTimeZone(timezone):
    with open("timezone.txt", "w") as f:
        f.write(timezone)
        
def readCityForWeather():
    with open("CityWeather.txt", "r") as f:
        line = f.readline()
    return line

def setCityForWeather(city):
    with open("CityWeather.txt", "w") as f:
        f.write(city)
        
def readNotes(day):
    tmp = []
    i = 0
    while i < 5:
        tmp.append('')
        i = i+1
        
    a = 0
    f = open(day)
    for line in f:
        if a < 5:
            tmp[a] = line
            a = a+1
    return tmp

def setNote(day, note):
    with open(day, "a") as f:
        f.write(note + '\n')

def deleteNotes(day):
    with open(day, "w") as f:
        f.write(' ')

            
ui_locale = '' 
time_format = 24 #12 or 24
date_format = "%b %d, %Y" 
xlarge_text_size = 94
large_text_size = 48
big_text_size = 33
medium_text_size = 28
small_text_size = 18
TOKEN = "682185822:AAGz6IhOj-cJM0n5M3m6nZlOstjM9kluY0M"
chat_allow1 = 148545016
chat_allow2 = 885204760
message_with_inline_keyboard = None
id_write_critical_temper = 0


icon_lookup_day = {
    'ясно': "c:\\users\\123\\pictures\\weather_day\\sun.png", 
    'мокрый снег': "c:\\users\\123\\pictures\\weather_day\\sleet.png",   
    'облачно': "c:\\users\\123\\pictures\\weather_day\\cloudy.png",
    'слегка облачно': "c:\\users\\123\\pictures\\weather_day\\partialy-cloudy.png",
    'пасмурно': "c:\\users\\123\\pictures\\weather_day\\overcast-day.png",  
    'дождь': "c:\\users\\123\\pictures\\weather_day\\rainy-day.png",  
    'снег': "c:\\users\\123\\pictures\\weather_day\\snow.png", 
    'снег с дождем': "c:\\users\\123\\pictures\\weather_day\\sleet.png",
    'легкий дождь': "c:\\users\\123\\pictures\\weather_day\\small_rain.png",
    'гроза': "c:\\users\\123\\pictures\\weather_day\\lighting.png"
}

icon_lookup_night = {
    'ясно': "c:\\users\\123\\pictures\\weather_night\\moon.png",  
    'мокрый снег': "c:\\users\\123\\pictures\\weather_night\\sleet.png",  
    'облачно': "c:\\users\\123\\pictures\\weather_night\\partialy-cloudy.png",
    'слегка облачно': "c:\\users\\123\\pictures\\weather_night\\partialy-cloudy.png",
    'пасмурно': "c:\\users\\123\\pictures\\weather_night\\overcast-day.png",  
    'дождь': "c:\\users\\123\\pictures\\weather_night\\rainy-day.png",  
    'снег': "c:\\users\\123\\pictures\\weather_night\\snow.png",  
    'снег с дождем': "c:\\users\\123\\pictures\\weather_night\\sleet.png",
    'легкий дождь': "c:\\users\\123\\pictures\\weather_night\\small_rain.png",
    'гроза': "c:\\users\\123\\pictures\\weather_night\\lighting.png"
}


class Weather(Frame):
    def __init__(self, parent, *args, **kwargs):
        Frame.__init__(self, parent, bg='black')
        self.city = "Санкт-Петербург"
        self.app = "42dfb1b3420a987588771d0dc21cf225"
        self.temperature = ''
        self.weather_info = ''
        self.forecast_temp = ''
        self.forecast_summ = ''
        self.forecast = ''
        
        self.degreeFrm = Frame(self, bg="black")
        self.degreeFrm.pack(side=BOTTOM, anchor=W, pady = 40)

        self.iconLb1 = Label(self, bg="black")
        self.iconLb1.pack(side=LEFT, anchor=W, padx=20)

        self.wthrLbl = Label(self, font=('Helvetica', large_text_size), fg="white", bg="black")
        self.wthrLbl.pack(side=BOTTOM, anchor=W, padx=20)

        self.temperatureLbl = Label(self, font=('Helvetica', xlarge_text_size), fg="white", bg="black")
        self.temperatureLbl.pack(side=LEFT, anchor=W)
        
        self.forecast_iconLb1 = Label(self.degreeFrm, bg="black")
        self.forecast_iconLb1.pack(side=LEFT, anchor=W, padx=30)

        self.forecast_summLbl = Label(self.degreeFrm, font=('Helvetica', big_text_size), fg="white", bg="black")
        self.forecast_summLbl.pack(side=BOTTOM, anchor=W)

        self.forecast_tempLbl = Label(self.degreeFrm, font=('Helvetica', large_text_size), fg="white", bg="black")
        self.forecast_tempLbl.pack(side=LEFT, anchor=W)
        

        self.get_ip(self.city)
        self.get_weather()

    def get_ip(self, fileCity):

        s_city = fileCity
        city_id = 0
        appid = self.app
        
        try:
            res = requests.get("http://api.openweathermap.org/data/2.5/find", params={'q': s_city, 'type': 'like', 'units': 'metric', 'APPID': appid})
            data = res.json()
            return data['list'][0]['id']
        except Exception as e:
            traceback.print_exc()
            return ("Error: %s. Cannot get ip." %e)

    def get_weather(self):
        
        fileCity = readCityForWeather()
        city_id = self.get_ip(fileCity)
        appid = self.app
        
        try:

            degree_sign= u'\N{DEGREE SIGN}'
            r = requests.get("http://api.openweathermap.org/data/2.5/weather", params={'id': city_id, 'units': 'metric', 'lang': 'ru', 'APPID': appid})
            weather_obj = r.json()
            wthr = weather_obj['weather'][0]['description']
            temp1 = weather_obj['main']['temp']
            temp1 = round(temp1)
            temp = (str(temp1) + degree_sign)

            weather_info2 = wthr
            icon_id = wthr

            time_inf = Clock(self)
            timing = time_inf.time1
            a = timing.split(':')
            hours = a[0]
            hours = int(hours)
            next_hour = hours + 3

            w = requests.get("https://api.openweathermap.org/data/2.5/forecast", params={'id': city_id, 'units': 'metric', 'lang': 'ru', 'APPID': appid})
            forecast_obj = w.json()
            forecast_temp1 = forecast_obj['list'][1]['main']['temp']
            forecast_temp1 = round(forecast_temp1)
            forecast_temp1 = (str(forecast_temp1)+ degree_sign)
            forecast_summ1 = forecast_obj['list'][2]['weather'][0]['description']
            forecast_icon = forecast_obj['list'][2]['weather'][0]['description']

            if hours >= 8 and hours <= 20:
                if icon_id in icon_lookup_day:
                    icon = icon_lookup_day[icon_id]
                    image = Image.open(icon)
                    image = image.resize((210, 210), Image.ANTIALIAS)
                    photo = ImageTk.PhotoImage(image)
                    self.iconLb1.image = photo
                    self.iconLb1.config(image = photo)
                else:
                    self.iconLb1.config(image='')
                
 
            else:
                if icon_id in icon_lookup_night:
                    icon = icon_lookup_night[icon_id]
                    image = Image.open(icon)
                    image = image.resize((210, 210), Image.ANTIALIAS)
                    photo = ImageTk.PhotoImage(image)
                    self.iconLb1.image = photo
                    self.iconLb1.config(image = photo)
                else:
                    self.iconLb1.config(image='')

            if weather_info2 is not None:
                if self.weather_info != weather_info2:
                    self.weather_info = weather_info2
                    self.wthrLbl.config(text=weather_info2)

            if self.temperature != temp:
                self.temperature = temp
                self.temperatureLbl.config(text=temp)



            if self.forecast_temp != forecast_temp1:
                self.forecast_temp = forecast_temp1
                self.forecast_tempLbl.config(text=forecast_temp1)

            if forecast_summ1 is not None:
                if self.forecast_summ != forecast_summ1:
                    self.forecast_summ = forecast_summ1
                    self.forecast_summLbl.config(text=forecast_summ1)
            
            if next_hour >= 8 and next_hour <= 20:        
                if forecast_icon in icon_lookup_day:
                    icon = icon_lookup_day[forecast_icon]
                    image = Image.open(icon)
                    image = image.resize((130, 130), Image.ANTIALIAS)
                    photo = ImageTk.PhotoImage(image)
                    self.forecast_iconLb1.image = photo
                    self.forecast_iconLb1.config(image = photo)
                else:
                    self.forecast_iconLb1.config(image='')
            else:
                if forecast_icon in icon_lookup_night:
                    icon = icon_lookup_night[forecast_icon]
                    image = Image.open(icon)
                    image = image.resize((130, 130), Image.ANTIALIAS)
                    photo = ImageTk.PhotoImage(image)
                    self.forecast_iconLb1.image = photo
                    self.forecast_iconLb1.config(image = photo)
                else:
                    self.forecast_iconLb1.config(image='')
                
        except Exception as e:
            traceback.print_exc()
            print ("Error: %s. Cannot get weather." %e)

        #self.after(500, self.get_weather)
        self.after(200, self.get_weather)

class Notes(Frame):
    def __init__(self, parent, *args, **kwargs):
        Frame.__init__(self, parent, bg = 'black')
        self.note1 = ''
        self.note2 = ''
        self.note3 = ''
        self.note4 = ''
        self.note5 = ''
        
        self.note1Lb = Label(self, text=(self.note1), font=('Helvetica', medium_text_size), fg = "white", bg = "black")
        self.note1Lb.pack(side=TOP, anchor = W)
        
        self.note2Lb = Label(self, text=(self.note2), font=('Helvetica', medium_text_size), fg = "white", bg = "black")
        self.note2Lb.pack(side=TOP, anchor = W)
        
        self.note3Lb = Label(self, text=(self.note3), font=('Helvetica', medium_text_size), fg = "white", bg = "black")
        self.note3Lb.pack(side=TOP, anchor = W)
        
        self.note4Lb = Label(self, text=(self.note4), font=('Helvetica', medium_text_size), fg = "white", bg = "black")
        self.note4Lb.pack(side=TOP, anchor = W)
        
        self.note5Lb = Label(self, text=(self.note5), font=('Helvetica', medium_text_size), fg = "white", bg = "black")
        self.note5Lb.pack(side=TOP, anchor = W)
        self.getUpdNotes()

    def getUpdNotes(self):
        TextNote = []
        day_of_week = time.strftime('%A')
        if day_of_week == 'Monday':
            TextNote = readNotes('Monday.txt')
        elif day_of_week == 'Tuesday':
            TextNote = readNotes('Tuesday.txt')
        elif day_of_week == 'Wednesday':
            TextNote = readNotes('Wednesday.txt')
        elif day_of_week == 'Thursday':
            TextNote = readNotes('Thursday.txt')
        elif day_of_week == 'Friday':
            TextNote = readNotes('Friday.txt')
        elif day_of_week == 'Saturday':
            TextNote = readNotes('Saturday.txt')
        elif day_of_week == 'Sunday':
            TextNote = readNotes('Sunday.txt')
            
        oldNote = self.note1
        if oldNote != TextNote[0]:
            self.note1 = TextNote[0]
            self.note1Lb.config(text = TextNote[0])

        oldNote = self.note2
        if oldNote != TextNote[1]:
            self.note2 = TextNote[1]
            self.note2Lb.config(text = TextNote[1])

        oldNote = self.note3
        if oldNote != TextNote[2]:
            self.note3 = TextNote[2]
            self.note3Lb.config(text = TextNote[2])

        oldNote = self.note4
        if oldNote != TextNote[3]:
            self.note4 = TextNote[3]
            self.note4Lb.config(text = TextNote[3])

        oldNote = self.note5
        if oldNote != TextNote[4]:
            self.note5 = TextNote[4]
            self.note5Lb.config(text = TextNote[4])
            
        self.after(200, self.getUpdNotes)
        

class Clock(Frame):
    def __init__(self, parent, *args, **kwargs):
        Frame.__init__(self, parent, bg='black')
        self.time1 = ''
        self.timeLbl = Label(self, font=('DIN Next CYR UltraLight', xlarge_text_size), fg="white", bg="black")
        self.timeLbl.pack(side=TOP, anchor=CENTER)
        self.day_of_week1 = ''
        self.date1 = ''
        self.allString1 = ''
        self.allStringLb1 = Label(self, text =(self.day_of_week1, self.date1), font=('DIN Next CYR UltraLight', medium_text_size), fg="white", bg="black")
        self.allStringLb1.pack(side=TOP, anchor=CENTER)
        self.tick()

    def tick(self):
        tz = readTimeZone()
        utc_time = datetime.utcnow()
        temp_tz = pytz.timezone(tz)
        utc_time = utc_time.replace(tzinfo=pytz.UTC)
        nor_tz = utc_time.astimezone(temp_tz)  
        with setlocale(ui_locale):
            time2 = nor_tz.strftime ('%H:%M')

            day_of_week2 = time.strftime('%A')
            date2 = time.strftime("%d.%m")
            
	    # if time string has changed, update it
            if time2 != self.time1:
                self.time1 = time2
                self.timeLbl.config(text=time2)
            if day_of_week2 != self.day_of_week1:
                self.day_of_week1 = day_of_week2
                self.allStringLb1.config(text=(day_of_week2,',', self.date1))
            if date2 != self.date1:
                self.date1 = date2
                self.allStringLb1.config(text=(self.day_of_week1,',', date2))                         
            # calls itself every 200 milliseconds
            self.timeLbl.after(200, self.tick)

async def set_notes(msg, day):
    content_type, chat_type, chat_id = telepot.glance(msg)
    print('Chat(set_notes):', content_type, chat_type)
    print("id отправителя сообщения(Ura): "+str(chat_id))
    if chat_id == chat_allow1 or chat_id == chat_allow2:
        if content_type != 'text':
            return
        else:
            ok = 1
        Text = msg['text']
        print(Text)
        Text = msg['text']
        print(Text)
        if day == 'Понедельник':
            setNote('Monday.txt', Text)
        elif day == 'Вторник':
            setNote('Tuesday.txt', Text)
        elif day == 'Среда':
            setNote('Wednesday.txt', Text)
        elif day == 'Четверг':
            setNote('Thursday.txt', Text)
        elif day == 'Пятница':
            setNote('Friday.txt', Text)
        elif day == 'Суббота':
            setNote('Saturday.txt', Text)
        elif day == 'Воскресенье':
            setNote('Sunday.txt', Text)

async def on_chat_message(msg):
    global id_write_critical_temper
    content_type, chat_type, chat_id = telepot.glance(msg)
    print('Chat:', content_type, chat_type)
    print("id отправителя сообщения: "+str(chat_id))
    if chat_id == chat_allow1 or chat_id == chat_allow2:
        if content_type != 'text':
            return
        else:
            ok = 1
        command = msg['text'].lower()
        print(command)

        if command == '/help':
            markup = ReplyKeyboardMarkup(keyboard=[
            [dict(text='Сменить часовой пояс')],
            [dict(text='Сменить город')],
            [dict(text='Удалить заметки')],
            ])
            await bot.sendMessage(chat_id, 'Привет, я Магическое Зеркало. Можешь воспользоваться одной из готовых команд. Если же хочешь добавить заметку - напиши сообщение следующего типа: <день недели>#<заметка>;<заметка>;... . Помни - на каждый день ты можешь иметь не больше пяти заметок. Готов вкалывать.', reply_markup=markup)

        elif command == 'главное меню':
            markup = ReplyKeyboardMarkup(keyboard=[
            [dict(text='Сменить часовой пояс')],
            [dict(text='Сменить город')],
            [dict(text='Удалить заметки')],
            ])
            await bot.sendMessage(chat_id, 'Опять работа?', reply_markup=markup)

        elif command == u'сменить часовой пояс':
            markup = ReplyKeyboardMarkup(keyboard=[
            [dict(text='MSK(GMT+4)'), dict(text='YEKT (GMT+06)')],
            [dict(text='OMST(GMT+07)')],
            [dict(text='Главное меню')],
            ])
            await bot.sendMessage(chat_id, 'Да будет так.', reply_markup=markup)

        elif command == u'сменить город':
            markup = ReplyKeyboardMarkup(keyboard=[
            [dict(text='Москва'), dict(text='Санкт-Петербург')],
            [dict(text='Новосибирск'), dict(text='Екатеринбург')],
            [dict(text='Нижний Новгород'), dict(text='Казань')],
            [dict(text='Уфа'), dict(text='Омск')],
            [dict(text='Главное меню')],
            ])
            await bot.sendMessage(chat_id, 'Займемся этим.', reply_markup=markup)

        elif command == u'удалить заметки':
            markup = ReplyKeyboardMarkup(keyboard=[
            [dict(text='Понедельник'), dict(text='Вторник')],
            [dict(text='Среда'), dict(text='Четверг')],
            [dict(text='Пятница'), dict(text='Суббота')],
            [dict(text='Воскресенье'), dict(text='Главное меню')],
            ])
            await bot.sendMessage(chat_id, 'Склоняюсь перед вашей волей.', reply_markup=markup)

        elif command == u'omst(gmt+07)':
            markup = ReplyKeyboardMarkup(keyboard=[
            [dict(text='Сменить часовой пояс')],
            [dict(text='Сменить город')],
            [dict(text='Добавить заметку')],
            ])
            R = str(readTimeZone())
            setTimeZone('Etc/GMT-6')
            await bot.sendMessage(chat_id, 'Правильное решение. Было %s, стало Europe/OMSK.' %R,  reply_markup=markup)

        elif command == u'yekt (gmt+06)':
            markup = ReplyKeyboardMarkup(keyboard=[
            [dict(text='Сменить часовой пояс')],
            [dict(text='Сменить город')],
            [dict(text='Удалить заметки')],
            ])
            R = str(readTimeZone())
            setTimeZone('Etc/GMT-5')
            await bot.sendMessage(chat_id, 'Правильное решение. Было %s, стало Europe/YEKT.' %R,  reply_markup=markup)

        elif command == u'msk(gmt+4)':
            markup = ReplyKeyboardMarkup(keyboard=[
            [dict(text='Сменить часовой пояс')],
            [dict(text='Сменить город')],
            [dict(text='Удалить заметки')],
            ])
            R = str(readTimeZone())
            setTimeZone('Etc/GMT-3')
            await bot.sendMessage(chat_id, 'Правильное решение. Было %s, стало Europe/MSK.' %R,  reply_markup=markup)
           
        elif command == u'москва':
            markup = ReplyKeyboardMarkup(keyboard=[
            [dict(text='Сменить часовой пояс')],
            [dict(text='Сменить город')],
            [dict(text='Удалить заметки')],
            ])
            setCityForWeather('Москва')
            await bot.sendMessage(chat_id, 'Дело сделано.',  reply_markup=markup)

        elif command == u'нижний новгород':
            markup = ReplyKeyboardMarkup(keyboard=[
            [dict(text='Сменить часовой пояс')],
            [dict(text='Сменить город')],
            [dict(text='Удалить заметки')],
            ])
            setCityForWeather('Нижний Новгород')
            await bot.sendMessage(chat_id, 'Дело сделано.',  reply_markup=markup)

        elif command == u'уфа':
            markup = ReplyKeyboardMarkup(keyboard=[
            [dict(text='Сменить часовой пояс')],
            [dict(text='Сменить город')],
            [dict(text='Удалить заметки')],
            ])
            setCityForWeather('Уфа')
            await bot.sendMessage(chat_id, 'Дело сделано.',  reply_markup=markup)

        elif command == u'омск':
            markup = ReplyKeyboardMarkup(keyboard=[
            [dict(text='Сменить часовой пояс')],
            [dict(text='Сменить город')],
            [dict(text='Удалить заметки')],
            ])
            setCityForWeather('Омск')
            await bot.sendMessage(chat_id, 'Дело сделано.',  reply_markup=markup)

        elif command == u'казань':
            markup = ReplyKeyboardMarkup(keyboard=[
            [dict(text='Сменить часовой пояс')],
            [dict(text='Сменить город')],
            [dict(text='Удалить заметки')],
            ])
            setCityForWeather('Казань')
            await bot.sendMessage(chat_id, 'Дело сделано.',  reply_markup=markup)

        elif command == u'новосибирск':
            markup = ReplyKeyboardMarkup(keyboard=[
            [dict(text='Сменить часовой пояс')],
            [dict(text='Сменить город')],
            [dict(text='Удалить заметки')],
            ])
            setCityForWeather('Новосибирск')
            await bot.sendMessage(chat_id, 'Дело сделано.',  reply_markup=markup)

        elif command == u'санкт-петербург':
            markup = ReplyKeyboardMarkup(keyboard=[
            [dict(text='Сменить часовой пояс')],
            [dict(text='Сменить город')],
            [dict(text='Удалить заметки')],
            ])
            setCityForWeather('Санкт-Петербург')
            await bot.sendMessage(chat_id, 'Дело сделано.',  reply_markup=markup)

        elif command == u'екатеринбург':
            markup = ReplyKeyboardMarkup(keyboard=[
            [dict(text='Сменить часовой пояс')],
            [dict(text='Сменить город')],
            [dict(text='Удалить заметки')],
            ])
            setCityForWeather('екатеринбург')
            await bot.sendMessage(chat_id, 'Дело сделано.',  reply_markup=markup)

        elif command == 'понедельник':
            markup = ReplyKeyboardMarkup(keyboard=[
            [dict(text='Сменить часовой пояс')],
            [dict(text='Сменить город')],
            [dict(text='Удалить заметки')],
            ])
            deleteNotes("Monday.txt")
            await bot.sendMessage(chat_id, 'Сгинь нечистая сила! Останься чистый спирт!',  reply_markup=markup)

        elif command == 'вторник':
            markup = ReplyKeyboardMarkup(keyboard=[
            [dict(text='Сменить часовой пояс')],
            [dict(text='Сменить город')],
            [dict(text='Удалить заметки')],
            ])
            deleteNotes("Tuesday.txt")
            await bot.sendMessage(chat_id, 'Сгинь нечистая сила! Останься чистый спирт!',  reply_markup=markup)

        elif command == 'среда':
            markup = ReplyKeyboardMarkup(keyboard=[
            [dict(text='Сменить часовой пояс')],
            [dict(text='Сменить город')],
            [dict(text='Удалить заметки')],
            ])
            deleteNotes("Wednesday.txt")
            await bot.sendMessage(chat_id, 'Сгинь нечистая сила! Останься чистый спирт!',  reply_markup=markup)

        elif command == 'четверг':
            markup = ReplyKeyboardMarkup(keyboard=[
            [dict(text='Сменить часовой пояс')],
            [dict(text='Сменить город')],
            [dict(text='Добавить заметку')],
            ])
            deleteNotes("Thursday.txt")
            await bot.sendMessage(chat_id, 'Сгинь нечистая сила! Останься чистый спирт!',  reply_markup=markup)

        elif command == 'пятница':
            markup = ReplyKeyboardMarkup(keyboard=[
            [dict(text='Сменить часовой пояс')],
            [dict(text='Сменить город')],
            [dict(text='Удалить заметки')],
            ])
            deleteNotes("Friday.txt")
            await bot.sendMessage(chat_id, 'Сгинь нечистая сила! Останься чистый спирт!',  reply_markup=markup)

        elif command == 'суббота':
            markup = ReplyKeyboardMarkup(keyboard=[
            [dict(text='Сменить часовой пояс')],
            [dict(text='Сменить город')],
            [dict(text='Удалить заметки')],
            ])
            deleteNotes("Saturday.txt")
            await bot.sendMessage(chat_id, 'Сгинь нечистая сила! Останься чистый спирт!',  reply_markup=markup)

        elif command == 'воскресенье':
            markup = ReplyKeyboardMarkup(keyboard=[
            [dict(text='Сменить часовой пояс')],
            [dict(text='Сменить город')],
            [dict(text='Удалить заметки')],
            ])
            deleteNotes("Sunday.txt")
            await bot.sendMessage(chat_id, 'Сгинь нечистая сила! Останься чистый спирт!',  reply_markup=markup)

        else:
            markup = ReplyKeyboardMarkup(keyboard=[
            [dict(text='Сменить часовой пояс')],
            [dict(text='Сменить город')],
            [dict(text='Удалить заметки')],
            ])
            command = msg['text']
            if command.find('#')!= -1:
                note = command.split('#', 1)
                if note[0] == 'Понедельник' or note[0] == 'понедельник' or note[0] == 'пн' or note[0] == 'Пн' or note[0] == 'Понедельник ' or note[0] == 'понедельник ' or note[0] == 'пн ' or note[0] == 'Пн ':
                    tmp = note[1].split(';')
                    i = 0
                    while i < len(tmp):
                        setNote("Monday.txt", tmp[i])
                        i = i+1
                    
                elif note[0] == 'Вторник' or note[0] == 'вторник' or note[0] == 'вт' or note[0] == 'Вт' or note[0] == 'Вторник ' or note[0] == 'вторник ' or note[0] == 'вт ' or note[0] == 'Вт ':
                    tmp = note[1].split(';')
                    i = 0
                    while i < len(tmp):
                        setNote("Tuesday.txt", tmp[i])
                        i = i+1
                    
                elif note[0] == 'Среда' or note[0] == 'среда' or note[0] == 'ср' or note[0] == 'Ср' or note[0] == 'Среда ' or note[0] == 'среда ' or note[0] == 'ср ' or note[0] == 'Ср ':
                    tmp = note[1].split(';')
                    i = 0
                    while i < len(tmp):
                        setNote("Wednesday.txt", tmp[i])
                        i = i+1
                    
                elif note[0] == 'Четверг' or note[0] == 'четверг' or note[0] == 'чт' or note[0] == 'Чт' or note[0] == 'Четверг ' or note[0] == 'четверг ' or note[0] == 'чт ' or note[0] == 'Чт ':
                    tmp = note[1].split(';')
                    i = 0
                    while i < len(tmp):
                        setNote("Thursday.txt", tmp[i])
                        i = i+1
                        
                elif note[0] == 'Пятница' or note[0] == 'пятница' or note[0] == 'пт' or note[0] == 'Пт' or note[0] == 'Пятница ' or note[0] == 'пятница ' or note[0] == 'пт ' or note[0] == 'Пт ':
                    tmp = note[1].split(';')
                    i = 0
                    while i < len(tmp):
                        setNote("Friday.txt", tmp[i])
                        i = i+1
                    
                elif note[0] == 'Суббота' or note[0] == 'суббота' or note[0] == 'сб' or note[0] == 'Сб' or note[0] == 'Суббота ' or note[0] == 'суббота ' or note[0] == 'сб ' or note[0] == 'Сб ' :
                    tmp = note[1].split(';')
                    i = 0
                    while i < len(tmp):
                        setNote("Saturday.txt", tmp[i])
                        i = i+1
                    
                elif note[0] == 'Воскресенье' or note[0] == 'воскресенье' or note[0] == 'вс' or note[0] == 'Вс' or note[0] == 'Воскресенье ' or note[0] == 'воскресенье ' or note[0] == 'вс ' or note[0] == 'Вс ':
                    tmp = note[1].split(';')
                    i = 0
                    while i < len(tmp):
                        setNote("Sunday.txt", tmp[i])
                        i = i+1
                    
                await bot.sendMessage(chat_id, 'Мудрые слова!',  reply_markup=markup)
            else:
                await bot.sendMessage(chat_id, 'Дурацкий план.',  reply_markup=markup)

    else:
        #если чат айди не соответствует разрешенному
        markup_protect = ReplyKeyboardMarkup(keyboard=[[dict(text='Нельзя сотворить здесь.')]])
        await bot.sendMessage(chat_id, 'Вы не имеете доступа к этому боту! Обратитесь к владельцу за разрешением.', reply_markup=markup_protect)
        return

#THREAD#

def run_tgBot(async_loop, loop, bot):
    threading.Thread(target=tgBot_thread, args=(async_loop, loop, bot,)).start()
def tgBot_thread(async_loop, loop, bot):
    asyncio.set_event_loop(loop)
    loop.run_until_complete(bot.message_loop({'chat': on_chat_message}))                  

class FullscreenWindow:

    def __init__(self, async_loop, loop, bot):
        self.tk = Tk()
        self.tk.configure(background='black')
        self.tk.geometry('1366x768')
        
        self.topFrame = Frame(self.tk, background = 'black')
        self.topFrame.pack(side = TOP, fill=BOTH, expand = YES)
        
        self.bottomFrame = Frame(self.tk, background = 'black')
        self.bottomFrame.pack(side = BOTTOM, fill=BOTH, expand = YES)
        
        self.rightFrame = Frame(self.tk, background = 'black')
        self.rightFrame.pack(side = RIGHT, fill=BOTH, expand = YES)
        
        self.state = False
        self.tk.bind("<Return>", self.toggle_fullscreen)
        self.tk.bind("<Escape>", self.end_fullscreen)
        
        # clock
        self.clock = Clock(self.topFrame)
        self.clock.pack(anchor=NW, padx=60, pady=10)
        
        # weather
        self.weather = Weather(self.topFrame)
        self.weather.pack(anchor=NW, padx=60, pady=50)
        
        # notes
        self.Notes = Notes(self.topFrame)
        self.Notes.pack(anchor = NW, padx = 40, pady = 10)
        
        # thread
        run_tgBot(async_loop, loop, bot)
        self.tk.mainloop()

    def toggle_fullscreen(self, event=None):
        self.state = not self.state  # Just toggling the boolean
        self.tk.attributes("-fullscreen", self.state)
        return "break"

    def end_fullscreen(self, event=None):
        self.state = False
        self.tk.attributes("-fullscreen", False)
        return "break"

if __name__ == '__main__':
    bot = telepot.aio.Bot("682185822:AAGz6IhOj-cJM0n5M3m6nZlOstjM9kluY0M")
    loop = asyncio.get_event_loop()
    async_loop = asyncio.get_event_loop()
    w = FullscreenWindow(async_loop, loop, bot)
