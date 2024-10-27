import speech_recognition as sr
import os
import pyttsx3

from decouple import Config, RepositoryEnv
from datetime import datetime
from random import choice
from conv import random_text

# pyttsx3 converts the given text into speech
engine = pyttsx3.init('sapi5')
# sapi5 is microsoft speech api used for speech recognition
engine.setProperty('volume', 2)
engine.setProperty('rate', 180)
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)

# voices[0] --> male assistant voice
# voices[1] --> female assistant voice

# Load the .env file from the specified path
config = Config(RepositoryEnv(r"config\.env"))
USER = config('USER')
HOSTNAME = config('BOT')

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
    import time
    time.sleep(0.6)
    say(f"I am {HOSTNAME}. How may I assist you {USER}?")
    
def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone as source:
        print('Listening...')
        
        r.pause_threshold = 0.5 # this will wait for the user to complete (by default = 0.8)
        audio = r.listen(source)
        
        try:
            print("Recognizing...")
            queri = r.recognize_google(audio, language='en-in')
            print(queri)
            # speak(queri)
            # this will all the commands given by the user
            if not 'stop' in queri or 'exit' in queri:
                say(choice(random_text))
            elif 'open' in queri:
                say(choice(random_text))
            else:
                hour = datetime.now().hour
                if (hour >= 21) or (hour < 6):
                    say("Good Night sir, take care!")
                else:
                    say("Have a good day sir!")
                    exit()
        except Exception:
            say("Sorry I couldn't understand, Can you please repeat?")
            queri = 'None'
        return queri

if __name__ == '__main__':
    # say('hello i am V Bot')
    # print(f"USER: {USER}, HOSTNAME: {HOSTNAME}")
    greet_me()
