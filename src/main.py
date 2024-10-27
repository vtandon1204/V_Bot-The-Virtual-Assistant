import speech_recognition as sr
import os
import time
import pyttsx3
import webbrowser
import numpy as np
import keyboard # type: ignore
import subprocess as sp
import openai
import sys

from decouple import Config, RepositoryEnv
from datetime import datetime
from random import choice
from conv import random_text
from online import find_my_id, search_on_google, search_on_wikipedia, youtube

# *** Setting up the voice engine ***
engine = pyttsx3.init('sapi5') 
# pyttsx3 converts the given text into speech
# sapi5 is microsoft speech api used for speech recognition
engine.setProperty('volume', 2)
engine.setProperty('rate', 180)
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)
# voices[0] --> male assistant voice
# voices[1] --> female assistant voice


# *** Loading the configurations ***
config = Config(RepositoryEnv(r"config\.env"))
USER = config('USER')
HOSTNAME = config('BOT')


# *** Starting & Stopping listening ***
listening = False
def start_listening():
    global listening
    listening = True
    print("Started Listening...")
def pause_listening():
    global listening
    listening = False
    print("Stopped Listening...")
keyboard.add_hotkey('ctrl+alt+v', start_listening)
keyboard.add_hotkey('ctrl+alt+p', pause_listening)


def say(text):
    print(f"Saying: {text}")  # Debug line to verify the text
    engine.say(text)
    engine.runAndWait()

def greet_me():
    hour = datetime.now().hour

    if 6 <= hour < 12:
        say(f"Good Morning {USER}")
    elif 12 <= hour < 16:
        say(f"Good Afternoon {USER}")
    elif 16 <= hour < 21:
        say(f"Good Evening {USER}")
    # Add a slight delay before saying the hostname
    time.sleep(0.1)
    say(f"I am {HOSTNAME}. How may I assist you?")
    
def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print('Listening...')
        r.pause_threshold = 0.5 # this will wait for the user to complete (by default = 0.8)
        audio = r.listen(source)
        try:
            print('Recognizing...')
            query = r.recognize_google(audio,language= "en-in")
            print(f"{USER} said: {query}")
            if not 'stop' in query or 'exit' in query:
                # say(choice(random_text))
                pass
            elif 'open' in query:
                say(choice(random_text))
            else:
                hour = datetime.now().hour
                if (hour >= 21) or (hour < 6):
                    say("Good Night sir, take care!")
                else:
                    say("Have a good day sir!")
                    exit()
            return query
        except Exception as e:
            say("Sorry I couldn't understand, Can you please repeat?")

if __name__ == '__main__':
    # say('Hello I am V Bot')
    # print(f"USER: {USER}, HOSTNAME: {HOSTNAME}")
    # greet_me()
    while True:
        if listening:
            query = takeCommand()
            # say(query)
            if "how are you" in query.lower():
                say("I'm absolutely fine sir. What about you?")
            elif "open command prompt" in query.lower():
                say("Opening command prompt")
                os.system('start cmd')
            elif "open camera" in query.lower():
                say("Opening camera")
                sp.run('start microsoft.windows.camera:', shell=True)
            elif "play youtube" in query.lower():
                say(f"What do you want to play on YouTube {USER}?")
                video = takeCommand().lower()
                youtube(video)
            elif "open google" in query.lower():
                say(f"What do you want to search on google {USER}?")
                query = takeCommand().lower()
                search_on_google(query)
            elif "open wikipedia" in query.lower():
                say(f"What do you want to search on wikipedia {USER}?")
                search = takeCommand().lower()
                result = search_on_wikipedia(search)
                say(f"According to wikipedia, {result}")
                say(f"i am printing on terminal")
                print(result)
            elif "the time" in query.lower():
                strfTime = datetime.now().strftime("%H:%M:%S")
                say(f"The time is {strfTime}")
                # hour = datetime.now().strftime("%H")
                # min = datetime.now().strftime("%M")
                # say(f"The time is {hour} bajke {min} minute")
                
            elif "IP address" in query.lower():
                ip_address = find_my_id()
                say(f"Your I.P address is {ip_address}")
                print(f"Your I.P address is {ip_address}")
            
            sites = [["youtube", "https://www.youtube.com/"],
                     ["lms", "https://lms.thapar.edu/moodle/login/"],
                     ["personal mail", "https://mail.google.com/mail/u/0/#inbox"],
                     ["college mail", "https://mail.google.com/mail/u/1/#inbox"],
                     ["striver", "https://takeuforward.org/"],
                     ["github", "https://github.com/"],
                     ["lead code", "https://leetcode.com/problemset/"],
                     ["twitter", "https://x.com/home?lang=en-in"],
                     ["google","https://www.google.com/"],
                     ["udemy","https://www.udemy.com/"],
                     ["github","https://github.com/"],
                     ["youtube music","https://music.youtube.com/"]
                    ]
            for site in sites:
                if f"open {site[0]}".lower() in query.lower():
                    say(f"Opening {site[0]}")
                    webbrowser.open(site[1])
            
            # todo: add more apps
            apps = [["Edge",
                     "C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe"],
                    # ["WhatsApp",
                    #  "C:\\Users\\Vaibhav Tandon\\AppData\\Local\\Temp\\MicrosoftEdgeDownloads\\77638b9c-b97b-4c2b-91c3-56bf29721d63"],
                    ["VS code", 
                     "C:\\Users\\Vaibhav Tandon\\AppData\\Local\\Programs\\Microsoft VS Code\\Code.exe"],
                    ["Spotify", 
                     "C:\\Users\\Vaibhav Tandon\\Desktop\\Spotify.lnk"]
                   ]
            for app in apps:
                if f"open {app[0]}".lower() in query.lower():
                    say(f"Opening {app[0]}")
                    os.startfile(app[1])
             
            # todo: add a feature to play a specific song        
            # # New condition for Spotify
            # if "play" in query.lower() and "on spotify" in query.lower():
            #     say("Opening Spotify, what singer would you like to listen to?")
            #     artist = takeCommand().lower()
            #     say(f"Playing {artist} on Spotify.")
            #     # If you have a way to play the artist, use it here. This opens Spotify.
            #     os.startfile("C:\\Users\\Vaibhav Tandon\\AppData\\Roaming\\Spotify\\Spotify.exe")  # Adjust this path
            #     # Optionally, you can control playback with Spotify API here.