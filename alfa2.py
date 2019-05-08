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
    temp = []
    i = 0
    while i < 5:
        temp.append(" ")
        i = i+1
    with open(day, "r") as f:
        i = 0
        for line in f.readlines():
            temp[i] = line
            i = i+1
    return temp
def setNote(day, note):
	with open(day, "w") as f:
		f.write(note)


	
ui_locale = '' # e.g. 'fr_FR' fro French, '' as default
time_format = 24 # 12 or 24
date_format = "%b %d, %Y" # check python doc for strftime() for options
xlarge_text_size = 94
large_text_size = 48
medium_text_size = 28
small_text_size = 18
TOKEN = "682185822:AAGz6IhOj-cJM0n5M3m6nZlOstjM9kluY0M"
chat_allow1 = 148545016
chat_allow2 = 885204760
message_with_inline_keyboard = None
id_write_critical_temper = 0
icon_lookup_day = {
	'ясно': "c:\\users\\123\\pictures\weather_day/sun.png",   
	'облачно': "c:\\users\\123\\pictures\weather_day/cloudy.png",
	'слегка облачно': "c:\\users\\123\\pictures\weather_day/partialy-cloudy.png",
	'пасмурно': "c:\\users\\123\\pictures\weather_day/overcast-day.png",  
	'дождь': "c:\\users\\123\\pictures\weather_day/rainy-day.png",  
	'снег': "c:\\users\\123\\pictures\weather_day/snow.png", 
	'снег с дождем': "c:\\users\\123\\pictures\weather_day/sleet.png",    
}

icon_lookup_night = {
	'ясно': "c:\\users\\123\\pictures\weather_night/moon.png",    
	'облачно': "c:\\users\\123\\pictures\weather_night/partialy-cloudy.png",
	'слегка облачно': "c:\\users\\123\\pictures\weather_day/partialy-cloudy.png",
	'пасмурно': "c:\\users\\123\\pictures\weather_night/overcast-day.png",  
	'дождь': "c:\\users\\123\\pictures\weather_night/rainy-day.png",  
	'снег': "c:\\users\\123\\pictures\weather_night/snow.png",  
	'снег с дождем': "c:\\users\\123\\pictures\weather_night/sleet.png",  
}

class Weather(Frame):
	def __init__(self, parent, *args, **kwargs):
		Frame.__init__(self, parent, bg='black')
		self.city = "Санкт-Петербург"
		self.app = "42dfb1b3420a987588771d0dc21cf225"
		self.temperature = ''
		#self.forecast = ''
		#self.location = ''
		self.weather_info = ''
		
		self.degreeFrm = Frame(self, bg="black")
		self.degreeFrm.pack(side=RIGHT, anchor=N)
		
		self.iconLb1 = Label(self, bg="black")
		self.iconLb1.pack(side=LEFT, anchor=W, padx=20)

		self.wthrLbl = Label(self, font=('Helvetica', large_text_size), fg="white", bg="black")
		self.wthrLbl.pack(side=BOTTOM, anchor=W, padx=20)

		self.temperatureLbl = Label(self, font=('Helvetica', xlarge_text_size), fg="white", bg="black")
		self.temperatureLbl.pack(side=BOTTOM, anchor=W)

		self.cityLB1 = Label(self, font=('Helvetica', medium_text_size), fg = 'white', bg='black')
		self.cityLB1.pack(side = BOTTOM, anchor = W, padx = 30)        

		#self.forecastLbl = Label(self, font=('Helvetica', small_text_size), fg="white", bg="black")
		#self.forecastLbl.pack(side=TOP, anchor=W)

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
		
		s_city = self.city
		fileCity = readCityForWeather()
		city_id = self.get_ip(fileCity)
		appid = self.app
		
		try:

			degree_sign= u'\N{DEGREE SIGN}'
			r = requests.get("http://api.openweathermap.org/data/2.5/weather", params={'id': city_id, 'units': 'metric', 'lang': 'ru', 'APPID': appid})
			data = r.json()
			wthr = data['weather'][0]['description']
			temp1 = data['main']['temp']
			temp1 = round(temp1)
			temp1 = str(temp1)
			temp = (temp1 + degree_sign)

			weather_info2 = wthr
			icon_id = wthr

			time_inf = Clock(self)
			timing = time_inf.time1
			a = timing.split(':')
			hours = a[1]
			hours = int(hours)
			#tempcity = self.city
			tempcity = fileCity
			self.cityLB1.config(text=tempcity)

			if hours < 8 and hours >= 20:
				if icon_id in icon_lookup_day:
					icon = icon_lookup_day[icon_id]
					image = Image.open(icon)
					image = image.resize((220, 220), Image.ANTIALIAS)
					photo = ImageTk.PhotoImage(image)
					self.iconLb1.image = photo
					self.iconLb1.config(image = photo)
				else:
					# remove image
					self.iconLbl.config(image='')
				
 
			else:
				if icon_id in icon_lookup_night:
					icon = icon_lookup_night[icon_id]
					image = Image.open(icon)
					image = image.resize((220, 220), Image.ANTIALIAS)
					photo = ImageTk.PhotoImage(image)
					self.iconLb1.image = photo
					self.iconLb1.config(image = photo)
				else:
					# remove image
					self.iconLb1.config(image='')

			if weather_info2 is not None:
				if self.weather_info != weather_info2:
					self.weather_info = weather_info2
					self.wthrLbl.config(text=weather_info2)

			if self.temperature != temp:
				self.temperature = temp
				self.temperatureLbl.config(text=temp)

				
		except Exception as e:
			traceback.print_exc()
			print ("Error: %s. Cannot get weather." %e)

		self.after(500, self.get_weather)
class Notes(Frame):
        def __init__(self, parent, *args, **kwargs):
                Frame.__init__(self, parent, bg = 'black')
                self.note1 = ''
                self.note2 = ''
                self.note3 = ''
                self.note4 = ''
                self.note5 = ''
                self.note1Lb = Label(self, text=(self.note1), font=('Helvetica', medium_text_size), fg = "white", bg = "black")
                self.note1Lb.pack(side=TOP, anchor = CENTER)
                self.note2Lb = Label(self, text=(self.note2), font=('Helvetica', medium_text_size), fg = "white", bg = "black")
                self.note2Lb.pack(side=TOP, anchor = CENTER)
                self.note3Lb = Label(self, text=(self.note3), font=('Helvetica', medium_text_size), fg = "white", bg = "black")
                self.note3Lb.pack(side=TOP, anchor = CENTER)
                self.note4Lb = Label(self, text=(self.note4), font=('Helvetica', medium_text_size), fg = "white", bg = "black")
                self.note4Lb.pack(side=TOP, anchor = CENTER)
                self.note5Lb = Label(self, text=(self.note5), font=('Helvetica', medium_text_size), fg = "white", bg = "black")
                self.note5Lb.pack(side=TOP, anchor = CENTER)
                self.getUpdNotes()
                
        def getUpdNotes(self):
                TextNote = []
                i = 0
                while i < 5:
                    TextNote.append(" ")
                    i = i+1
                day_of_week = time.strftime('%A')
                if day_of_week == 'понедельник':
                    TextNote = readNotes('Monday.txt')
                elif day_of_week == 'вторник':
                    TextNote = readNotes('Tuesday.txt')
                elif day_of_week == 'среда':
                    TextNote = readNotes('Wednesday.txt')
                elif day_of_week == 'четверг':
                    TextNote = readNotes('Thursday.txt')
                elif day_of_week == 'пятница':
                    TextNote = readNotes('Friday.txt')
                elif day_of_week == 'суббота':
                    TextNote = readNotes('Saturday.txt')
                elif day_of_week == 'воскресенье':
                    TextNote = readNotes('Sunday.txt')

                oldNote = self.note1
                if oldNote != TextNote[0]:
                    self.note1 = TextNote[0]
                    self.note1Lb.config(text = TextNote[0])
                    self.after(200, self.getUpdNotes)
    
                oldNote = self.note2
                if oldNote != TextNote[1]:
                    self.note1 = TextNote[1]
                    self.note1Lb.config(text = TextNote[1])
                    self.after(200, self.getUpdNotes)

                oldNote = self.note3
                if oldNote != TextNote[2]:
                    self.note1 = TextNote[2]
                    self.note1Lb.config(text = TextNote[2])
                    self.after(200, self.getUpdNotes)

                oldNote = self.note4
                if oldNote != TextNote[3]:
                    self.note1 = TextNote[3]
                    self.note1Lb.config(text = TextNote[3])
                    self.after(200, self.getUpdNotes)

                oldNote = self.note5
                if oldNote != TextNote[4]:
                    self.note1 = TextNote[4]
                    self.note1Lb.config(text = TextNote[4])
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
		self.allStringLb1 = Label(self, text =(self.day_of_week1, self.date1), font=('DIN Next CYR UltraLight', small_text_size), fg="white", bg="black")
		self.allStringLb1.pack(side=TOP, anchor=CENTER)
		self.tick()

	def tick(self):
		tz = readTimeZone()
		utc_time = datetime.utcnow()
		temp_tz = pytz.timezone(tz)
		utc_time =utc_time.replace(tzinfo=pytz.UTC)
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
                        ok=1
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
#def on_chat_message(msg):
	global id_write_critical_temper
	content_type, chat_type, chat_id = telepot.glance(msg)
	print('Chat:', content_type, chat_type)
	print("id отправителя сообщения: "+str(chat_id))
	if chat_id == chat_allow1 or chat_id == chat_allow2:
		if content_type != 'text':
			return
		else:
			ok=1
		command = msg['text'].lower()
		print(command)
 
		if command == '/start':
			markup = ReplyKeyboardMarkup(keyboard=[
			[dict(text='сменить часовой пояс')],
			[dict(text='сменить город')],
			[dict(text='добавить заметку')],
			])
			await bot.sendMessage(chat_id, 'чем воспользуешься?', reply_markup=markup)
		
		elif command == 'главное меню':
			markup = ReplyKeyboardMarkup(keyboard=[
			[dict(text='сменить часовой пояс')],
			[dict(text='сменить город')],
			[dict(text='добавить заметку')],
			])
			await bot.sendMessage(chat_id, 'выбери раздел', reply_markup=markup)
	
		elif command == u'сменить часовой пояс':
			markup = ReplyKeyboardMarkup(keyboard=[
			[dict(text='MSK(GMT+4)'), dict(text='YEKT (GMT+06)')],
			[dict(text='OMST(GMT+07)')],
			[dict(text='главное меню')],
			])
			await bot.sendMessage(chat_id, 'выбери время', reply_markup=markup)
		
		elif command == u'сменить город':
			markup = ReplyKeyboardMarkup(keyboard=[
			[dict(text='Москва'), dict(text='Санкт-Петербург')],
			[dict(text='Новосибирск'), dict(text='Екатеринбург')],
			[dict(text = 'Нижний Новгород'), dict(text='Казань')],
			[dict(text = 'Уфа'), dict(text='Омск')],
			[dict(text='главное меню')],
			])
			await bot.sendMessage(chat_id, 'Выбери город', reply_markup=markup)
		
		elif command == u'добавить заметку':
			markup = ReplyKeyboardMarkup(keyboard=[])
			[dict(text='Понедельник'), dict(text='Вторник')],
			[dict(text='Среда'), dict(text='Четверг')],
			[dict(text='Пятница'), dict(text='Суббота')],
			[dict(text='Воскресенье')],
			await bot.sendMessage(chat_id, 'Выбирай день, лох', reply_markup=markup)
			#await bot({'chat':set_notes}) 
		elif command == u'omst(gmt+07)':
			markup = ReplyKeyboardMarkup(keyboard=[
			[dict(text='сменить часовой пояс')],
			[dict(text='сменить город')],
			[dict(text='добавить заметку')],
			])
			R = str(readTimeZone())
			setTimeZone('Etc/GMT-6')
			await bot.sendMessage(chat_id, 'Меняю время, аббажи чуток, парень. Было %s, стало Europe/Omsk.' %R,  reply_markup=markup)
		elif command == u'yekt (gmt+06)':
			markup = ReplyKeyboardMarkup(keyboard=[
			[dict(text='сменить часовой пояс')],
			[dict(text='сменить город')],
			[dict(text='добавить заметку')],
			])
			R = str(readTimeZone())
			setTimeZone('Etc/GMT-5')
			await bot.sendMessage(chat_id, 'Меняю время, аббажи чуток, парень. Было %s, стало Europe/YEKT.' %R,  reply_markup=markup)
		elif command == u'msk(gmt+4)':
			markup = ReplyKeyboardMarkup(keyboard=[
			[dict(text='сменить часовой пояс')],
			[dict(text='сменить город')],
			[dict(text='добавить заметку')],
			])
			R = str(readTimeZone())
			setTimeZone('Etc/GMT-3')
			await bot.sendMessage(chat_id, 'Меняю время, аббажи чуток, парень. Было %s, стало Europe/MSK.' %R,  reply_markup=markup)
		elif command == u'москва':
			markup = ReplyKeyboardMarkup(keyboard=[
			[dict(text='сменить часовой пояс')],
			[dict(text='сменить город')],
			[dict(text='добавить заметку')],
			])
			setCityForWeather('Москва')
			await bot.sendMessage(chat_id, 'Поменял город, проверяй, eblan',  reply_markup=markup)
		elif command == u'Нижний Новгород':
			markup = ReplyKeyboardMarkup(keyboard=[
			[dict(text='сменить часовой пояс')],
			[dict(text='сменить город')],
			[dict(text='добавить заметку')],
			])
			setCityForWeather('Нижний Новгородо')
			await bot.sendMessage(chat_id, 'Поменял город, проверяй, eblan',  reply_markup=markup)
		elif command == u'уфа':
			markup = ReplyKeyboardMarkup(keyboard=[
			[dict(text='сменить часовой пояс')],
			[dict(text='сменить город')],
			[dict(text='добавить заметку')],
			])
			setCityForWeather('Уфа')
			await bot.sendMessage(chat_id, 'Поменял город, проверяй, eblan',  reply_markup=markup)
		elif command == u'омск':
			markup = ReplyKeyboardMarkup(keyboard=[
			[dict(text='сменить часовой пояс')],
			[dict(text='сменить город')],
			[dict(text='добавить заметку')],
			])
			setCityForWeather('Омск')
			await bot.sendMessage(chat_id, 'Поменял город, проверяй, eblan',  reply_markup=markup)
		elif command == u'казань':
			markup = ReplyKeyboardMarkup(keyboard=[
			[dict(text='сменить часовой пояс')],
			[dict(text='сменить город')],
			[dict(text='добавить заметку')],
			])
			setCityForWeather('Казань')
			await bot.sendMessage(chat_id, 'Поменял город, проверяй, eblan',  reply_markup=markup)
		elif command == 'понедельник':
			#setNote('Monday.txt', command)
			markup = ReplyKeyboardMarkup(keyboard=[
			[dict(text='сменить часовой пояс')],
			[dict(text='сменить город')],
			[dict(text='добавить заметку')],
			])
			await bot.sendMessage(chat_id, 'Pishi zametku, loh',  reply_markup=markup)
			await bot({'chat':set_notes('Понедельник')}) 
			await bot.sendMessage(chat_id, 'Сделал заметку, чекай, лох',  reply_markup=markup)
						
					
 
		
 
	else:
		#если чат айди не соответствует разрешенному
		markup_protect = ReplyKeyboardMarkup(keyboard=[[dict(text='я очень тугой, еще раз можно?')]])
		await bot.sendMessage(chat_id, 'Вы не имеете доступа к этому боту! Обратитесь к владельцу за разрешением.', reply_markup=markup_protect)
		return
####### Thread ####### 
def run_tgBot(async_loop, loop, bot):
	threading.Thread(target=tgBot_thread, args=(async_loop, loop, bot,)).start()
def tgBot_thread(async_loop, loop, bot):
	asyncio.set_event_loop(loop)
	loop.run_until_complete(bot.message_loop({'chat': on_chat_message}))
	
class FullscreenWindow:

	def __init__(self, async_loop, loop, bot):
		self.tk = Tk()
		self.tk.configure(background='black')
		self.topFrame = Frame(self.tk, background = 'black')
		self.bottomFrame = Frame(self.tk, background = 'black')
		self.topFrame.pack(side = TOP, fill=BOTH, expand = YES)
		self.bottomFrame.pack(side = BOTTOM, fill=BOTH, expand = YES)
		self.state = False
		self.tk.bind("<Return>", self.toggle_fullscreen)
		self.tk.bind("<Escape>", self.end_fullscreen)
		# clock
		self.clock = Clock(self.topFrame, 3)
		self.clock.pack(side=LEFT, anchor=NW, padx=60, pady=10)
		# weather
		self.weather = Weather(self.topFrame)
		self.weather.pack(anchor=NW, padx=60, pady=50)
		#Notes
		self.Notes = Notes(self.topFrame)
		self.Notes.pack(side = LEFT, anchor = NW, padx = 40, pady = 10)
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
	
	
