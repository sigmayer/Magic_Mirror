import datetime
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
from contextlib import contextmanager
from PIL import Image, ImageTk
LOCALE_LOCK = threading.Lock()

@contextmanager
def setlocale(name): #thread proof function to work with locale
    with LOCALE_LOCK:
        saved = locale.setlocale(locale.LC_ALL)
        try:
            yield locale.setlocale(locale.LC_ALL, name)
        finally:
            locale.setlocale(locale.LC_ALL, saved)
            
ui_locale = '' # e.g. 'fr_FR' fro French, '' as default
time_format = 24 # 12 or 24
date_format = "%b %d, %Y" # check python doc for strftime() for options
xlarge_text_size = 94
large_text_size = 48
medium_text_size = 28
small_text_size = 18

# maps open weather icons to
# icon reading is not impacted by the 'lang' parameter
icon_lookup_day = {
    'ясно': "c:\\users\\123\\pictures\\weather_day\\sun.png", 
    'wind': "assets/Wind.png",   
    'облачно': "c:\\users\\123\\pictures\\weather_day\\cloudy.png",
    'слегка облачно': "c:\\users\\123\\pictures\\weather_day\\partialy-cloudy.png",
    'пасмурно': "c:\\users\\123\\pictures\\weather_day\\overcast-day.png",  
    'дождь': "c:\\users\\123\\pictures\\weather_day\\rainy-day.png",  
    'снег': "c:\\users\\123\\pictures\\weather_day\\snow.png", 
    'снег с дождем': "c:\\users\\123\\pictures\\weather_day\\sleet.png",  
    'fog': "assets/Haze.png", 
    'clear-night': "assets/Moon.png",  
    'partly-cloudy-night': "assets/PartlyMoon.png",  
    'thunderstorm': "assets/Storm.png",  
    'tornado': "assests/Tornado.png",    
    'hail': "assests/Hail.png"  
}

icon_lookup_night = {
    'ясно': "c:\\users\\123\\pictures\\weather_night\\moon.png",  
    'wind': "assets/Wind.png",  
    'облачно': "c:\\users\\123\\pictures\\weather_night\\partialy-cloudy.png",
    'слегка облачно': "c:\\users\\123\\pictures\\weather_day\\partialy-cloudy.png",
    'пасмурно': "c:\\users\\123\\pictures\\weather_night\\overcast-day.png",  
    'дождь': "c:\\users\\123\\pictures\\weather_night\\rainy-day.png",  
    'снег': "c:\\users\\123\\pictures\\weather_night\\snow.png",  
    'снег с дождем': "c:\\users\\123\\pictures\\weather_night\\sleet.png",  
    'fog': "assets/Haze.png", 
    'clear-night': "assets/Moon.png",  
    'partly-cloudy-night': "assets/PartlyMoon.png",  
    'thunderstorm': "assets/Storm.png",  
    'tornado': "assests/Tornado.png",    
    'hail': "assests/Hail.png"  
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

        #self.forecastLbl = Label(self, font=('Helvetica', small_text_size), fg="white", bg="black")
        #self.forecastLbl.pack(side=TOP, anchor=W)

        self.get_ip()
        self.get_weather()

    def get_ip(self):

        s_city = self.city
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
        city_id = self.get_ip()
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

            #if self.forecast != forecast2:
                #self.forecast = forecast2
                #self.forecastLbl.config(text=forecast2)
                
            #if self.location != location2:
                #if location2 == ", ":
                    #self.location = "Cannot Pinpoint Location"
                    #self.locationLbl.config(text="Cannot Pinpoint Location")
                #else:
                    #self.location = location2
                    #self.locationLbl.config(text=location2)
                
        except Exception as e:
            traceback.print_exc()
            print ("Error: %s. Cannot get weather." %e)

        self.after(600000, self.get_weather)

class Clock(Frame):
    def __init__(self, parent, *args, **kwargs):
        Frame.__init__(self, parent, bg='black')
        # initialize time label
        self.time1 = ''
        self.timeLbl = Label(self, font=('DIN Next CYR UltraLight', xlarge_text_size), fg="white", bg="black")
        self.timeLbl.pack(side=TOP, anchor=CENTER)
        # initialize day of week
        self.day_of_week1 = ''
        #self.dayOWLbl = Label(self, text=self.day_of_week1, font=('DIN Next CYR UltraLight', small_text_size), fg="white", bg="black")
        #self.dayOWLbl.pack(side=TOP, anchor=E)
        # initialize date label
        self.date1 = ''
        #self.dateLbl = Label(self, text=self.date1, font=('DIN Next CYR UltraLight', small_text_size), fg="white", bg="black")
        #self.dateLbl.pack(side=TOP, anchor=E)
        #self.tick()
        #for string, like dayOfTheWeek, date
        self.allString1 = ''
        self.allStringLb1 = Label(self, text =(self.day_of_week1, self.date1), font=('DIN Next CYR UltraLight', medium_text_size), fg="white", bg="black") #!ИЗМЕНИЛ РАЗМЕР ШРИФТА НА MEDIUM!
        self.allStringLb1.pack(side=TOP, anchor=CENTER)
        self.tick()

    def tick(self):
        with setlocale(ui_locale):
            if time_format == 12:
                time2 = time.strftime('%I:%M %p') #hour in 12h format
            else:
                time2 = time.strftime('%H:%M') #hour in 24h format

            day_of_week2 = time.strftime('%A')
            date2 = time.strftime("%d.%m")
            # if time string has changed, update it
            if time2 != self.time1:
                self.time1 = time2
                self.timeLbl.config(text=time2)
            if day_of_week2 != self.day_of_week1:
                self.day_of_week1 = day_of_week2
                #self.dayOWLbl.config(text=day_of_week2)
                self.allStringLb1.config(text=(day_of_week2,',', self.date1))
            if date2 != self.date1:
                self.date1 = date2
                #self.dateLbl.config(text=date2)
                self.allStringLb1.config(text=(self.day_of_week1,',', date2))                         
            # calls itself every 200 milliseconds
            # to update the time display as needed
            # could use >200 ms, but display gets jerky
            self.timeLbl.after(200, self.tick)

class FullscreenWindow:

    def __init__(self):
        self.tk = Tk()
        self.tk.configure(background='black')
        self.tk.geometry('1366x768')                                            #!РАЗРЕШЕНИЕ ОКНА! 
        self.topFrame = Frame(self.tk, background = 'black')
        self.bottomFrame = Frame(self.tk, background = 'black')
        self.topFrame.pack(side = TOP, fill=BOTH, expand = YES)
        self.bottomFrame.pack(side = BOTTOM, fill=BOTH, expand = YES)
        self.state = False
        self.tk.bind("<Return>", self.toggle_fullscreen)
        self.tk.bind("<Escape>", self.end_fullscreen)
        # clock
        self.clock = Clock(self.topFrame)
        #self.clock.pack(side=LEFT, anchor=NW, padx=60, pady=10)                !СТАРЫЕ НАСТРОЙКИ РАСПОЛОЖЕНИЯ!
        self.clock.pack(anchor=NW, padx=60, pady=10)
        # weather
        self.weather = Weather(self.topFrame)
        #self.weather.pack(side=LEFT, anchor=N, padx=100, pady=60)              !СТАРЫЕ НАСТРОЙКИ РАСПОЛОЖЕНИЯ!
        self.weather.pack(anchor=NW, padx=60, pady=50)

    def toggle_fullscreen(self, event=None):
        self.state = not self.state  # Just toggling the boolean
        self.tk.attributes("-fullscreen", self.state)
        return "break"

    def end_fullscreen(self, event=None):
        self.state = False
        self.tk.attributes("-fullscreen", False)
        return "break"

if __name__ == '__main__':
    w = FullscreenWindow()
    w.tk.mainloop()
