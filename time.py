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
        self.allStringLb1 = Label(self, text =(self.day_of_week1, self.date1), font=('DIN Next CYR UltraLight', small_text_size), fg="white", bg="black")
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
        self.topFrame = Frame(self.tk, background = 'black')
        self.bottomFrame = Frame(self.tk, background = 'black')
        self.topFrame.pack(side = TOP, fill=BOTH, expand = YES)
        self.bottomFrame.pack(side = BOTTOM, fill=BOTH, expand = YES)
        self.state = False
        self.tk.bind("<Return>", self.toggle_fullscreen)
        self.tk.bind("<Escape>", self.end_fullscreen)
        # clock
        self.clock = Clock(self.topFrame)
        self.clock.pack(side=LEFT, anchor=NW, padx=60, pady=10)
   

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
