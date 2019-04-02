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
icon_lookup = {
    'clear-day': "assets/Sun.png",  # clear sky day
    'wind': "assets/Wind.png",   #wind
    'cloudy': "assets/Cloud.png",  # cloudy day
    'partly-cloudy-day': "assets/PartlySunny.png",  # partly cloudy day
    'rain': "assets/Rain.png",  # rain day
    'snow': "assets/Snow.png",  # snow day
    'snow-thin': "assets/Snow.png",  # sleet day
    'fog': "assets/Haze.png",  # fog day
    'clear-night': "assets/Moon.png",  # clear sky night
    'partly-cloudy-night': "assets/PartlyMoon.png",  # scattered clouds night
    'thunderstorm': "assets/Storm.png",  # thunderstorm
    'tornado': "assests/Tornado.png",    # tornado
    'hail': "assests/Hail.png"  # hail
}

class Weather(Frame):
    def __init__(self, parent, *args, **kwargs):
        Frame.__init__(self, parent, bg='black')
        self.temperature = ''
        #self.forecast = ''
        #self.location = ''
        #self.currently = ''
        self.icon = ''
        self.degreeFrm = Frame(self, bg="black")
        self.degreeFrm.pack(side=RIGHT, anchor=N)
        self.temperatureLbl = Label(self.degreeFrm, font=('Helvetica', xlarge_text_size), fg="white", bg="black")
        self.temperatureLbl.pack(side=LEFT, anchor=W)
        #self.iconLbl = Label(self.degreeFrm, bg="black")
        self.iconLbl = Label(self, font=('Helvetica', large_text_size), fg="white", bg="black")
        self.iconLbl.pack(side=LEFT, anchor=W, padx=20)
        #self.currentlyLbl = Label(self, font=('Helvetica', medium_text_size), fg="white", bg="black")
        #self.currentlyLbl.pack(side=TOP, anchor=W)
        #self.forecastLbl = Label(self, font=('Helvetica', small_text_size), fg="white", bg="black")
        #self.forecastLbl.pack(side=TOP, anchor=W)
        #self.locationLbl = Label(self, font=('Helvetica', small_text_size), fg="white", bg="black")
        #self.locationLbl.pack(side=TOP, anchor=W)
        self.get_weather()

    #def get_ip(self):
        #try:
            #ip_url = "http://jsonip.com/"
            #req = requests.get(ip_url)
            #ip_json = json.loads(req.text)
            #return ip_json['ip']
        #except Exception as e:
            #traceback.print_exc()
            #return ("Error: %s. Cannot get ip." %e)

    def get_weather(self):
        
        s_city = "Saint Petersburg"
        city_id = 498817
        appid = "42dfb1b3420a987588771d0dc21cf225"
        
        try:

            #if latitude is None and longitude is None:
                # get location
                #location_req_url = "http://freegeoip.net/json/%s" % self.get_ip()
                #r = requests.get(location_req_url)
                #location_obj = json.loads(r.text)

                #lat = location_obj['latitude']
                #lon = location_obj['longitude']

                #location2 = "%s, %s" % (location_obj['city'], location_obj['region_code'])

                # get weather
                #weather_req_url = "https://api.darksky.net/forecast/%s/%s,%s?lang=%s&units=%s" % (weather_api_token, lat,lon,weather_lang,weather_unit)
            #else:
                #location2 = ""
                # get weather
                #weather_req_url = "https://api.darksky.net/forecast/%s/%s,%s?lang=%s&units=%s" % (weather_api_token, latitude, longitude, weather_lang, weather_unit)

            degree_sign= u'\N{DEGREE SIGN}'
            r = requests.get("http://api.openweathermap.org/data/2.5/weather", params={'id': city_id, 'units': 'metric', 'lang': 'ru', 'APPID': appid})
            data = r.json()
            wthr = data['weather'][0]['description']
            temp = data['main']['temp']
            temp = round(temp)
            temp = (temp, degree_sign)
            #weather_obj = json.loads(r.text)

            #temperature2 = "%s%s" % (str(int(weather_obj['currently']['temperature'])), degree_sign)
            #currently2 = weather_obj['currently']['summary']
            #forecast2 = weather_obj["hourly"]["summary"]

            #icon_id = weather_obj['currently']['icon']
            #icon2 = None
            icon2 = wthr

            #if icon_id in icon_lookup:
                #icon2 = icon_lookup[icon_id]

            if icon2 is not None:
                if self.icon != icon2:
                    self.icon = icon2
                    #image = Image.open(icon2)
                    #image = image.resize((100, 100), Image.ANTIALIAS)
                    #image = image.convert('RGB')
                    #photo = ImageTk.PhotoImage(image)

                    self.iconLbl.config(text=icon2)
                    #self.iconLbl.image = photo
            #else:
                # remove image
                #self.iconLbl.config(image='')

            #if self.currently != temp:
                #self.currently = temp
                #self.currentlyLbl.config(text=temp)
            #if self.forecast != forecast2:
                #self.forecast = forecast2
                #self.forecastLbl.config(text=forecast2)
            if self.temperature != temp:
                self.temperature = temp
                self.temperatureLbl.config(text=temp)
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
