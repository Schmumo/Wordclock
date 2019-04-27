# coding: utf8

#V24. Anleitung hinzugefügt, kleine Bugfixes, Wiederholungen bei Textanzeige, Eingabe Morgenzeit. Knöpfe deaktiviert.
#V25. Snakebug behoben, Pokal und Herz eingefügt, weitere Einstellungen zu Tag- und Nachtmodus eingebaut.
#V30. ConfigFile hinzugefügt
#V31. Rainbow hinzugefügt, Matrix neu gemacht
#V32. GUI überarbeitet, Slider nun direkter Farbwechsel, Preset-Button entfernt.
#V33. Circle und Binär-Uhr hinzugefügt. Uhr ausschalten hinzugefügt.
#V34. Easteregg. Code neu strukturiert.
#V35. Tetris hinzugefügt
#V36. Space Invaders hinzugefügt
#V37. Tetris und Space Invaders jetzt stabil und vollständig.
#V372. Tetris bunt und pausieren mit Leertaste
#V373. Tetris zeigt nun in den Ecken den nächsten Block an
#V38. Pacman hinzugefügt

from tkColorChooser import askcolor
import tkMessageBox
import ttk
import time
import thread
from neopixel import *
from Tkinter import *
import sys
import datetime
import RPi.GPIO as GPIO
import copy
import random
import ConfigParser
from TetrisClass import *
#from TetrisClass import QBlock

LED_COUNT = 114
LED_PIN = 18
LED_FREQ_HZ = 800000
LED_DMA = 10
LED_BRIGHTNESS = 255
LED_INVERT = False
LED_CHANNEL = 0
BLACK = Color(0, 0, 0)
BUTTONCHANGE = 17
BUTTONDIMM = 22
BUTTONDIMMALL = 24
global hour
global minute
global arrayLEDs
BITMASK_RED = 65280
BITMASK_GREEN = 16711680
BITMASK_BLUE = 255

###GRUNDLEGENDE FUNKTIONEN FÜR DAS HAUPTPROGRAMM###

#Bildet die Nummern der LEDs auf eine 10x11-Matrix ab
def buildMatrix():
    global matrix
    matrix = [[12,11,10,9,8,7,6,5,4,3,2],[13,14,15,16,17,18,19,20,21,22,23],[34,33,32,31,30,29,28,27,26,25,24],[35,36,37,38,39,40,41,42,43,44,45],
          [56,55,54,53,52,51,50,49,48,47,46],[57,58,59,60,61,62,63,64,65,66,67],[78,77,76,75,74,73,72,71,70,69,68],[79,80,81,82,83,84,85,86,87,88,89],
          [100,99,98,97,96,95,94,93,92,91,90],[101,102,103,104,105,106,107,108,109,110,111]]

#Erstellt die Liste mit den voreingestellten Farben
def preset():
    global COLOR
    global COLORCOPY
    global COLORS
    COLORS = []
    global preset
    preset = ["0-Rot", "1-Dunkelorange", "2-Orange", "3-Gelb", "4-Hellgrün", "5-Grün", "6-Cyan", "7-Blau", "8-Dunkelblau", "9-Dunkellila", "10-Helllila", "11-Weiß"]
    #Hier können neue Farben hinzugefügt werden. Einfach beliebig oft die Zeile "COLORS.append" kopieren und Werte zwischen 0 und 255 einsetzen
    COLORS.append(Color(0,255,0)) #ROT
    COLORS.append(Color(25,255,0)) #DunkelORANGE
    COLORS.append(Color(90,255,0)) #ORANGE
    COLORS.append(Color(200,255,0)) #GELB
    COLORS.append(Color(255,100,0)) #HELLGRÜN
    COLORS.append(Color(255,0,0)) #GRÜN
    COLORS.append(Color(255,0,255)) #CYAN
    COLORS.append(Color(50,0,255)) #BLAU
    COLORS.append(Color(0,0,255)) #DUNKELBLAU    
    COLORS.append(Color(0,75,255)) #DUNKELLILA
    COLORS.append(Color(0,140,255)) #HELLLILA
    COLORS.append(Color(255,255,255)) #WEISS 
    
    return preset

#Berechnet die nötigen LEDs aus der Uhrzeit
def calculateArray(hour, minute):
    array = []
    
    if (minute % 5 == 4): array.extend((0, 1, 112, 113))
    elif (minute % 5 == 3): array.extend((0,1,112))
    elif (minute % 5 == 2): array.extend((0,1))
    elif (minute % 5 == 1): array.append(0)

    #Uhrzeit für normale Menschen
    if (varMystery.get() == 0):
        array.extend((12, 11, 9, 8, 7))
        if (minute < 5): array.extend((109,110,111)) #UHR
        elif (minute < 10): array.extend((5,4,3,2,37,38,39,40)) #FÜNF NACH
        elif (minute < 15): array.extend((13,14,15,16,37,38,39,40)) #ZEHN NACH
        elif (minute < 20) : array.extend((30,29,28,27,26,25,24,37,38,39,40)) #VIERTEL NACH
        elif (minute < 25): array.extend((17,18,19,20,21,22,23, 37,38,39,40)) #ZWANZIG NACH
        elif (minute < 30): array.extend((5,4,3,2,41,42,43,56,55,54,53)) #FÜNF VOR HALB
        elif (minute < 35): array.extend((56,55,54,53)) #HALB
        elif (minute < 40): array.extend((5,4,3,2,37,38,39,40,56,55,54,53)) #FÜNF NACH HALB
        elif (minute < 45): array.extend((17,18,19,20,21,22,23,41,42,43)) #ZWANZIG VOR
        elif (minute < 50): array.extend((30,29,28,27,26,25,24,41,42,43))#VIERTEL VOR
        elif (minute < 55): array.extend((13,14,15,16,41,42,43))#ZEHN VOR
        elif (minute < 60): array.extend((5,4,3,2,41,42,43))#FÜNF VOR
        if (minute >=25): hour = hour + 1

    #Uhrzeit für Schwaben
    elif (varMystery.get() == 1):
        array.extend((12, 11, 9, 8, 7))
        if (minute < 5): array.extend((109,110,111)) #UHR
        elif (minute < 10): array.extend((5,4,3,2,37,38,39,40)) #FÜNF NACH
        elif (minute < 15): array.extend((13,14,15,16,37,38,39,40)) #ZEHN NACH
        elif (minute < 20) : array.extend((30,29,28,27,26,25,24)) #VIERTEL
        elif (minute < 25): array.extend((17,18,19,20,21,22,23, 37,38,39,40)) #ZWANZIG NACH
        elif (minute < 30): array.extend((5,4,3,2,41,42,43,56,55,54,53)) #FÜNF VOR HALB
        elif (minute < 35): array.extend((56,55,54,53)) #HALB
        elif (minute < 40): array.extend((5,4,3,2,37,38,39,40,56,55,54,53)) #FÜNF NACH HALB
        elif (minute < 45): array.extend((17,18,19,20,21,22,23,41,42,43)) #ZWANZIG VOR
        elif (minute < 50): array.extend((34,33,32,31,30,29,28,27,26,25,24))#DREIVIERTEL
        elif (minute < 55): array.extend((13,14,15,16,41,42,43))#ZEHN VOR
        elif (minute < 60): array.extend((5,4,3,2,41,42,43))#FÜNF VOR
        if (minute >=25 or (minute >= 15 and minute < 20)): hour = hour + 1

    hour = hour % 12
    if ((hour == 1) and (minute < 5)): array.extend((59,60,61))
    elif ((hour == 1) and (minute >= 5)): array.extend((59,60,61,62))
    elif (hour == 2): array.extend((57,58,59,60))
    elif (hour == 3): array.extend((77,76,75,74))
    elif (hour == 4): array.extend((86,87,88,89))
    elif (hour == 5): array.extend((71,70,69,68))
    elif (hour == 6): array.extend((102,103,104,105,106))
    elif (hour == 7): array.extend((62,63,64,65,66,67))
    elif (hour == 8): array.extend((99,98,97,96))
    elif (hour == 9): array.extend((82,83,84,85))
    elif (hour == 10): array.extend((95,94,93,92))
    elif (hour == 11): array.extend((79,80,81))
    elif (hour == 0): array.extend((51,50,49,48,47))
    
    return array

#Berechnet die nötigen LEDs für die binäre Darstellung
def calculateArrayBinary(year, month, day, hour, minute, second):
    array = []

    arrayYear = binaryArray(year)
    for i in range(len(arrayYear)):
        array.append(matrix[0][arrayYear[i]])

    arrayMonth = binaryArray(month)
    for i in range(len(arrayMonth)):
        array.append(matrix[1][arrayMonth[i]])

    arrayDay = binaryArray(day)
    for i in range(len(arrayDay)):
        array.append(matrix[2][arrayDay[i]])

    arrayHour = binaryArray(hour)
    for i in range(len(arrayHour)):
        array.append(matrix[3][arrayHour[i]])

    arrayMinute = binaryArray(minute)
    for i in range(len(arrayMinute)):
        array.append(matrix[4][arrayMinute[i]])

    arraySecond = binaryArray(second)
    for i in range(len(arraySecond)):
        array.append(matrix[5][arraySecond[i]])
    
    return array

#Hilfsmethode zur binären Rechnung
def binaryArray(number):
    array = []
    if number >= 1024:
        array.append(0)
        number = number - 1024
    if number >= 512:
        array.append(1)
        number = number - 512
    if number >= 256:
        array.append(2)
        number = number - 256
    if number >= 128:
        array.append(3)
        number = number - 128
    if number >= 64:
        array.append(4)
        number = number - 64
    if number >= 32:
        array.append(5)
        number = number - 32
    if number >= 16:
        array.append(6)
        number = number - 16
    if number >= 8:
        array.append(7)
        number = number - 8
    if number >= 4:
        array.append(8)
        number = number - 4
    if number >= 2:
        array.append(9)
        number = number - 2
    if number >= 1:
        array.append(10)

    return array

#Setzt die LEDs des Arrays auf die gesetzte Farbe
def turnOnLEDs(strip, arrayLEDs):
    clear(strip)
    for i in range(len(arrayLEDs)):
        strip.setPixelColor(arrayLEDs[i], COLOR)
    strip.show()

#Schaltet alle LEDs aus
def clear(strip):
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, BLACK)

#Wird nach Spezialfunktionen aufgerufen. Setzt die normale Uhranzeige fort
def proceed(strip):
    ti = datetime.datetime.now()
    hour = ti.hour
    minute = ti.minute
    second = ti.second
    arrayLEDs = calculateArray(hour, minute)
    turnOnLEDs(strip, arrayLEDs)
    strColor = "Farbe: "+str((COLOR & BITMASK_RED) >> 8) +", "+ str((COLOR & BITMASK_GREEN) >> 16) +", "+ str(COLOR & BITMASK_BLUE)
    actualColor.config(text=strColor)

###FUNKTIONEN ZUM WÄHLEN DER FARBE###

#Farbe wird visuell gewählt.
def chooseVisual():
    result = askcolor(title="Farbe wählen", color=((2, 11, 97)))
    colors = result[0]
    global COLOR
    global COLORCOPY
    if colors != None:
        COLOR = Color(colors[1], colors[0], colors[2])
        COLORCOPY = Color(colors[1], colors[0], colors[2])
    proceed(strip)

#Farbe der Slider wird über den Button gesetzt
def chooseFromSliders():
    red = slider_red.get()
    green=slider_green.get()
    blue=slider_blue.get()
    global COLOR
    global COLORCOPY
    COLOR = Color(green, red, blue)
    COLORCOPY = Color(green, red, blue)
    proceed(strip)

#Farbe der Slider wird gesetzt, während einer der Slider verändert wird
def chooseFromSliders2(null):
    red = slider_red.get()
    green=slider_green.get()
    blue=slider_blue.get()
    global COLOR
    global COLORCOPY
    COLOR = Color(green, red, blue)
    COLORCOPY = Color(green, red, blue)
    proceed(strip)

#Farbe wird aus Presets gewählt.
def chooseFromPreset(null):
    var = variable.get()
    split = var.split('-')
    c = int(split[0])
    global COLORS
    global COLOR
    global COLORCOPY
    COLOR = COLORS[c]
    COLORCOPY = COLORS[c]
    proceed(strip)
    
#Farbe wird zufällig aus Presets gesetzt
def randomFromPreset():
    global COLORS
    global COLOR
    global COLORCOPY 
    COLOR = COLORS[random.randint(0,len(COLORS)-1)]
    COLORCOPY = COLOR
    proceed(strip)

#Farbe wird komplett zufällig gesetzt
def randomTotally():
    global COLOR
    global COLORCOPY 
    COLOR = Color(random.randint(0,255), random.randint(0,255), random.randint(0,255))
    COLORCOPY = COLOR
    proceed(strip)

#Farbe wird über Druckknopf gedimmt. Ruft die eigentliche Dimm-Funktion auf
def dimm(null):
    dimmColor()

#Farbe wird gedimmt
def dimmColor():
    global d
    global COLOR
    global COLORCOPY
    
    if (d < 3):
        red = (COLOR & BITMASK_RED) >> 8
        green = (COLOR & BITMASK_GREEN) >> 16
        blue = COLOR & BITMASK_BLUE
        COLOR = Color(green/2, red/2, blue/2)
        d = d + 1
    elif (d >= 3):
        COLOR = COLORCOPY
        d = 0
    proceed(strip)

#Farbe wird auf komplett dunkel (nicht sichtbar) gesetzt
def dark():
    global COLOR
    global COLORCOPY
    if COLOR != BLACK:
        COLOR = BLACK
    else:
        COLOR = COLORCOPY
    proceed(strip)

#Farbe wird über Druckknopf geändert, indem die Rainbow-Funktion gestartet wird
def changeRainbow(null):
    print("Change")
    global COLORCOPY
    COLORCOPY = rainbow(strip)
    print((COLOR & BITMASK_GREEN) >> 16, (COLOR & BITMASK_RED) >> 8, COLOR & BITMASK_BLUE)
    turnOnLEDs(strip, arrayLEDs)

#Über Druckknopf aufgerufene Rainbow-Funktion
def rainbow(strip):
    global COLOR
    global abschnitt
    wait = 0.01
    while True:
        if abschnitt == 0:
            for j in range(255):
                taster = GPIO.input(17)
                if (taster == True):
                    return COLOR
                COLOR = Color(j, 255, 0)
                showAll(strip)
                time.sleep(5*wait)
            abschnitt = 1
        elif abschnitt == 1:
            for j in range(255):
                taster = GPIO.input(17)
                if (taster == True):
                    return COLOR
                COLOR = Color(255, 255 - j, 0)
                showAll(strip)
                time.sleep(wait)
            abschnitt = 2
        elif abschnitt == 2:
            for j in range(255):
                taster = GPIO.input(17)
                if (taster == True):
                    return COLOR
                COLOR = Color(255, 0, j)
                showAll(strip)
                time.sleep(wait)
            abschnitt = 3
        elif abschnitt == 3:
            for j in range(255):
                taster = GPIO.input(17)
                if (taster == True):
                    return COLOR
                COLOR = Color(255-j, 0, 255)
                showAll(strip)
                time.sleep(wait)
            abschnitt = 4
        elif abschnitt == 4:
            for j in range(255):
                taster = GPIO.input(17)
                if (taster == True):
                    return COLOR
                COLOR = Color(0, j, 255)
                showAll(strip)
                time.sleep(wait)
            abschnitt = 5
        elif abschnitt == 5:
            for j in range(255):
                taster = GPIO.input(17)
                if (taster == True):
                    return COLOR
                COLOR = Color(0, 255, 255-j)
                showAll(strip)
                time.sleep(wait)
            abschnitt = 0

#Hilfsfunktion für Rainbow: lässt alle LEDs in der aktuellen Farbe leuchten
def showAll(strip):
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, COLOR)
    strip.show()
            
#Farbe wird über die GUI geändert, indem die Rainbow-Funktion gestartet wird
def startRainbow(null):
    global busy
    busy = True
    thread.start_new_thread(rainbow2, ())
    print("Leave start")

#Rainbow-Funktion, die über die GUI gestartet wird
def rainbow2():
    global running
    print("Start running")
    running = True

    global COLOR
    global abschnitt
    wait = 0.01
    while True:
        if abschnitt == 0:
            for j in range(255):
                if (running == False):
                    return
                COLOR = Color(j, 255, 0)
                showAll(strip)
                time.sleep(wait)
            abschnitt = 1
        elif abschnitt == 1:
            for j in range(255):
                if (running == False):
                    return
                COLOR = Color(255, 255 - j, 0)
                showAll(strip)
                time.sleep(wait)
            abschnitt = 2
        elif abschnitt == 2:
            for j in range(255):
                if (running == False):
                    return
                COLOR = Color(255, 0, j)
                showAll(strip)
                time.sleep(wait)
            abschnitt = 3
        elif abschnitt == 3:
            for j in range(255):
                if (running == False):
                    return
                COLOR = Color(255-j, 0, 255)
                showAll(strip)
                time.sleep(wait)
            abschnitt = 4
        elif abschnitt == 4:
            for j in range(255):
                if (running == False):
                    return
                COLOR = Color(0, j, 255)
                showAll(strip)
                time.sleep(wait)
            abschnitt = 5
        elif abschnitt == 5:
            for j in range(255):
                if (running == False):
                    return
                COLOR = Color(0, 255, 255-j)
                showAll(strip)
                time.sleep(wait)
            abschnitt = 0

#Hält die Rainbow-Funktion an. Ausgelöst, sobald der Button in der GUI losgelassen wird
def stopRainbow(null):
    global busy
    global COLORCOPY
    global COLOR
    global running
    print("Stop running")
    running = False
    time.sleep(1)
    print("Proceed")
    COLORCOPY = COLOR
    busy = False
    proceed(strip)

###FUNKTIONEN ZUM ANZEIGEN VON TEXTEN###

#Texteingabe: diese Funktion wird aufgerufen, sobald der Button gedrückt wurde. Ruft dann entweder die Easteregg-Funktion
#auf oder startet den Textdurchlauf.
def showInput():
    global busy
    if busy == True:
        return
    if (input_text.get().startswith("#egg-")):
        try:
            egg, seconds = input_text.get().split("-")
            second = (int)(seconds)
            lightning(second)
            input_text.delete(0,END)
        except:
            input_text.delete(0,END)
            print("Know your eastereggs!")
    elif (input_text.get().startswith("#fade")):
        fade()
        input_text.delete(0,END)
    elif (input_text.get().startswith("#werder")):
        werder()
        input_text.delete(0,END)
    elif (input_text.get().startswith("#pacman")):
        pacman()
        input_text.delete(0,END)
    else:
        thread.start_new_thread(showInput2, ())

#"Umgebung" der Textanzeige: Ruft die showText-Funktion auf und führt dann die Uhr normal fort
def showInput2():
    global busy
    busy = True
    text = input_text.get()
    text = " " + text
    print("Text gestartet")
    showText(text)
    while varCheckLoop.get() == 1:
        showText(text)
    input_text.delete(0,END)
    print("Text fertig")
    proceed(strip)
    busy = False

#Berechnet das nötige Array und ruft die Animations-Funktion auf
def showText(text):
    length = initialisieren(text)
    animation(length)

#Baut das Array anhand des Textes auf
def initialisieren(word):
    global t
    t = [[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0]]
    for i in range(7*len(word)):
        for j in range(len(t)):
            t[j].append(0)

    fillText(word)
    return len(t[2])

#Hilfsfunktion zum Aufbauen des Arrays
def fillText(word):
    for i in range(len(word)):
        if ((word[i] == "A") or (word[i] == "a")):
            t[2][7*i+5]=t[2][7*i+6]=t[2][7*i+7]=t[3][7*i+4]=t[3][7*i+8]=t[4][7*i+4]=t[4][7*i+8]=t[5][7*i+4]=t[5][7*i+8]=t[6][7*i+4]=t[6][7*i+5]=t[6][7*i+6]=t[6][7*i+7]=t[6][7*i+8]=t[7][7*i+4]=t[7][7*i+8]=t[8][7*i+4]=t[8][7*i+8]=1
        elif ((word[i] == u"Ä") or (word[i] == u"ä")):
            t[0][7*i+5]=t[0][7*i+7]=t[2][7*i+5]=t[2][7*i+6]=t[2][7*i+7]=t[3][7*i+4]=t[3][7*i+8]=t[4][7*i+4]=t[4][7*i+8]=t[5][7*i+4]=t[5][7*i+8]=t[6][7*i+4]=t[6][7*i+5]=t[6][7*i+6]=t[6][7*i+7]=t[6][7*i+8]=t[7][7*i+4]=t[7][7*i+8]=t[8][7*i+4]=t[8][7*i+8]=1
        elif ((word[i] == "B") or (word[i] == "b")):
            t[2][7*i+4]=t[2][7*i+5]=t[2][7*i+6]=t[2][7*i+7]=t[3][7*i+4]=t[3][7*i+8]=t[4][7*i+4]=t[4][7*i+8]=t[5][7*i+4]=t[5][7*i+5]=t[5][7*i+6]=t[5][7*i+7]=t[6][7*i+4]=t[6][7*i+8]=t[7][7*i+4]=t[7][7*i+8]=t[8][7*i+4]=t[8][7*i+5]=t[8][7*i+6]=t[8][7*i+7]=1
        elif ((word[i] == "C") or (word[i] == "c")):
            t[2][7*i+5]=t[2][7*i+6]=t[2][7*i+7]=t[3][7*i+4]=t[3][7*i+8]=t[4][7*i+4]=t[5][7*i+4]=t[6][7*i+4]=t[7][7*i+4]=t[7][7*i+8]=t[8][7*i+5]=t[8][7*i+6]=t[8][7*i+7]=1
        elif ((word[i] == "D") or (word[i] == "d")):
            t[2][7*i+4]=t[2][7*i+5]=t[2][7*i+6]=t[3][7*i+4]=t[3][7*i+7]=t[4][7*i+4]=t[4][7*i+8]=t[5][7*i+4]=t[5][7*i+8]=t[6][7*i+4]=t[6][7*i+8]=t[7][7*i+4]=t[7][7*i+7]=t[8][7*i+4]=t[8][7*i+5]=t[8][7*i+6]=1
        elif ((word[i] == "E") or (word[i] == "e")):
            t[2][7*i+4]=t[2][7*i+5]=t[2][7*i+6]=t[2][7*i+7]=t[2][7*i+8]=t[3][7*i+4]=t[4][7*i+4]=t[5][7*i+4]=t[5][7*i+5]=t[5][7*i+6]=t[5][7*i+7]=t[6][7*i+4]=t[7][7*i+4]=t[8][7*i+4]=t[8][7*i+5]=t[8][7*i+6]=t[8][7*i+7]=t[8][7*i+8]=1
        elif ((word[i] == "F") or (word[i] == "f")):
            t[2][7*i+4]=t[2][7*i+5]=t[2][7*i+6]=t[2][7*i+7]=t[2][7*i+8]=t[3][7*i+4]=t[4][7*i+4]=t[5][7*i+4]=t[5][7*i+5]=t[5][7*i+6]=t[5][7*i+7]=t[6][7*i+4]=t[7][7*i+4]=t[8][7*i+4]=1
        elif ((word[i] == "G") or (word[i] == "g")):
            t[2][7*i+5]=t[2][7*i+6]=t[2][7*i+7]=t[3][7*i+4]=t[3][7*i+8]=t[4][7*i+4]=t[5][7*i+4]=t[5][7*i+6]=t[5][7*i+7]=t[5][7*i+8]=t[6][7*i+4]=t[6][7*i+8]=t[7][7*i+4]=t[7][7*i+8]=t[8][7*i+5]=t[8][7*i+6]=t[8][7*i+7]=t[8][7*i+8]=1
        elif ((word[i] == "H") or (word[i] == "h")):
            t[2][7*i+4]=t[2][7*i+8]=t[3][7*i+4]=t[3][7*i+8]=t[4][7*i+4]=t[4][7*i+8]=t[5][7*i+4]=t[5][7*i+5]=t[5][7*i+6]=t[5][7*i+7]=t[5][7*i+8]=t[6][7*i+4]=t[6][7*i+8]=t[7][7*i+4]=t[7][7*i+8]=t[8][7*i+4]=t[8][7*i+8]=1
        elif ((word[i] == "I") or (word[i] == "i")):
            t[2][7*i+5]=t[2][7*i+6]=t[2][7*i+7]=t[3][7*i+6]=t[4][7*i+6]=t[5][7*i+6]=t[6][7*i+6]=t[7][7*i+6]=t[8][7*i+5]=t[8][7*i+6]=t[8][7*i+7]=1
        elif ((word[i] == "J") or (word[i] == "j")):
            t[2][7*i+6]=t[2][7*i+7]=t[2][7*i+8]=t[3][7*i+7]=t[4][7*i+7]=t[5][7*i+7]=t[6][7*i+7]=t[7][7*i+4]=t[7][7*i+7]=t[8][7*i+5]=t[8][7*i+6]=1
        elif ((word[i] == "K") or (word[i] == "k")):
            t[2][7*i+4]=t[2][7*i+8]=t[3][7*i+4]=t[3][7*i+7]=t[4][7*i+4]=t[4][7*i+6]=t[5][7*i+4]=t[5][7*i+5]=t[6][7*i+4]=t[6][7*i+6]=t[7][7*i+4]=t[7][7*i+7]=t[8][7*i+4]=t[8][7*i+8]=1
        elif ((word[i] == "L") or (word[i] == "l")):
            t[2][7*i+4]=t[3][7*i+4]=t[4][7*i+4]=t[5][7*i+4]=t[6][7*i+4]=t[7][7*i+4]=t[8][7*i+4]=t[8][7*i+5]=t[8][7*i+6]=t[8][7*i+7]=t[8][7*i+8]=1
        elif ((word[i] == "M") or (word[i] == "m")):
            t[2][7*i+4]=t[2][7*i+8]=t[3][7*i+4]=t[3][7*i+5]=t[3][7*i+7]=t[3][7*i+8]=t[4][7*i+4]=t[4][7*i+6]=t[4][7*i+8]=t[5][7*i+4]=t[5][7*i+6]=t[5][7*i+8]=t[6][7*i+4]=t[6][7*i+8]=t[7][7*i+4]=t[7][7*i+8]=t[8][7*i+4]=t[8][7*i+8]=1
        elif ((word[i] == "N") or (word[i] == "n")):
            t[2][7*i+4]=t[2][7*i+8]=t[3][7*i+4]=t[3][7*i+8]=t[4][7*i+4]=t[4][7*i+5]=t[4][7*i+8]=t[5][7*i+4]=t[5][7*i+6]=t[5][7*i+8]=t[6][7*i+4]=t[6][7*i+7]=t[6][7*i+8]=t[7][7*i+4]=t[7][7*i+8]=t[8][7*i+4]=t[8][7*i+8]=1
        elif ((word[i] == "O") or (word[i] == "o")):
            t[2][7*i+5]=t[2][7*i+6]=t[2][7*i+7]=t[3][7*i+4]=t[3][7*i+8]=t[4][7*i+4]=t[4][7*i+8]=t[5][7*i+4]=t[5][7*i+8]=t[6][7*i+4]=t[6][7*i+8]=t[7][7*i+4]=t[7][7*i+8]=t[8][7*i+5]=t[8][7*i+6]=t[8][7*i+7]=1
        elif ((word[i] == u"Ö") or (word[i] == u"ö")):
            t[0][7*i+5]=t[0][7*i+7]=t[2][7*i+5]=t[2][7*i+6]=t[2][7*i+7]=t[3][7*i+4]=t[3][7*i+8]=t[4][7*i+4]=t[4][7*i+8]=t[5][7*i+4]=t[5][7*i+8]=t[6][7*i+4]=t[6][7*i+8]=t[7][7*i+4]=t[7][7*i+8]=t[8][7*i+5]=t[8][7*i+6]=t[8][7*i+7]=1
        elif ((word[i] == "P") or (word[i] == "p")):
            t[2][7*i+4]=t[2][7*i+5]=t[2][7*i+6]=t[2][7*i+7]=t[3][7*i+4]=t[3][7*i+8]=t[4][7*i+4]=t[4][7*i+8]=t[5][7*i+4]=t[5][7*i+5]=t[5][7*i+6]=t[5][7*i+7]=t[6][7*i+4]=t[7][7*i+4]=t[8][7*i+4]=1
        elif ((word[i] == "Q") or (word[i] == "q")):
            t[2][7*i+5]=t[2][7*i+6]=t[2][7*i+7]=t[3][7*i+4]=t[3][7*i+8]=t[4][7*i+4]=t[4][7*i+8]=t[5][7*i+4]=t[5][7*i+8]=t[6][7*i+4]=t[6][7*i+6]=t[6][7*i+8]=t[7][7*i+4]=t[7][7*i+7]=t[8][7*i+5]=t[8][7*i+6]=t[8][7*i+8]=1
        elif ((word[i] == "R") or (word[i] == "r")):
            t[2][7*i+4]=t[2][7*i+5]=t[2][7*i+6]=t[2][7*i+7]=t[3][7*i+4]=t[3][7*i+8]=t[4][7*i+4]=t[4][7*i+8]=t[5][7*i+4]=t[5][7*i+5]=t[5][7*i+6]=t[5][7*i+7]=t[6][7*i+4]=t[6][7*i+6]=t[7][7*i+4]=t[7][7*i+7]=t[8][7*i+4]=t[8][7*i+8]=1
        elif ((word[i] == "S") or (word[i] == "s")):
            t[2][7*i+5]=t[2][7*i+6]=t[2][7*i+7]=t[2][7*i+8]=t[3][7*i+4]=t[4][7*i+4]=t[5][7*i+5]=t[5][7*i+6]=t[5][7*i+7]=t[6][7*i+8]=t[7][7*i+8]=t[8][7*i+4]=t[8][7*i+5]=t[8][7*i+6]=t[8][7*i+7]=1
        elif ((word[i] == "T") or (word[i] == "t")):
            t[2][7*i+4]=t[2][7*i+5]=t[2][7*i+6]=t[2][7*i+7]=t[2][7*i+8]=t[3][7*i+6]=t[4][7*i+6]=t[5][7*i+6]=t[6][7*i+6]=t[7][7*i+6]=t[8][7*i+6]=1
        elif ((word[i] == "U") or (word[i] == "u")):
            t[2][7*i+4]=t[2][7*i+8]=t[3][7*i+4]=t[3][7*i+8]=t[4][7*i+4]=t[4][7*i+8]=t[5][7*i+4]=t[5][7*i+8]=t[6][7*i+4]=t[6][7*i+8]=t[7][7*i+4]=t[7][7*i+8]=t[8][7*i+5]=t[8][7*i+6]=t[8][7*i+7]=1
        elif ((word[i] == u"Ü") or (word[i] == u"ü")):
            t[0][7*i+5]=t[0][7*i+7]=t[2][7*i+4]=t[2][7*i+8]=t[3][7*i+4]=t[3][7*i+8]=t[4][7*i+4]=t[4][7*i+8]=t[5][7*i+4]=t[5][7*i+8]=t[6][7*i+4]=t[6][7*i+8]=t[7][7*i+4]=t[7][7*i+8]=t[8][7*i+5]=t[8][7*i+6]=t[8][7*i+7]=1
        elif ((word[i] == "V") or (word[i] == "v")):
            t[2][7*i+4]=t[2][7*i+8]=t[3][7*i+4]=t[3][7*i+8]=t[4][7*i+4]=t[4][7*i+8]=t[5][7*i+4]=t[5][7*i+8]=t[6][7*i+4]=t[6][7*i+8]=t[7][7*i+5]=t[7][7*i+7]=t[8][7*i+6]=1
        elif ((word[i] == "W") or (word[i] == "w")):
            t[2][7*i+4]=t[2][7*i+8]=t[3][7*i+4]=t[3][7*i+8]=t[4][7*i+4]=t[4][7*i+8]=t[5][7*i+4]=t[5][7*i+6]=t[5][7*i+8]=t[6][7*i+4]=t[6][7*i+6]=t[6][7*i+8]=t[7][7*i+4]=t[7][7*i+6]=t[7][7*i+8]=t[8][7*i+5]=t[8][7*i+7]=1
        elif ((word[i] == "X") or (word[i] == "x")):
            t[2][7*i+4]=t[2][7*i+8]=t[3][7*i+4]=t[3][7*i+8]=t[4][7*i+5]=t[4][7*i+7]=t[5][7*i+6]=t[6][7*i+5]=t[6][7*i+7]=t[7][7*i+4]=t[7][7*i+8]=t[8][7*i+4]=t[8][7*i+8]=1
        elif ((word[i] == "Y") or (word[i] == "y")):
            t[2][7*i+4]=t[2][7*i+8]=t[3][7*i+4]=t[3][7*i+8]=t[4][7*i+4]=t[4][7*i+8]=t[5][7*i+5]=t[5][7*i+7]=t[6][7*i+6]=t[7][7*i+6]=t[8][7*i+6]=1
        elif ((word[i] == "Z") or (word[i] == "z")):
            t[2][7*i+4]=t[2][7*i+5]=t[2][7*i+6]=t[2][7*i+7]=t[2][7*i+8]=t[3][7*i+8]=t[4][7*i+7]=t[5][7*i+6]=t[6][7*i+5]=t[7][7*i+4]=t[8][7*i+4]=t[8][7*i+5]=t[8][7*i+6]=t[8][7*i+7]=t[8][7*i+8]=1
	elif (word[i] == "0"):
            t[2][7*i+5]=t[2][7*i+6]=t[2][7*i+7]=t[3][7*i+4]=t[3][7*i+8]=t[4][7*i+4]=t[4][7*i+7]=t[4][7*i+8]=t[5][7*i+4]=t[5][7*i+6]=t[5][7*i+8]=t[6][7*i+4]=t[6][7*i+5]=t[6][7*i+8]=t[7][7*i+4]=t[7][7*i+8]=t[8][7*i+5]=t[8][7*i+6]=t[8][7*i+7]=1
        elif (word[i] == "1"):
            t[2][7*i+6]=t[3][7*i+5]=t[3][7*i+6]=t[4][7*i+6]=t[5][7*i+6]=t[6][7*i+6]=t[7][7*i+6]=t[8][7*i+5]=t[8][7*i+6]=t[8][7*i+7]=1
        elif (word[i] == "2"):
            t[2][7*i+5]=t[2][7*i+6]=t[2][7*i+7]=t[3][7*i+4]=t[3][7*i+8]=t[4][7*i+8]=t[5][7*i+7]=t[6][7*i+6]=t[7][7*i+5]=t[8][7*i+4]=t[8][7*i+5]=t[8][7*i+6]=t[8][7*i+7]=t[8][7*i+8]=1
        elif (word[i] == "3"):
            t[2][7*i+4]=t[2][7*i+5]=t[2][7*i+6]=t[2][7*i+7]=t[2][7*i+8]=t[3][7*i+7]=t[4][7*i+6]=t[5][7*i+7]=t[6][7*i+8]=t[7][7*i+4]=t[7][7*i+8]=t[8][7*i+5]=t[8][7*i+6]=t[8][7*i+7]=1
        elif (word[i] == "4"):
            t[2][7*i+7]=t[3][7*i+6]=t[3][7*i+7]=t[4][7*i+5]=t[4][7*i+7]=t[5][7*i+4]=t[5][7*i+7]=t[6][7*i+4]=t[6][7*i+5]=t[6][7*i+6]=t[6][7*i+7]=t[6][7*i+8]=t[7][7*i+7]=t[8][7*i+7]=1
        elif (word[i] == "5"):
            t[2][7*i+4]=t[2][7*i+5]=t[2][7*i+6]=t[2][7*i+7]=t[2][7*i+8]=t[3][7*i+4]=t[4][7*i+4]=t[4][7*i+5]=t[4][7*i+6]=t[4][7*i+7]=t[5][7*i+8]=t[6][7*i+8]=t[7][7*i+4]=t[7][7*i+8]=t[8][7*i+5]=t[8][7*i+6]=t[8][7*i+7]=1
        elif (word[i] == "6"):
            t[2][7*i+6]=t[2][7*i+7]=t[3][7*i+5]=t[4][7*i+4]=t[5][7*i+4]=t[5][7*i+5]=t[5][7*i+6]=t[5][7*i+7]=t[6][7*i+4]=t[6][7*i+8]=t[7][7*i+4]=t[7][7*i+8]=t[8][7*i+5]=t[8][7*i+6]=t[8][7*i+7]=1
        elif (word[i] == "7"):
            t[2][7*i+4]=t[2][7*i+5]=t[2][7*i+6]=t[2][7*i+7]=t[2][7*i+8]=t[3][7*i+8]=t[4][7*i+7]=t[5][7*i+6]=t[6][7*i+5]=t[7][7*i+5]=t[8][7*i+5]=1
        elif (word[i] == "8"):
            t[2][7*i+5]=t[2][7*i+6]=t[2][7*i+7]=t[3][7*i+4]=t[3][7*i+8]=t[4][7*i+4]=t[4][7*i+8]=t[5][7*i+5]=t[5][7*i+6]=t[5][7*i+7]=t[6][7*i+4]=t[6][7*i+8]=t[7][7*i+4]=t[7][7*i+8]=t[8][7*i+5]=t[8][7*i+6]=t[8][7*i+7]=1
        elif (word[i] == "9"):
            t[2][7*i+5]=t[2][7*i+6]=t[2][7*i+7]=t[3][7*i+4]=t[3][7*i+8]=t[4][7*i+4]=t[4][7*i+8]=t[5][7*i+5]=t[5][7*i+6]=t[5][7*i+7]=t[5][7*i+8]=t[6][7*i+8]=t[7][7*i+7]=t[8][7*i+5]=t[8][7*i+6]=1
        elif (word[i] == "."):
            t[7][7*i+5]=t[7][7*i+6]=t[8][7*i+5]=t[8][7*i+6]=1
        elif (word[i] == ","):
            t[6][7*i+5]=t[6][7*i+6]=t[7][7*i+6]=t[8][7*i+5]=1
        elif (word[i] == "!"):
            t[2][7*i+6]=t[3][7*i+6]=t[4][7*i+6]=t[5][7*i+6]=t[8][7*i+6]=1
        elif (word[i] == "?"):
            t[2][7*i+5]=t[2][7*i+6]=t[2][7*i+7]=t[3][7*i+4]=t[3][7*i+8]=t[4][7*i+8]=t[5][7*i+7]=t[6][7*i+6]=t[8][7*i+6]=1
        elif (word[i] == "#"):
            t[2][7*i+5]=t[2][7*i+7]=t[3][7*i+5]=t[3][7*i+7]=t[4][7*i+4]=t[4][7*i+5]=t[4][7*i+6]=t[4][7*i+7]=t[4][7*i+8]=t[5][7*i+5]=t[5][7*i+7]=t[6][7*i+4]=t[6][7*i+5]=t[6][7*i+6]=t[6][7*i+7]=t[7][7*i+5]=t[7][7*i+7]=t[8][7*i+5]=t[8][7*i+7]=1       
            
#Der eigentliche Textdurchlauf: setzt die LEDs, verzögert, und bewegt dann alles nach links
def animation(length):
    x = length
    while (x>0):
        arNew = []
        for i in range(len(matrix)):
            for j in range(len(matrix[i])):
                if (t[i][j]==1):
                    arNew.append(matrix[i][j])
        turnOnLEDs(strip, arNew)
        array = arNew
        shiftText()
        x = x-1
        time.sleep(slider_delay.get())

#Hilfsfunktion zum Verschieben nach links        
def shiftText():
    global t
    for i in range(len(t)):
        for j in range(len(t[i])-1):
            t[i][j] = t[i][j+1]

#EASTEREGG: Taschenlampe
def lightning(second):
    global busy
    busy = True
    showAllColor(strip, Color(255, 0, 0))
    time.sleep(second)
    busy = False
    proceed(strip)

#EASTEREGG: Fade
def fade():
    global busy
    busy = True
    x = 170
    for j in range(3):
        for i in range(x):
            showAllColor(strip, Color(0, i, 0))
            time.sleep(0.001)
        for i in range(x):
            showAllColor(strip, Color(0, x-1-i, 0))
            time.sleep(0.001)
    busy = False
    proceed(strip)

#EASTEREGG: Werder-Logo
def werder():
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, Color(0, 0, 0))
    arrayLEDs = []
    arrayLEDs.extend((18, 30, 38, 54, 58, 76, 82, 96, 106, 94, 86, 70, 66, 48, 42, 28))
    arrayLEDs.extend((29,39,40,41,50,51,52,61,74,63,72,59,65,84,95))
    for i in range(len(arrayLEDs)):
        strip.setPixelColor(arrayLEDs[i], Color(255, 0, 0))
    arrayLEDs2 = []
    arrayLEDs2.extend((53, 60, 75, 83, 62, 73, 85, 49, 64, 71))
    for i in range(len(arrayLEDs2)):
        strip.setPixelColor(arrayLEDs2[i], Color(255, 255, 255))
    strip.show()

#Lässt alle LEDs in der übergebenen Farbe leuchten
def showAllColor(strip, colo):
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, colo)
    strip.show()

###FUNKTIONEN ZUM SETZEN DER ZEITEN UND SPRACHE###

#Setzt die Morgenzeit auf die vom Nutzer eingegebene Uhrzeit
def setMorningTime():
    global morningMinutes
    global morningHour
    try:
        mh, mm = time_entry.get().split(':')
        h = (int)(mh)
        m = (int)(mm)
        if (h >= 0 and h <= 23 and m >= 0 and m < 60):
            morningHour = h
            morningMinutes = m
            print("Erfolgreiche Eingabe")
            time_entry.delete(0,END)
        else:
            print("Keine gültige Uhrzeit")
            tkMessageBox.showerror("Fehlerhafte Eingabe","Die Eingabe entspricht keiner gültigen Uhrzeit! Bitte Format HH:MM eingeben.")
    except:
        tkMessageBox.showerror("Fehlerhafte Eingabe","Die Eingabe entspricht keiner gültigen Uhrzeit! Bitte Format HH:MM eingeben.")
        print("Fehlerhafte Eingabe")
        time_entry.delete(0,END)

#Setzt die Nachtzeit auf die vom Nutzer eingegebene Uhrzeit
def setNightTime():
    global nightMinutes
    global nightHour
    try:
        nh, nm = time_entry2.get().split(':')
        h = (int)(nh)
        m = (int)(nm)
        if (h >= 0 and h <= 23 and m >= 0 and m < 60):
            nightHour = h
            nightMinutes = m
            print("Erfolgreiche Eingabe")
            time_entry2.delete(0,END)
        else:
            print("Keine gültige Uhrzeit")
            tkMessageBox.showerror("Fehlerhafte Eingabe","Die Eingabe entspricht keiner gültigen Uhrzeit! Bitte Format HH:MM eingeben.")
    except:
        tkMessageBox.showerror("Fehlerhafte Eingabe","Die Eingabe entspricht keiner gültigen Uhrzeit! Bitte Format HH:MM eingeben.")
        print("Fehlerhafte Eingabe")
        time_entry2.delete(0,END)

#Setzt die Nachtfarbe auf die aktuell gesetzte Farbe    
def setNightcolor():
    global NIGHTCOLOR
    global COLOR
    NIGHTCOLOR = COLOR

#Ändert die Spracheinstellung auf Schwäbisch bzw normal
def changeLanguage():
    print("Sprachmodus geändert")
    proceed(strip)

###FUNKTIONEN FÜR WEITERE EFFEKTE###

#Zeigt ein Herz auf der Uhr an
def heart():
    arrayLEDs = []
    arrayLEDs.extend((16,17,19,20,32,29,26,36,55,59,75,83,95,85,71,65,47,44))
    #Ausgefülltes Herz: arrayLEDs.extend((31,30,28,27,37,38,39,40,41,42,43,54,53,52,51,50,49,48,60,61,62,63,64,74,73,72,84))
    turnOnLEDs(strip, arrayLEDs)

#Zeigt einen Smiley auf der Uhr an
def smiley():
    arrayLEDs = []
    arrayLEDs.extend((30,39,28,41,65,71,85,84,83,75,59))
    turnOnLEDs(strip, arrayLEDs)
    
#Zeigt Pacman auf der Uhr an
def pacman():
    clear(strip)
    arrayX = [0,0,0,0,1,1,2,2,3,3,4,4,5,5,6,6,7,7,8,8,8,8]
    arrayY = [3,4,5,6,2,7,1,8,0,7,0,6,0,7,1,8,2,7,3,4,5,6]
    for i in range(len(arrayX)):
        strip.setPixelColor(matrix[arrayX[i]][arrayY[i]], Color(200,255,0))
    strip.setPixelColor(matrix[2][5], Color(100,255,0))
    strip.setPixelColor(matrix[4][8], Color(100,255,0))
    strip.setPixelColor(matrix[4][10], Color(100,255,0))
    strip.show()
    

#Animation, in der die Buchstaben der Uhrzeit einzeln einlaufen
def circle():
    global busy
    busy = True
    global COLOR

    clear(strip)
    ti = datetime.datetime.now()
    hour = ti.hour
    minute = ti.minute
    second = ti.second
    arrayNumbers = calculateArray(hour, minute)
    arrayNumbers.sort()
    
    for i in range(len(arrayNumbers)):
        maximum = arrayNumbers.pop()
        for j in range(maximum + 1):
            strip.setPixelColor(j, COLOR)
            strip.setPixelColor(j-1, Color(0, 0, 0))
            strip.show()
            time.sleep(0.03)

    proceed(strip)
    busy = False

#Aus nostalgischen Gründen noch hier :)
def dimmAll(null):
    ti = datetime.datetime.now()
    minute = ti.minute
    if minute == 50:
        showText(" 847.")
        print("Ok.")
    else:
        arrayLEDs = []
        arrayLEDs.extend((30,39,28,41,61,62,63,75,71,81,87))
        turnOnLEDs(strip, arrayLEDs)
        print("Smiley")

#Startet die Matrix-Animation
def matrix():
    global busy
    if busy == True:
        return
    global COLOR
    global matrixRunning
    matrixRunning = 0
    busy = True
    clear(strip)
    ti = datetime.datetime.now()
    hour = ti.hour
    minute = ti.minute
    second = ti.second
    arrayNumbers = calculateArray(hour, minute)
    for i in range(len(matrix[0])):
        thread.start_new_thread(matrixLine, (strip,i, arrayNumbers))
    print("ALLE THREADS GESTARTET")
    while matrixRunning < 11:
        time.sleep(1)
    print("FAHRE FORT")
    proceed(strip)
    busy = False

#Hilfsfunktion für die Matrix-Animation  
def matrixLine(strip, line, arrayNumbers):
    global matrixRunning
    time.sleep(random.random()*1)
    lC = 250
    lL = 0
    lastRun = False
    finishNow=0

    j = 0
    while (finishNow<=18):
         #strip.setPixelColor(matrix[lL][line],Color(lC, 0, 0))
         for i in range(lL):
             if (i < 10 and (lastRun == False or matrix[i][line] not in arrayNumbers)):
                 strip.setPixelColor(matrix[i][line],Color((int)((lC / (2**(lL-i-1)))*1), 0, 0))
                 #strip.setPixelColor(matrix[i][line],Color(max(lC-((lL-i)*33),0), 0, 0))
         if lL < 10:
             strip.setPixelColor(matrix[lL][line],COLOR)
         lL = lL + 1
         strip.show()
         if lastRun == True:
             finishNow=finishNow+1
         if (lL > 13 and random.random() > 0.8 and lastRun == False):
             lL = 0
             if j >= 150:
                 lastRun = True
         time.sleep(0.1)
         
         j= j+1
    matrixRunning = matrixRunning + 1

#Startet das Snake-Spiel.
def startSnake():
    global busy
    if busy == True:
        return
    thread.start_new_thread(snake, ())

#Snake
def snake():
    global busy
    global COLOR
    global COLORCOPY
    global newDirection
    busy = True
    print("Start Snake.")
    counter = 0
    sleepTime = 0.4
    xHead = random.randint(0, 9)
    yHead = random.randint(0, 10)
    xFood = random.randint(0, 9)
    yFood = random.randint(0, 10)
    greenLEDs = [matrix[xHead][yHead]]
    food = matrix[xFood][yFood]
    clear(strip)
    strip.setPixelColor(food, Color(0,255,0))
    strip.setPixelColor(matrix[xHead][yHead], Color(255,100,0))
    strip.show()
    time.sleep(2)
    curDir = random.choice(["w", "a", "s", "d"])
    newDirection = curDir
    master.bind("w", snakeW)
    master.bind("a", snakeA)
    master.bind("s", snakeS)
    master.bind("d", snakeD)
    finished = False

    #Hauptschleife
    while finished == False:
        #Neue Richtung setzen, falls erlaubte Änderung
        newDir = newDirection
        if newDir == "w" and curDir != "s": curDir = "w"
        elif newDir == "s" and curDir != "w": curDir = "s"
        elif newDir == "d" and curDir != "a": curDir = "d"
        elif newDir == "a" and curDir != "d": curDir = "a"

        #Neuen Head setzen und am Ende hinzufügen, abhängig von Richtung
        if curDir == "w":
            xHead = (xHead - 1) % 10
        elif curDir == "s":
            xHead = (xHead + 1) % 10
        elif curDir == "a":
            yHead = (yHead - 1) % 11
        elif curDir == "d":
            yHead = (yHead + 1) % 11

        greenLEDs.append(matrix[xHead][yHead])
        
        #Falls kein Futter getroffen: Ende der Schlange entfernen
        if not matrix[xHead][yHead] == food:
            greenLEDs.pop(0)
        else:
            #Falls Futter getroffen: neues Futter setzen
            counter = counter + 1
            while (food in greenLEDs and counter != 109):
                food = matrix[random.randint(0,9)][random.randint(0,10)]

        #Prüfen, ob Schlange sich selbst frisst
        greenLEDs.remove(matrix[xHead][yHead])
        if matrix[xHead][yHead] in greenLEDs:
            finished = True
        greenLEDs.append(matrix[xHead][yHead])

        #Spielfeld anzeigen und Sleep
        clear(strip)
        for i in range(len(greenLEDs)):
            strip.setPixelColor(greenLEDs[i], Color(255,0,0))
        strip.setPixelColor(food, Color(0,255,0))
        strip.setPixelColor(matrix[xHead][yHead], Color(255, 100,0))
        strip.show()
        time.sleep(sleepTime)

    #Ende. Tasten deaktivieren, Punktzahl anzeigen.
    master.unbind("w")
    master.unbind("a")
    master.unbind("s")
    master.unbind("d")
    time.sleep(1)

    if (counter > config.getint('sonstiges_section', 'highscore')):
        trophy = []
        trophy.extend((matrix[1][3], matrix[1][4], matrix[1][5], matrix[1][6], matrix[1][7], matrix[2][2], matrix[2][3], matrix[2][7], matrix[2][8] ))
        trophy.extend((matrix[3][2], matrix[3][3], matrix[3][7], matrix[3][8], matrix[4][2], matrix[4][3], matrix[4][7], matrix[4][8]))
        trophy.extend((matrix[5][3], matrix[5][7], matrix[6][3], matrix[6][7], matrix[7][4], matrix[7][5], matrix[7][6], matrix[8][5]))
        trophy.extend((matrix[9][3], matrix[9][4], matrix[9][5], matrix[9][6], matrix[9][7], matrix[3][1], matrix[3][9]))
        turnOnLEDs(strip, trophy)
        time.sleep(5)
        config.set('sonstiges_section', 'highscore', counter)
        with open('/home/pi/Schreibtisch/Python/WordClock/wordclock_cfg.cfg', 'wb') as configfile:
            config.write(configfile)

    score = str(counter)
    scoreShow = " " + score
    showText(scoreShow)
    print("Snake fertig. Deine Punktzahl: " + score)
    COLOR = COLORCOPY
    deleteEntries()
    busy = False
    proceed(strip)

###Hilfsfunktionen für Snake: Ändern bei Drücken von WASD die Richtung###
def snakeW(event):
    global newDirection
    newDirection = "w"

def snakeA(event):
    global newDirection
    newDirection = "a"

def snakeS(event):
    global newDirection
    newDirection = "s"

def snakeD(event):
    global newDirection
    newDirection = "d"


###################################################################


#Startet das Pacman-Spiel.
def startPacman():
    global busy
    if busy == True:
        return
    thread.start_new_thread(pacman, (1,0))

#Snake
def pacman(l, c):
    global busy
    global COLOR
    global COLORCOPY
    global newPDirection
    busy = True
    print("Start Pacman.")
    counter = c
    level = l
    sleepTime = 0.3
    xPacman = random.randint(0, 9)
    yPacman = random.randint(0, 10)
    xEnemy1 = random.randint(0, 9)
    yEnemy1 = random.randint(0, 10)
    xEnemy2 = random.randint(0, 9)
    yEnemy2 = random.randint(0, 10)
    xEnemy3 = random.randint(0, 9)
    yEnemy3 = random.randint(0, 10)
    xEnemy4 = random.randint(0, 9)
    yEnemy4 = random.randint(0, 10)
    pills = []
    for i in range(2,111):
        pills.append(i)
    pacman = matrix[xPacman][yPacman]
    enemy1 = matrix[xEnemy1][yEnemy1]
    enemy2 = matrix[xEnemy2][yEnemy2]
    enemy3 = matrix[xEnemy3][yEnemy3]
    enemy4 = matrix[xEnemy4][yEnemy4]
    power1 = 12
    power2 = 2
    power3 = 101
    power4 = 111
    clear(strip)
    for i in range(len(pills)):
        strip.setPixelColor(pills[i], Color(255,255,255))
    strip.setPixelColor(pacman, Color(200,255,0))
    strip.setPixelColor(enemy1, Color(0,255,0))
    strip.setPixelColor(enemy2, Color(255,0,0))
    strip.setPixelColor(enemy3, Color(60,0,255))
    strip.setPixelColor(enemy4, Color(50,255,0))
    strip.show()
    time.sleep(2)
    curDir = random.choice(["w", "a", "s", "d"])
    newPDirection = curDir
    master.bind("w", pacmanW)
    master.bind("a", pacmanA)
    master.bind("s", pacmanS)
    master.bind("d", pacmanD)
    finished = False

    #Hauptschleife
    while finished == False:
        #Neue Richtung setzen, falls erlaubte Änderung
        curDir = newPDirection

        #Neue Position von Pacman berechnen
        if curDir == "w":
            xPacman = max(xPacman - 1, 0)
        elif curDir == "s":
            xPacman = min(xPacman + 1, 9)
        elif curDir == "a":
            yPacman = max(yPacman - 1, 0)
        elif curDir == "d":
            yPacman = min(yPacman + 1, 10)
        pacman = matrix[xPacman][yPacman]

        #Pillen berechnen
        if pacman in pills:
            pills.remove(pacman)
            counter = counter + 1

        #Geister Bewegung berechnen

        #Kollision mit Geistern prüfen
        if pacman == enemy1 or pacman == enemy2 or pacman == enemy3 or pacman == enemy4:
            finished = True
        
        #Spielfeld anzeigen und Sleep
        clear(strip)
        for i in range(len(pills)):
            strip.setPixelColor(pills[i], Color(30,30,0))
        strip.setPixelColor(pacman, Color(200,255,0))
        strip.setPixelColor(enemy1, Color(0,255,0))
        strip.setPixelColor(enemy2, Color(0,255,0))
        strip.setPixelColor(enemy3, Color(0,255,0))
        strip.setPixelColor(enemy4, Color(0,255,0))
        strip.show()
        time.sleep(sleepTime)

    #Ende. Tasten deaktivieren, Punktzahl anzeigen.
    master.unbind("w")
    master.unbind("a")
    master.unbind("s")
    master.unbind("d")
    time.sleep(1)

    if (counter > config.getint('sonstiges_section', 'pacmanscore')):
        trophy = []
        trophy.extend((matrix[1][3], matrix[1][4], matrix[1][5], matrix[1][6], matrix[1][7], matrix[2][2], matrix[2][3], matrix[2][7], matrix[2][8] ))
        trophy.extend((matrix[3][2], matrix[3][3], matrix[3][7], matrix[3][8], matrix[4][2], matrix[4][3], matrix[4][7], matrix[4][8]))
        trophy.extend((matrix[5][3], matrix[5][7], matrix[6][3], matrix[6][7], matrix[7][4], matrix[7][5], matrix[7][6], matrix[8][5]))
        trophy.extend((matrix[9][3], matrix[9][4], matrix[9][5], matrix[9][6], matrix[9][7], matrix[3][1], matrix[3][9]))
        turnOnLEDs(strip, trophy)
        time.sleep(5)
        config.set('sonstiges_section', 'pacmanscore', counter)
        with open('/home/pi/Schreibtisch/Python/WordClock/wordclock_cfg.cfg', 'wb') as configfile:
            config.write(configfile)

    score = str(counter)
    scoreShow = " " + score
    showText(scoreShow)
    print("Pacman fertig. Deine Punktzahl: " + score)
    COLOR = COLORCOPY
    deleteEntries()
    busy = False
    proceed(strip)

###Hilfsfunktionen für Pacman: Ändern bei Drücken von WASD die Richtung###
def pacmanW(event):
    global newPDirection
    newPDirection = "w"

def pacmanA(event):
    global newPDirection
    newPDirection = "a"

def pacmanS(event):
    global newPDirection
    newPDirection = "s"

def pacmanD(event):
    global newPDirection
    newPDirection = "d"

###################################################################
    

#Startet Tetris
def startTetris():
    global busy
    if busy == True:
        return
    thread.start_new_thread(tetris, ())

#Tetris
def tetris():
    global COLOR
    global COLORCOPY
    global busy
    global calcActive
    global paused
    paused = False
    calcActive = False
    busy = True
    master.bind("a", left)
    master.bind("d", right)
    master.bind("s", down)
    master.bind("q", rotateL)
    master.bind("e", rotateR)
    master.bind("w", rotateR)
    master.bind("<space>", pauseTetris)
    global currentBlock
    global nextBlock
    global isMovable
    isMovable = True
    randomBlock = random.randint(0,6)
    if randomBlock == 0:
        currentBlock = QBlock()
    elif randomBlock == 1:
        currentBlock = LBlock()
    elif randomBlock == 2:
        currentBlock = ZBlock()
    elif randomBlock == 3:
        currentBlock = TBlock()
    elif randomBlock == 4:
        currentBlock = IBlock()
    elif randomBlock == 5:
        currentBlock = SBlock()
    elif randomBlock == 6:
        currentBlock = JBlock()
    randomBlock2 = random.randint(0,6)
    if randomBlock2 == 0:
        nextBlock = QBlock()
    elif randomBlock2 == 1:
        nextBlock = LBlock()
    elif randomBlock2 == 2:
        nextBlock = ZBlock()
    elif randomBlock2 == 3:
        nextBlock = TBlock()
    elif randomBlock2 == 4:
        nextBlock = IBlock()
    elif randomBlock2 == 5:
        nextBlock = SBlock()
    elif randomBlock2 == 6:
        nextBlock = JBlock()
    finish = False
    print("Start Tetris.")
    while finish == False:
        while ((calcActive == True) or (paused == True)):
            time.sleep(0.05)
        calcActive = True
        isMovable = currentBlock.isMovable()
        if isMovable == True:
            currentBlock.moveDown()
            turnOnBlock(currentBlock, nextBlock)
        else:
            currentBlock.addToField()
            removeAnything = currentBlock.checkAndRemoveFullRows()
            if removeAnything == True:
                turnOnField(currentBlock, nextBlock)
                time.sleep(0.5)
                currentBlock.fillEmptyRows()
                turnOnField(currentBlock, nextBlock)
                time.sleep(0.5)
            isMovable = True
            currentBlock = nextBlock
            randomBlock = random.randint(0,6)
            if randomBlock == 0:
                nextBlock = QBlock()
            elif randomBlock == 1:
                nextBlock = LBlock()
            elif randomBlock == 2:
                nextBlock = ZBlock()
            elif randomBlock == 3:
                nextBlock = TBlock()
            elif randomBlock == 4:
                nextBlock = IBlock()
            elif randomBlock == 5:
                nextBlock = SBlock()
            elif randomBlock == 6:
                nextBlock = JBlock()
            finish = currentBlock.isLost()
            isMovable = currentBlock.isMovable()
            turnOnBlock(currentBlock, nextBlock)
        calcActive = False
        time.sleep(1.0)
    master.unbind("a")
    master.unbind("s")
    master.unbind("d")
    master.unbind("w")
    master.unbind("e")
    master.unbind("q")
    master.unbind("<space>")
    counter = currentBlock.getScore()
    if (counter > config.getint('sonstiges_section', 'tetrisscore')):
        trophy = []
        trophy.extend((matrix[1][3], matrix[1][4], matrix[1][5], matrix[1][6], matrix[1][7], matrix[2][2], matrix[2][3], matrix[2][7], matrix[2][8] ))
        trophy.extend((matrix[3][2], matrix[3][3], matrix[3][7], matrix[3][8], matrix[4][2], matrix[4][3], matrix[4][7], matrix[4][8]))
        trophy.extend((matrix[5][3], matrix[5][7], matrix[6][3], matrix[6][7], matrix[7][4], matrix[7][5], matrix[7][6], matrix[8][5]))
        trophy.extend((matrix[9][3], matrix[9][4], matrix[9][5], matrix[9][6], matrix[9][7], matrix[3][1], matrix[3][9]))
        turnOnLEDs(strip, trophy)
        time.sleep(5)
        config.set('sonstiges_section', 'tetrisscore', counter)
        with open('/home/pi/Schreibtisch/Python/WordClock/wordclock_cfg.cfg', 'wb') as configfile:
            config.write(configfile)
    score = str(counter)
    scoreShow = " " + score
    showText(scoreShow) 
    print("Tetris fertig. Deine Punktzahl: " + score)
    currentBlock.delete()
    deleteEntries()
    proceed(strip)
    busy = False

#Aktualisiert das Spielfeld nach normaler Bewegung.
def turnOnBlock(cBlock, nBlock):
    clear(strip)
    blockArray = cBlock.getBlock()
    blockColor = cBlock.getColor()
    for i in range(len(blockArray)):
        strip.setPixelColor(blockArray[i], blockColor)
    allFields = cBlock.getAllFields()
    allColors = cBlock.getAllColors()
    for i in range(len(allFields)):
        strip.setPixelColor(allFields[i], allColors[i])
    strip.setPixelColor(0, nBlock.getColor())
    strip.setPixelColor(1, nBlock.getColor())
    strip.setPixelColor(112, nBlock.getColor())
    strip.setPixelColor(113, nBlock.getColor())
    strip.show()

#Aktualisiert das Spielfeld nach Auflösen von Reihen.
def turnOnField(cBlock, nBlock):
    clear(strip)
    allFields = cBlock.getAllFields()
    allColors = cBlock.getAllColors()
    for i in range(len(allFields)):
        strip.setPixelColor(allFields[i], allColors[i])
    strip.setPixelColor(0, nBlock.getColor())
    strip.setPixelColor(1, nBlock.getColor())
    strip.setPixelColor(112, nBlock.getColor())
    strip.setPixelColor(113, nBlock.getColor())
    strip.show()

###Hilfsfunktionen für Tetris, die durch Tastendruck ausgelöst werden (Pause, Bewegung und Rotation)###
def pauseTetris(event):
    global paused
    global calcActive
    while calcActive == True:
        time.sleep(0.05)
    if paused == False:
        master.unbind("a")
        master.unbind("s")
        master.unbind("d")
        master.unbind("w")
        master.unbind("e")
        master.unbind("q")
        master.bind("x", showTetrisScore)
        paused = True
    else:
        master.bind("a", left)
        master.bind("d", right)
        master.bind("s", down)
        master.bind("q", rotateL)
        master.bind("e", rotateR)
        master.bind("w", rotateR)
        master.unbind("x")
        paused = False

def showTetrisScore(event):
    global currentBlock
    global nextBlock
    showText(" "+(str)(currentBlock.getScore()))
    turnOnBlock(currentBlock, nextBlock)
        
def left(event):
    global currentBlock
    global nextBlock
    global calcActive
    while calcActive == True:
        time.sleep(0.05)
    calcActive = True
    currentBlock.moveLeft()
    turnOnBlock(currentBlock, nextBlock)
    calcActive = False

def right(event):
    global currentBlock
    global nextBlock
    global calcActive
    while calcActive == True:
        time.sleep(0.05)
    calcActive = True
    currentBlock.moveRight()
    turnOnBlock(currentBlock, nextBlock)
    calcActive = False

def down(event):
    global currentBlock
    global nextBlock
    global calcActive
    while calcActive == True:
        time.sleep(0.05)
    if currentBlock.isMovable() == True:
        calcActive = True
        currentBlock.moveDown()
        turnOnBlock(currentBlock, nextBlock)
        calcActive = False

def rotateL(event):
    global currentBlock
    global nextBlock
    global calcActive
    while calcActive == True:
        time.sleep(0.05)
    calcActive = True
    currentBlock.rotateLeft()
    turnOnBlock(currentBlock, nextBlock)
    calcActive = False

def rotateR(event):
    global currentBlock
    global nextBlock
    global calcActive
    while calcActive == True:
        time.sleep(0.05)
    calcActive = True
    currentBlock.rotateRight()
    turnOnBlock(currentBlock, nextBlock)
    calcActive = False

#Startet Space Invaders
def startSpaceInvaders():
    global busy
    if busy == True:
        return
    thread.start_new_thread(spaceInvaders, ())

#Space Invaders
def spaceInvaders():
    global busy
    global finish
    finish = False
    busy = True
    bindSpaceKeys()
    counter = 0
    global shipY
    global enemiesX
    global enemiesY
    global enemyShotsX
    global enemyShotsY
    global shipShotX
    global shipShotY
    shipY = 5
    enemiesX = []
    enemiesY = []
    for i in range (11):
        enemiesX.append(0)
        enemiesY.append(i)
    enemyShotsX = []
    enemyShotsY = []
    shipShotX = -1
    print("Start Space Invaders.")
    showBattlefield()
    time.sleep(3)

    levelCounter = 1
    moveCounter = 0
    timeCounter = 0

    #HAUPTSCHLEIFE EINES LEVELS
    while finish == False:
        #Zufällig neuen Schuss hinzufügen
        rng = random.randint(0, 10)
        if rng == 1:
            newPos = random.randint(0, len(enemiesX) - 1)
            enemyShotsX.append(enemiesX[newPos])
            enemyShotsY.append(enemiesY[newPos])

        #Alle 10 Sekunden Gegner runterrücken
        if moveCounter == 180:
            for i in range (len(enemiesX)):
                enemiesX[i] = enemiesX[i] + 1
                if enemiesX[i] == 9:
                    finish = True
            moveCounter = 0
        
        #Eigenen Schuss, falls vorhanden, nach oben setzen und auf Gegner prüfen
        if (shipShotX != -1):
            shipShotX = shipShotX - 1
            if (shipShotX != -1):
                for i in range(len(enemiesX)):
                    if shipShotX == enemiesX[i] and shipShotY  == enemiesY[i]:
                        del enemiesX[i]
                        del enemiesY[i]
                        shipShotX = -1
                        counter = counter + 1
                        #Falls alle Gegner weg: neues Level starten
                        if len(enemiesX) == 0:
                            unbindSpaceKeys()
                            showBattlefield()
                            time.sleep(0.5)
                            if levelCounter % 2 == 0:
                                beatenTheBoss = bossLevel(levelCounter)
                                if beatenTheBoss == False:
                                    finish = True
                                    break
                                else:
                                    counter = counter + 25*levelCounter
                            levelCounter = levelCounter + 1
                            showText("level" + (str)(levelCounter))
                            enemiesX = []
                            enemiesY = []
                            for i in range (((levelCounter-1)%9)+1):
                                for j in range (11):
                                    enemiesX.append(i)
                                    enemiesY.append(j)
                            enemyShotsX = []
                            enemyShotsY = []
                            shipShotX = -1
                            moveCounter = 0
                            showBattlefield()
                            time.sleep(3)
                            bindSpaceKeys()
                        break
                    
        #Gegnerische Schüsse runtersetzen und prüfen
        if timeCounter == 2:
            newPositionsX = []
            newPositionsY = []
            for i in range (len(enemyShotsX)):
                #Check, ob Schuss jetzt rausfällt
                if (enemyShotsX[i] != 9):
                    #Fällt nicht raus: 1 runter, dem neuen Array hinzufügen, und checken, ob Schiff getroffen
                    newPositionsX.append(enemyShotsX[i] + 1)
                    newPositionsY.append(enemyShotsY[i])
                    if (enemyShotsX[i]+1 == 9) and (enemyShotsY[i] == shipY):
                        finish = True
                        break
            enemyShotsX = newPositionsX
            enemyShotsY = newPositionsY
            timeCounter = 0   

        #Neues Spielfeld anzeigen
        showBattlefield()
        timeCounter = timeCounter + 1
        moveCounter = moveCounter + 1
        time.sleep(0.05)

    unbindSpaceKeys()
    
    
    if (counter > config.getint('sonstiges_section', 'spacescore')):
        trophy = []
        trophy.extend((matrix[1][3], matrix[1][4], matrix[1][5], matrix[1][6], matrix[1][7], matrix[2][2], matrix[2][3], matrix[2][7], matrix[2][8] ))
        trophy.extend((matrix[3][2], matrix[3][3], matrix[3][7], matrix[3][8], matrix[4][2], matrix[4][3], matrix[4][7], matrix[4][8]))
        trophy.extend((matrix[5][3], matrix[5][7], matrix[6][3], matrix[6][7], matrix[7][4], matrix[7][5], matrix[7][6], matrix[8][5]))
        trophy.extend((matrix[9][3], matrix[9][4], matrix[9][5], matrix[9][6], matrix[9][7], matrix[3][1], matrix[3][9]))
        turnOnLEDs(strip, trophy)
        time.sleep(5)
        config.set('sonstiges_section', 'spacescore', counter)
        with open('/home/pi/Schreibtisch/Python/WordClock/wordclock_cfg.cfg', 'wb') as configfile:
            config.write(configfile)
    score = str(counter)
    scoreShow = " " + score
    showText(scoreShow)
    print("Space Invaders fertig. Deine Punktzahl: " + score)
    deleteEntries()
    proceed(strip)
    busy = False

#Bosslevel
def bossLevel(life):
    global shipY
    global enemiesX
    global enemiesY
    global enemyShotsX
    global enemyShotsY
    global shipShotX
    global shipShotY
    global finish
    global BOSSCOLOR
    BOSSCOLOR = Color(255,255,255)
    bossIntro()
    enemiesX = [0,0,0,0,0,1,1,1,1,1,2,2,2,2,2]
    enemiesY = [3,4,5,6,7,3,4,5,6,7,3,4,5,6,7]
    enemyShotsX = []
    enemyShotsY = []
    shipShotX = -1
    timeCounter = 0
    lifeCounter = 15 + 5*(life-2)
    attackActive = False
    finish = False
    stompy = False
    showBossfield()
    time.sleep(1)

    while finish == False:
        #Zufällige Bewegung des Bosses
        if (timeCounter % 5 == 0) and (stompy == False):
            movement = random.randint(0,2)
            if (movement == 0) and (enemiesY[0] != 0):
                for i in range (len(enemiesY)):
                    enemiesY[i] = enemiesY[i] - 1
            elif (movement == 2) and (enemiesY[14] != 10):
                for i in range (len(enemiesY)):
                    enemiesY[i] = enemiesY[i] + 1

        #Zufällig Stampattacke beginnen
        if ((life >= 4) and (attackActive == False) and (random.randint(0,30) == 1)):
            stompy = True
            stompyCounter = 0
            attackActive = True
            
        #Stampf-Attacke ausführen
        if (stompy == True):
            if stompyCounter < 10:
                BOSSCOLOR = Color(255,0,255)
            elif stompyCounter < 17:
                for i in range (len(enemiesX)):
                    enemiesX[i] = enemiesX[i] + 1
                for i in range (len(enemiesX)):
                    if enemiesX[i] == 9 and enemiesY[i] == shipY:
                        showBossfield()
                        time.sleep(1)
                        return False
            elif stompyCounter < 26:
                for i in range (len(enemiesX)):
                    if enemiesX[i] == 9 and enemiesY[i] == shipY:
                        showBossfield()
                        time.sleep(1)
                        return False
            elif stompyCounter > 25 and stompyCounter < 33:   
                for i in range (len(enemiesX)):
                    enemiesX[i] = enemiesX[i] - 1
            elif stompyCounter == 33:
                BOSSCOLOR = Color(255,255,255)
                stompy = False
                stompyCounter = 0
                attackActive = False
            stompyCounter += 1
                    
        #Zufällig Schuss-Attacke beginnen
        if ((attackActive == False) and (random.randint(0,5) == 1)):
            attackActive = True
            #3 Schüsse
            enemyShotsX = [2,2,2]
            enemyShotsY = range(enemiesY[1], enemiesY[4])
            #5 Schüsse
            #enemyShotsX = [2,2,2,2,2]
            #enemyShotsY = range(enemiesY[0], enemiesY[4]+1)
            
        #Eigenen Schuss, falls vorhanden, nach oben setzen und auf Gegner prüfen
        if (shipShotX != -1):
            shipShotX = shipShotX - 1
            if (shipShotX != -1):
                for i in range(len(enemiesX)):
                    if shipShotX == enemiesX[i] and shipShotY == enemiesY[i]:
                        lifeCounter = lifeCounter - 1
                        shipShotX = -1
                        #Blinken
                        for i in range(len(enemiesX)):
                            strip.setPixelColor(matrix[enemiesX[i]][enemiesY[i]], Color(0,0,0))
                        strip.show()
                        time.sleep(0.01)
                        #Falls alle Leben weg: Ende Bosslevel
                        if lifeCounter == 0:
                            unbindSpaceKeys()
                            showBossfield()
                            time.sleep(0.5)
                            enemyShotsX = []
                            enemyShotsY = []
                            for j in range(2):
                                for i in range(len(enemiesX)):
                                    strip.setPixelColor(matrix[enemiesX[i]][enemiesY[i]], Color(0,0,0))
                                strip.show()
                                time.sleep(0.5)
                                showBossfield()
                                time.sleep(0.5)
                            for i in range(len(enemiesX)):
                                strip.setPixelColor(matrix[enemiesX[i]][enemiesY[i]], Color(0,0,0))
                            strip.show()
                            time.sleep(0.5)
                            return True
        #Gegnerische Schüsse runtersetzen und prüfen
        if timeCounter % 2 == 0:
            newPositionsX = []
            newPositionsY = []
            for i in range (len(enemyShotsX)):
                #Check, ob Schuss jetzt rausfällt
                if (enemyShotsX[i] != 9):
                    #Fällt nicht raus: 1 runter, dem neun Array hinzufügen, und Check, ob Schiff getroffen        
                    newPositionsX.append(enemyShotsX[i] + 1)
                    newPositionsY.append(enemyShotsY[i])
                    if (enemyShotsX[i]+1 == 9) and (enemyShotsY[i] == shipY):
                        return False
            enemyShotsX = newPositionsX
            enemyShotsY = newPositionsY
            if (stompy == False) and (len(enemyShotsX) == 0):
                attackActive = False  

        #Neues Spielfeld anzeigen
        showBossfield()
        timeCounter = timeCounter + 1
        time.sleep(0.05)
    return False
    

###Hilfsfunktionen für Space Invaders, die durch Tastendruck ausgelöst werden (Bewegung, Schuss und beenden)###
def moveLeft(event):
    global shipY
    global enemyShotsX
    global enemyShotsY
    global finish
    if shipY > 0:
        shipY = shipY - 1
        #showBattlefield()
        strip.setPixelColor(matrix[9][shipY], Color(255,0,0))
        for i in range (len(enemyShotsX)):
            if (enemyShotsX[i] == 9) and (enemyShotsY[i] == shipY):
                finish = True
        
    
def moveRight(event):
    global shipY
    global enemyShotsX
    global enemyShotsY
    global finish
    if shipY < 10:
        shipY = shipY + 1
        #showBattlefield()
        strip.setPixelColor(matrix[9][shipY], Color(255,0,0))
        for i in range (len(enemyShotsX)):
            if (enemyShotsX[i] == 9) and (enemyShotsY[i] == shipY):
                finish = True
    
def shoot(event):
    global shipShotX
    global shipShotY
    global shipY
    if shipShotX == -1:
        shipShotX = 9
        shipShotY = shipY

def end(event):
    global finish
    finish = True

###Weitere Hilfsfunktionen für Space Invaders: Spielfeld anzeigen, Bossintro, Keybinds an/aus###
def showBattlefield():
    global shipY
    global enemiesX
    global enemiesY
    global enemyShotsX
    global enemyShotsY
    global shipShotX
    global shipShotY
    clear(strip)
    for i in range(len(enemiesX)):
        strip.setPixelColor(matrix[enemiesX[i]][enemiesY[i]], Color(0,255,0))
    for i in range(len(enemyShotsX)):
        strip.setPixelColor(matrix[enemyShotsX[i]][enemyShotsY[i]], Color(80,255,0))
    strip.setPixelColor(matrix[9][shipY], Color(255,0,0))
    if shipShotX != -1:
        strip.setPixelColor(matrix[shipShotX][shipShotY], Color(255,0,255))
    strip.show()

def showBossfield():
    global shipY
    global enemiesX
    global enemiesY
    global enemyShotsX
    global enemyShotsY
    global shipShotX
    global shipShotY
    global BOSSCOLOR
    clear(strip)
    for i in range(len(enemiesX)):
        strip.setPixelColor(matrix[enemiesX[i]][enemiesY[i]], BOSSCOLOR)
    strip.setPixelColor(matrix[enemiesX[6]][enemiesY[6]], Color(0,255,0))
    strip.setPixelColor(matrix[enemiesX[8]][enemiesY[8]], Color(0,255,0))
    for i in range(len(enemyShotsX)):
        strip.setPixelColor(matrix[enemyShotsX[i]][enemyShotsY[i]], Color(80,255,0))
    strip.setPixelColor(matrix[9][shipY], Color(255,0,0))
    if shipShotX != -1:
        strip.setPixelColor(matrix[shipShotX][shipShotY], Color(255,0,255))
    strip.show()

def bossIntro():
    unbindSpaceKeys()
    clear(strip)
    strip.setPixelColor(matrix[9][shipY], Color(255,0,0))
    strip.show()
    time.sleep(2)
    enemiesX = [0,0,0,0,0]
    enemiesY = [3,4,5,6,7]
    for i in range(len(enemiesX)):
        strip.setPixelColor(matrix[enemiesX[i]][enemiesY[i]], Color(255,255,255))
    strip.show()
    time.sleep(1.5)
    
    enemiesX = [0,0,0,0,0,1,1,1,1,1]
    enemiesY = [3,4,5,6,7,3,4,5,6,7]
    for i in range(len(enemiesX)):
        strip.setPixelColor(matrix[enemiesX[i]][enemiesY[i]], Color(255,255,255))
    strip.setPixelColor(matrix[enemiesX[1]][enemiesY[1]], Color(0,255,0))
    strip.setPixelColor(matrix[enemiesX[3]][enemiesY[3]], Color(0,255,0))
    strip.show()
    time.sleep(1.5)

    enemiesX = [0,0,0,0,0,1,1,1,1,1,2,2,2,2,2]
    enemiesY = [3,4,5,6,7,3,4,5,6,7,3,4,5,6,7]
    for i in range(len(enemiesX)):
        strip.setPixelColor(matrix[enemiesX[i]][enemiesY[i]], Color(255,255,255))
    strip.setPixelColor(matrix[enemiesX[6]][enemiesY[6]], Color(0,255,0))
    strip.setPixelColor(matrix[enemiesX[8]][enemiesY[8]], Color(0,255,0))
    strip.show()
    time.sleep(1.5)
    bindSpaceKeys()


def bindSpaceKeys():
    master.bind("a", moveLeft)
    master.bind("d", moveRight)
    master.bind("<space>", shoot)
    master.bind("x", end)

def unbindSpaceKeys():
    master.unbind("a")
    master.unbind("d")
    master.unbind("<space>")
    master.unbind("x")

#Löscht den Inhalt aus sämtlichen Eingabefenstern, da oft während Spielen reingeschrieben wird.
def deleteEntries():
    time_entry.delete(0,END)
    time_entry2.delete(0,END)
    input_text.delete(0,END)


###FUNKTIONEN, DIE MIT DEM MENÜ UND DEN EINSTELLUNGEN ZUSAMMENHÄNGEN###

#Speichert die aktuellen Einstellungen in der .cfg-Datei
def saveConfig():
    global morningHour
    global morningMinutes
    global nightHour
    global nightMinutes
    global NIGHTCOLOR
    config.set('times_section', 'morninghour', morningHour)
    config.set('times_section', 'morningminutes', morningMinutes)
    config.set('times_section', 'nighthour', nightHour)
    config.set('times_section', 'nightminutes', nightMinutes)
    config.set('checkbox_section', 'schwabe', varMystery.get())
    config.set('checkbox_section', 'stündlichzufall', varRandom.get())
    config.set('checkbox_section', 'morgenszufall', varMorning.get())
    config.set('checkbox_section', 'nachtmodus', varNightmode.get())
    config.set('sonstiges_section', 'sliderspeed', slider_delay.get())
    config.set('nachtfarbe_section', 'grün', (NIGHTCOLOR & BITMASK_GREEN) >> 16)
    config.set('nachtfarbe_section', 'rot', (NIGHTCOLOR & BITMASK_RED) >> 8)
    config.set('nachtfarbe_section', 'blau', (NIGHTCOLOR & BITMASK_BLUE))

    with open('/home/pi/Schreibtisch/Python/WordClock/wordclock_cfg.cfg', 'wb') as configfile:
        config.write(configfile)

#Setzt die Einstellungen auf Standard zurück
def resetConfig():
    global morningHour
    global morningMinutes
    global nightHour
    global nightMinutes
    global NIGHTCOLOR
    config.set('times_section', 'morninghour', 7)
    config.set('times_section', 'morningminutes', 0)
    config.set('times_section', 'nighthour', 23)
    config.set('times_section', 'nightminutes', 0)
    config.set('checkbox_section', 'schwabe', 0)
    config.set('checkbox_section', 'stündlichzufall', 0)
    config.set('checkbox_section', 'morgenszufall', 0)
    config.set('checkbox_section', 'nachtmodus', 1)
    config.set('sonstiges_section', 'sliderspeed', 0.15)
    config.set('nachtfarbe_section', 'grün', 20)
    config.set('nachtfarbe_section', 'rot', 50)
    config.set('nachtfarbe_section', 'blau', 0)

    with open('/home/pi/Schreibtisch/Python/WordClock/wordclock_cfg.cfg', 'wb') as configfile:
        config.write(configfile)

#Zeigt die aktuell in der .cfg-Datei gespeicherten Einstellungen an
def showConfig():
    info_text= """Nachtfarbe: """+str(config.getint('nachtfarbe_section', 'rot'))+""", """+str(config.getint('nachtfarbe_section', 'grün'))+""", """+str(config.getint('nachtfarbe_section', 'blau'))+"""
    \nMorgenzeit: """+str(config.getint('times_section', 'morninghour'))+""":"""+str(config.getint('times_section', 'morningminutes'))+"""
    \nNachtzeit: """+str(config.getint('times_section', 'nighthour'))+""":"""+str(config.getint('times_section', 'nightminutes'))+"""
    \nSnake Highscore: """+str(config.getint('sonstiges_section', 'highscore'))+"""
    \nTetris Highscore: """+str(config.getint('sonstiges_section', 'tetrisscore'))+"""
    \nSpace Invaders Highscore: """+str(config.getint('sonstiges_section', 'spacescore'))
    tkMessageBox.showinfo(message=info_text, title="Aktuelle Einstellungen")   

#Zeigt das Impressum an
def about():
    info_text= "**************\nAuthor: Marc Jenne\nVersion: 3.7\n**************"
    tkMessageBox.showinfo(message=info_text, title="About")

#Diese und die folgenden Funktionen zeigen die verschiedenen Hilfefenster an
def anleitung_farbe():
    info_text= """Die Farbe der Uhr kann über mehrere Möglichkeiten eingestellt werden.
    \nVisuell: klick auf den Button "Visuell wählen". Anschließend öffnet sich ein Pop-Up, in dem du die Farbe auswählen kannst. Bestätige deine Auswahl mit Ok.
    \nSlider: Mithilfe der drei Slider kannst du die Farbe einstellen, indem du den Rot-, Grün- und Blauwert einstellst und dies mit dem Button daneben aktivierst.
    \nPresets: Die Presets beinhalten eine Liste voreingestellter Farben. Wähle über die Liste eine aus.
    \nMit dem Button "Random totally" wird eine zufällige Farbe gesetzt. Mit dem Button "Zufall aus Presets" wird eine Farbe aus den Presets gesetzt.
    \nRainbow: Drücke den Button "Rainbow" und halte ihn. Solange er gedrückt bleibt, ändert sich die Farbe der Uhr durchgehend über das gesamt Spektrum. Sobald du den Knopf loslässt, wird die zu diesem Zeitpunkt gezeigte Farbe gesetzt und aktiviert.
    \nDimmen: Mit diesem Button wird die gewählte Farbe der Uhr in 4 Stufen gedimmt."""
    tkMessageBox.showinfo(message=info_text, title="Farbe ändern")

def anleitung_spiele():
    info_text= """Auf der Uhr kannst du auch das gute alte Retro-Spiele zocken :) Klicke dazu einfach die entsprechenden Button, um eine Runde zu starten.\n
    \nSnake: Auf der Uhr erscheint deine Schlange: der Kopf ist Orange, der Körper grün. Das Ziel des Spiels ist es, das rote Futter zu fressen. Sobald du eines frisst, wächst deine Schlange und ein weiteres Futter taucht auf. Das Spiel endet, sobald der Kopf der Schlange in ihrem Körper landet, du dich also selbst beißt.
Steuerung: zu Beginn musst du in das Textfeld klicken (ein "w" taucht dort von alleine auf). Nun steuerst du die Schlange mit den Tasten WASD. Du kannst auch durch die Wände, dann taucht die Schlange am gegenüberliegenden Rand auf.
    \nTetris: Es ist Tetris, die Regeln kennt man ja. Vervollständige Reihen, um sie aufzulösen und Punkte zu erhalten. Löst du mit einem Teil mehrere Reihen gleichzeitig auf, erhältst du Bonuspunkte.
Steuerung: mit ASD bewegst du die Blöcke nach rechts, links oder unten (falls es dir zu langsam geht). Mit Q und E drehst du die Blöcke links- bzw rechtsrum (alternativ kannst du auch W benutzen), mit Leertaste wird Tetris pausiert.
    \nSpace Invaders: Bei Space Invaders steuerst du das kleine grüne Schiff nach rechts und links und schießt die roten Gegner ab, ohne selbst von diesen getroffen zu werden. Erreicht ein Gegner den unteren Rand, ist das Spiel ebenfalls vorbei.
Steuerung: Mit AD bewegst du dich nach links und rechts, mit Leertaste schießt du (es kann immer nur ein Schuss aktiv sein).
    \n\nNach einer beendeten Spielrunde wird deine Punktzahl angezeigt. Falls du einen neuen Highscore erreicht hast, erscheint ein Pokal.
WICHTIG: drücke auf der Uhr nichts anderes, bevor Snake beendet ist und wieder die Uhrzeit angezeigt wird."""
    tkMessageBox.showinfo(message=info_text, title="Snake spielen")

def anleitung_text():
    info_text= """Auf der Uhr kannst du Texte anzeigen lassen. Gib dazu den gewünschten Text in das Feld ein und klicke auf "Text durchlaufen". Mit dem Slider kannst du auswählen, wie schnell der Text läuft; das kann auch während dem Durchlauf geändert werden.
    \nWenn die Checkbox unter dem Textfeld aktiviert ist, läuft der Text wiederholt durch, und zwar solange, bis du die Checkbox deaktivierst: dann läuft nur noch der aktuelle Durchgang zuende.
    \nUnterstützte Zeichen sind A-Z, Umlaute, ,!?# und 0-9.
    \nWICHTIG: drücke auf der Uhr nichts anderes, bevor das Durchlaufen des Textes beendet ist und wieder die Uhrzeit angezeigt wird."""
    tkMessageBox.showinfo(message=info_text, title="Text durchlaufen lassen")

def anleitung_config():
    info_text= """Über das Menü kannst du deine Einstellungen speichern oder auf den Standard zurücksetzen. Das hat zur Folge, dass deine Einstellungen bei einem Neustart oder einer neuen Software-Version beibehalten werden. Gespeichert werden deine Nachtfarbe, die Morgen- und Nachtzeit, die Checkboxen und die Spiele-Highscores.
    \nDie aktuellen Einstellungen kannst du dort auch ansehen, falls du z.B. die Nachtzeit vergessen hast."""
    tkMessageBox.showinfo(message=info_text, title="Einstellungen speichern und zurücksetzen")

def anleitung_zeiten():
    info_text= """Die Uhr verfügt über einen Tag-Nacht-Modus: darüber kannst du einstellen, ob abends/nachts eine andere, z.B. stark gedimmte, Farbe eingestellt werden soll. Dieser Modus kann aber mit der entsprechenden Checkbox auch deaktiviert werden.
    \nDie Nachtzeit gibt an, ab wann die Nachtfarbe aktiviert wird, die Morgenzeit dagegen, wann morgens wieder die ursprüngliche Farbe aktiviert wird. Um diese beiden Zeiten einzustellen, gib in den Textfeldern im Format HH:MM die gewünschte Zeit ein und bestätige sie mit dem Button.
    \nNachtfarbe einstellen: der Button "Nachtfarbe setzen" legt die Nachtfarbe auf die gerade aktive Farbe fest.
    \nMit den Checkboxen "Stündlich Zufall" und "Morgens Zufall" kannst du auswählen, ob jede Stunde bzw morgens (zur gewählten Morgenzeit) eine Farbe zufällig aus den Presets gesetzt werden soll. Ist letzteres deaktiviert, geht morgens die Farbe an, die vorm Aktivieren der Nachtfarbe aktiv war."""
    tkMessageBox.showinfo(message=info_text, title="Nacht- und Morgenzeit setzen")

def anleitung_weiteres():
    info_text= """Mit den anderen Buttons kannst du Animationen oder spezielle Anzeigen starten, probier dich einfach durch. Bei all diesen Animationen geht die Uhr von alleine weiter, entweder wenn die Animation vorbei ist oder wenn eine Minute endet.
    \nMit der Checkbox "Schwabe" kannst du aktivieren und deaktivieren, ob die Uhr die Uhrzeit für normale Menschen anzeigt oder für Schwaben."""
    tkMessageBox.showinfo(message=info_text, title="Sonstiges")




###DAS HAUPTPROGRAMM##
def myMain():
    global arrayLEDs
    global COLORS
    global COLOR
    global COLORCOPY
    global NIGHTCOLOR
    global morningHour
    global morningMinutes
    global nightHour
    global nightMinutes
    
    print("START")
    buildMatrix()
    morningHour=config.getint('times_section', 'morningHour')
    morningMinutes=config.getint('times_section', 'morningMinutes')
    nightHour=config.getint('times_section', 'nightHour')
    nightMinutes=config.getint('times_section', 'nightMinutes')
    MORNING = Color(0, 255, 0)
    NIGHTCOLOR = Color(config.getint('nachtfarbe_section', 'grün'), config.getint('nachtfarbe_section', 'rot'), config.getint('nachtfarbe_section', 'blau'))
    nightmodeActive=False
    randomFromPreset()

    ###HAUPTSCHLEIFE###
    while(True):
        try:
            ti = datetime.datetime.now()
            hour = ti.hour
            minute = ti.minute
            second = ti.second
            strTime = "Uhrzeit: "+datetime.datetime.now().strftime('%H:%M:%S')
            actualTime.config(text=strTime)
            strColor = "Farbe: "+str((COLOR & BITMASK_RED) >> 8) +", "+ str((COLOR & BITMASK_GREEN) >> 16) +", "+ str(COLOR & BITMASK_BLUE)
            actualColor.config(text=strColor)
            if (second == 0):
                #Im Folgenden einige besondere Stunden, bei denen die Farbe gewechselt wird
                if varNightmode.get() == 1 and hour == nightHour and minute == nightMinutes:
                    #HIER NACHTFARBE
                    MORNING = COLOR
                    COLOR = NIGHTCOLOR
                    COLORCOPY = NIGHTCOLOR
                    nightmodeActive=True
                elif varNightmode.get() == 1 and hour == morningHour and minute == morningMinutes:
                    #HIER MORGENFARBE
                    COLOR = MORNING
                    COLORCOPY = MORNING
                    if varMorning.get() == 1:
                        randomFromPreset()
                    nightmodeActive=False
                elif minute == 0 and varRandom.get() == 1 and nightmodeActive == False:
                    COLOR = COLORS[random.randint(0,len(COLORS)-1)]
                    COLORCOPY = COLOR

                if varCheckBinary.get() == 0:
                    arrayLEDs = calculateArray(hour, minute)
                else:
                    year = ti.year
                    month = ti.month
                    day = ti.day
                    arrayLEDs = calculateArrayBinary(year, month, day, hour, minute, second)
                if (busy == False):
                    turnOnLEDs(strip, arrayLEDs)
            time.sleep(1)

        except KeyboardInterrupt:
            print("INTERRUPT")

################################################################
#BEGIN MAIN
master = Tk()
master.geometry("+90+100")
master.title("Wordclock")
GPIO.setmode(GPIO.BCM)
config = ConfigParser.RawConfigParser()
config.read('/home/pi/Schreibtisch/Python/WordClock/wordclock_cfg.cfg')
preset = preset()

#BUILD FRAME
visual_button = Button(master, text="Farbe visuell wählen", command = chooseVisual)
dimm_button = Button(master, text="Farbe dimmen", command = dimmColor)
matrix_button = Button(master, text="Matrix", command = matrix)
circle_button = Button(master, text="Cooooool", command = circle)
smiley_button = Button(master, text="Smile :)", command = smiley)
heart_button = Button(master, text="Liebe für alle <3", command = heart)
exit_button = Button(master, text="Beenden", command = master.quit)
randomPreset_button = Button(master, text="Zufall aus Preset", command = randomFromPreset)
randomTotally_button = Button(master, text="Random totally", command = randomTotally)
input_text=Entry(master)
text_button = Button(master, text="Text duchlaufen", command = showInput)
slider_delay = Scale(master, from_=0.01, to=0.5, orient=HORIZONTAL, length=200, resolution=0.01)
slider_delay.set(config.getfloat('sonstiges_section', 'sliderspeed'))
variable = StringVar(master)
variable.set("0-Rot")
preset_menu = OptionMenu(master, variable, *preset, command=chooseFromPreset)
preset_label = Label(master, text="Presets:")
slider_red = Scale(master, from_=0, to=255, orient=HORIZONTAL, length=200, troughcolor="red", command=chooseFromSliders2)
slider_green = Scale(master, from_=0, to=255, orient=HORIZONTAL, length=200, troughcolor="green", command=chooseFromSliders2)
slider_blue = Scale(master, from_=0, to=255, orient=HORIZONTAL, length=200, troughcolor="blue", command=chooseFromSliders2)
slider_button=Button(master, text="Farbe der Slider setzen", command=chooseFromSliders)
label=Label(master, text="Wordclock GUI", fg="red",bg="black",font="Times 20")
actualTime=Label(master, text="Start", fg="light green", bg="black", font="Times 15")
actualColor=Label(master, text="Start", fg="yellow", bg="black", font="Times 15")
varMystery = IntVar(value=config.getint('checkbox_section', 'schwabe'))
mystery = Checkbutton(command=changeLanguage, variable=varMystery, text="OMG ein Schwabe!", fg="red", cursor="spider")
varRandom = IntVar(value=config.getint('checkbox_section', 'stündlichzufall'))
check_random = Checkbutton(variable=varRandom, text="Stündlich Zufall", fg="red")
snake_button = Button(master, text="Snake", command = startSnake)
varCheckLoop = IntVar()
check_loop = Checkbutton(variable=varCheckLoop, text="Show. Read. Repeat.")
varMorning = IntVar(value=config.getint('checkbox_section', 'morgenszufall'))
check_morning = Checkbutton(variable=varMorning, text="Morgens Zufall", fg="red")
varNightmode = IntVar(value=config.getint('checkbox_section', 'nachtmodus'))
check_nightmode = Checkbutton(variable=varNightmode, text="Nachtmodus einschalten", fg="red")
time_entry=Entry(master, width=12)
time_label=Label(master, text="Morgenbeginn:")
time_button=Button(master, text="Zeit setzen", command = setMorningTime)
time_entry2=Entry(master, width=12)
time_label2=Label(master, text="Nachtbeginn:")
time_button2=Button(master, text="Zeit setzen", command = setNightTime)
nightcolor_button=Button(master, text="Nachtfarbe setzen", command = setNightcolor)
rainbow_button=Button(master, text="Rainbow")
rainbow_button.bind('<ButtonPress-1>', startRainbow)
rainbow_button.bind('<ButtonRelease-1>', stopRainbow)
varCheckBinary = IntVar()
check_binary = Checkbutton(variable=varCheckBinary, text="Binäre Uhr")
dark_button=Button(master, text="Farbe ausschalten", command = dark)
tetris_button=Button(master, text="Tetris", command = startTetris)
space_button=Button(master, text="Space Invaders", command = startSpaceInvaders)
pacman_button=Button(master, text = "PacMan", command = startPacman)

c1=1
c2=3
c3=5

#SEPARATORS
ttk.Separator(master, orient=HORIZONTAL).grid(row=0, column=0, columnspan=10, sticky='ew', pady=20, padx=20)
ttk.Separator(master, orient=HORIZONTAL).grid(row=2, column=0, columnspan=10, sticky='ew', pady=20, padx=20)
ttk.Separator(master, orient=HORIZONTAL).grid(row=7, column=0, columnspan=10, sticky='ew', pady=20, padx=20)
ttk.Separator(master, orient=HORIZONTAL).grid(row=10, column=0, columnspan=10, sticky='ew', pady=20, padx=20)
ttk.Separator(master, orient=HORIZONTAL).grid(row=14, column=0, columnspan=10, sticky='ew', pady=20, padx=20)
ttk.Separator(master, orient=HORIZONTAL).grid(row=17, column=0, columnspan=10, sticky='ew', pady=20, padx=20)
ttk.Separator(master, orient=HORIZONTAL).grid(row=19, column=0, columnspan=10, sticky='ew', pady=20, padx=20)
ttk.Separator(master, orient=VERTICAL).grid(row=0, column=0, rowspan=30, sticky='ns', pady=20, padx=(20,10))
ttk.Separator(master, orient=VERTICAL).grid(row=0, column=c3+1, rowspan=30, sticky='ns', pady=20, padx=20)
ttk.Separator(master, orient=VERTICAL).grid(row=2, column=c2+1, rowspan=30, sticky='ns', pady=20, padx=20)
ttk.Separator(master, orient=VERTICAL).grid(row=14, column=c1+1, rowspan=4, sticky='ns', pady=20, padx=20)


#ERSTE SPALTE
slider_red.grid(row=3, column=c1, padx=20)
slider_green.grid(row=4, column=c1)
slider_blue.grid(row=5, column=c1)
preset_menu.grid(row=6, column=c1, pady=(20, 0), padx=20, sticky='e')
preset_label.grid(row=6, column=c1, pady=(20, 0), padx=20, sticky='w')
input_text.grid(row=8, column=c1)
slider_delay.grid(row=9, column=c1)
time_label.grid(row=11, column=c1, sticky='w', padx=20)
time_entry.grid(row=11, column=c1, sticky='e', padx=20)
time_label2.grid(row=12, column=c1, sticky='w', padx=20)
time_entry2.grid(row=12, column=c1, sticky='e', padx=20)
nightcolor_button.grid(row=13, column=c1, pady=(10, 0))
space_button.grid(row=15, column=c1, pady=(20, 0), padx=(20, 0) ,sticky = 'w')
pacman_button.grid(row=15, column=c1, pady=(20, 0), padx=(0, 20), sticky = 'e')
#check_binary.grid(row=16, column=c1, pady=(20, 0), sticky = 'w')
tetris_button.grid(row=16, column=c1, pady=(20, 0), padx=(0, 20), sticky = 'e')
snake_button.grid(row=16, column=c1, pady=(20, 0), padx=(20, 0) ,sticky = 'w')
actualTime.grid(row=18, column=c1, sticky='n')

#ZWEITE SPALTE
label.grid(row=1, column=c2, columnspan=1)
slider_button.grid(row=3, column=c2, rowspan=3,sticky='ns')
randomPreset_button.grid(row=6, column=c2, pady=(20, 0))
text_button.grid(row=8, column=c2)
check_loop.grid(row=9, column=c2)
time_button.grid(row=11, column=c2)
time_button2.grid(row=12, column=c2)
check_nightmode.grid(row=13, column=c2)
matrix_button.grid(row=15, column=c2)
circle_button.grid(row=16, column=c2, pady=(10, 0))
actualColor.grid(row=18, column=c2, sticky='n')

#DRITTE SPALTE
rainbow_button.grid(row=3, column=c3)
randomTotally_button.grid(row=4, column=c3)
visual_button.grid(row=5, column=c3)
dimm_button.grid(row=6, column=c3, sticky='n', pady=(5, 30))
dark_button.grid(row=6, column=c3, sticky='s')
check_morning.grid(row=11, column=c3)
check_random.grid(row=12, column=c3)
mystery.grid(row=13, column=c3)
smiley_button.grid(row=15, column=c3, pady=(0, 10))
heart_button.grid(row=16, column=c3)
exit_button.grid(row=18, column=c3)

#MENU
menuleiste=Menu(master)
datei_menu=Menu(menuleiste, tearoff=0)
datei_menu.add_command(label="Einstellungen speichern", command=saveConfig)
datei_menu.add_command(label="Einstellungen zurücksetzen", command=resetConfig)
datei_menu.add_command(label="Einstellungen anzeigen", command=showConfig)
help_menu=Menu(menuleiste, tearoff=0)
anleitungen=Menu(help_menu, tearoff=0)
anleitungen.add_command(label="Farbe ändern", command=anleitung_farbe)
anleitungen.add_command(label="Text durchlaufen lassen", command=anleitung_text)
anleitungen.add_command(label="Nacht- und Morgenzeit setzen", command=anleitung_zeiten)
anleitungen.add_command(label="Einstellungen speichern und zurücksetzen", command=anleitung_config)
anleitungen.add_command(label="Spielautomat", command=anleitung_spiele)
anleitungen.add_command(label="Weitere Funktionen", command=anleitung_weiteres)
help_menu.add_cascade(label="Anleitungen", menu=anleitungen)
help_menu.add_command(label="About", command=about)

menuleiste.add_cascade(label="Datei",menu=datei_menu)
menuleiste.add_cascade(label="Hilfe",menu=help_menu)

master.config(menu=menuleiste)

####################
#Streifen initialisieren
strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
strip.begin()

COLOR = Color(0,255,0)
COLORCOPY = Color(0,255,0)
d=0
busy = False
abschnitt = 0

#Knöpfe aktivieren: #vor den folgenden Zeilen entfernen
#GPIO.setup(BUTTONCHANGE, GPIO.IN, pull_up_down = GPIO.PUD_UP)
#GPIO.add_event_detect(BUTTONCHANGE, GPIO.FALLING, callback=changeRainbow, bouncetime=300)
#GPIO.setup(BUTTONDIMM, GPIO.IN, pull_up_down = GPIO.PUD_UP)
#GPIO.add_event_detect(BUTTONDIMM, GPIO.FALLING, callback=dimm, bouncetime=300)
#GPIO.setup(BUTTONDIMMALL, GPIO.IN, pull_up_down = GPIO.PUD_UP)
#GPIO.add_event_detect(BUTTONDIMMALL, GPIO.FALLING, callback=dimmAll, bouncetime=2500)

######################################################
#MAIN
thread.start_new_thread(myMain, ())
master.mainloop()


