#!/usr/bin/env python
import Tkinter as tkinter

from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure

import numpy as np

from Measurement import Measurement
from Fmi import Fmi
from Extdev import Extdev
from RaspberryPinout import RaspberryPinout

import matplotlib.dates as md
from datetime import datetime, timedelta

root = tkinter.Tk()
root.wm_title("Tuuli")
root.attributes("-fullscreen", True)

var = tkinter.StringVar()
label = tkinter.Label( master=root, textvariable=var, relief="raised" )

observationList = ["","Harmaja","Kumpula","Vuosaari","Laru"]
observationVar = tkinter.StringVar(root)
observationVar.set(observationList[0])
observationOpt = tkinter.OptionMenu(root, observationVar, *observationList)
observationOpt.config(width=10, font=('Helvetica', 12))
raspberryPinout = RaspberryPinout()

fmilist = [
Fmi('Harmaja','r','100996'),
Fmi('Kumpula','c','101004'),
Fmi('Vuosaari','g','151028'),
Extdev('Laru','b')];

setup={'ha': 'center', 'va': 'center', 'bbox': {'fc': '0.8', 'pad': 0}}

def loadandredraw():
    ax=fig.gca()
    xfmt = md.DateFormatter('%H:%M')
    ax.xaxis.set_major_formatter(xfmt)
    
    starttime = datetime.now()-timedelta(hours=3)
    endtime = datetime.now()
    
    count = 0
    for fmi in fmilist:
        var.set('Lataus '+str(count)+'%')
        root.update_idletasks()
        fmi.read(starttime,endtime)
        abc.plot(fmi.aika,fmi.nopeus,fmi.color,label=fmi.place)
        count += 25

    counts = len(fmilist[0].aika)-1
    for i in range(counts, 0, -counts/12):
       abc.text(fmilist[0].aika[i], int(fmilist[0].nopeus[i])+1, str(fmilist[0].kulma[i])+'->', setup, rotation=(270-fmilist[0].kulma[i]))
    
    abc.grid(True)
    abc.legend()
    var.set(endtime.strftime(" %H:%M "))
    index = observationList.index(observationVar.get())-1
    if index > -1:
       cnt = len(fmilist[index].aika)-1
       raspberryPinout.writeToGpio(fmilist[index].nopeus[cnt],fmilist[index].kulma[cnt])

fig = Figure(figsize=(6, 4), dpi=100)
abc = fig.add_subplot(111)

loadandredraw()

canvas = FigureCanvasTkAgg(fig, master=root)
canvas.draw()
canvas.get_tk_widget().pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=1)

toolbar = NavigationToolbar2Tk(canvas, root)
toolbar.update()
canvas.get_tk_widget().pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=1)

def _quit():
    root.quit()
    root.destroy()

def repaintall():
    abc.clear()
    loadandredraw()
    canvas.draw()

timer = fig.canvas.new_timer(interval=300000) # 5 min
timer.add_callback(repaintall)
def toggle():
    if toggle_btn.config('relief')[-1] == 'sunken':
        toggle_btn.config(relief="raised")
        timer.stop()
    else:
        toggle_btn.config(relief="sunken")
        timer.start()

button = tkinter.Button(master=root, text="Lopeta", command=_quit)
button.pack(side=tkinter.LEFT)

button2 = tkinter.Button(master=root, text="Lataa", command=repaintall)
button2.pack(side=tkinter.LEFT)

toggle_btn = tkinter.Button(text="Paivitys", width=12, relief="raised", command=toggle)
toggle_btn.pack(side=tkinter.LEFT)

label.pack(side=tkinter.LEFT)

observationOpt.pack(side=tkinter.LEFT)

tkinter.mainloop()
