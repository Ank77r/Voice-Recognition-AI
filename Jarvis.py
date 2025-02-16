# pip install pyaudio pyttsx3 speechRecognition wikipedia pyjokes pyowm smtplib webbrowser os

import pyttsx3  # pip install pyttsx3
import speech_recognition as sr  # pip install speechRecognition
import datetime
import wikipedia  # pip install wikipedia
import webbrowser
import os
import smtplib
import pyjokes  # pip install pyjokes
import requests  # pip install requests
import time
import subprocess

# Initialize the pyttsx3 engine
engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)
engine.setProperty('volume', 1)  # Volume 0.0 to 1.0
engine.setProperty('rate', 200)  # Speed

def speak(audio):
    engine.say(audio)
    engine.runAndWait()

def wishMe():
    hour = int(datetime.datetime.now().hour)
    if hour >= 0 and hour < 12:
        speak("Good Morning Boss! Friday this side... tell me how may I help you")
    elif hour >= 12 and hour < 18:
        speak("Good Afternoon Boss! Friday this side... tell me how may I help you")
    else:
        speak("Good Evening Boss! Friday this side... tell me how may I help you")

def takeCommand():
    """Takes microphone input from the user and returns string output"""
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source)

    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language='en-in')
        print(f"User said: {query}\n")
    except Exception as e:
        print("Say that again please...")
        speak("Say that again please...")
        return "None"
    return query

def sendEmail(to, content):
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.ehlo()
        server.starttls()
        server.login('pandeyankur1405@gmail.com', '36goldenarrows36')  # Use your App Password
        server.sendmail('pandeyankur1405@gmail.com', to, content)
        server.close()
        speak("Email has been sent successfully, Boss!")
    except Exception as e:
        print(e)
        speak("Sorry Boss. I am not able to send this email")

def createFolder(folder_name):
    # Creates a folder in the current directory
    try:
        os.makedirs(folder_name)
        speak(f"Folder named {folder_name} has been created successfully!")
        print(f"Folder '{folder_name}' created.")
    except FileExistsError:
        speak("The folder already exists. Please try with a different name.")
        print(f"Folder '{folder_name}' already exists.")


def getWeather(city):
    """Fetches weather information from OpenWeatherMap"""
    api_key = '553402b855fd669159cbf224added58c'
    base_url = "http://api.openweathermap.org/data/2.5/weather?"
    complete_url = f"{base_url}q={city}&appid={api_key}&units=metric"
    response = requests.get(complete_url)
    data = response.json()
    
    if data["cod"] != "404":
        main_data = data["main"]
        weather_data = data["weather"][0]
        temperature = main_data["temp"]
        weather_description = weather_data["description"]
        print(f"Weather in {city}: {temperature}°C with {weather_description}")
        speak(f"Weather in {city}: {temperature}°C with {weather_description}")
    else:
        print("City not found, please try again.")
        speak("City not found, please try again.")

def tellJoke():
    """Tells a random joke"""
    joke = pyjokes.get_joke()
    print (joke)
    speak(joke)
    

def setReminder(time_str, reminder_message):
    """Sets a reminder"""
    time_struct = time.strptime(time_str, "%H:%M")
    reminder_time = time.mktime(time_struct)
    current_time = time.time()
    delay = reminder_time - current_time
    if delay < 0:
        speak("The time you have set is in the past. Please try again.")
        return
    speak(f"Reminder set for {time_str}.")
    time.sleep(delay)
    speak(f"Reminder: {reminder_message}")

def shutdownSystem():
    """Shuts down the system"""
    speak("Shutting down the system now!")
    subprocess.run(["shutdown", "/s", "/t", "1"])

def restartSystem():
    """Restarts the system"""
    speak("Restarting the system now!")
    subprocess.run(["shutdown", "/r", "/t", "1"])

if __name__ == "__main__":
    wishMe()
    while True:
        query = takeCommand().lower()

        # Logic for executing tasks based on query
        if 'wikipedia' in query:
            print('Searching Wikipedia...')
            speak('Searching Wikipedia...')
            query = query.replace("wikipedia", "")
            results = wikipedia.summary(query, sentences=2)
            print("According to Wikipedia")
            speak("According to Wikipedia")
            print(results)
            speak(results)

        elif 'open youtube' in query:
            webbrowser.open("youtube.com")

        elif 'open google' in query:
            webbrowser.open("google.com")

        elif 'open stackoverflow' in query:
            webbrowser.open("stackoverflow.com")

        elif 'the time' in query:
            strTime = datetime.datetime.now().strftime("%H:%M:%S")
            print(f"Sir, the time is {strTime}")
            speak(f"Sir, the time is {strTime}")

        elif 'open code' in query:
            codePath = "C:\\Users\\pande\\AppData\\Local\\Programs\\Microsoft VS Code\\Code.exe"
            os.startfile(codePath)

        elif 'create folder' in query:
            print("What should be the folder name?")
            speak("What should be the folder name?")
            folder_name = takeCommand().lower()
            createFolder(folder_name)

        elif 'email to ankur' in query:
            print("What should I say?")
            speak("What should I say?")
            content = takeCommand()
            to = "flyingofficerankur001@gmail.com"
            sendEmail(to, content)

        elif 'tell a joke' in query:
            tellJoke()

        elif 'weather' in query:
            print("Which city's weather would you like to know?")
            speak("Which city's weather would you like to know?")
            city = takeCommand().lower()
            getWeather(city)

        elif 'set reminder' in query:
            speak("Please provide the time in HH:MM format for the reminder.")
            time_str = takeCommand()
            speak("What should the reminder say?")
            reminder_message = takeCommand()
            setReminder(time_str, reminder_message)

        elif 'shutdown' in query:
            shutdownSystem()

        elif 'restart' in query:
            restartSystem()

        elif 'exit' in query or 'close' in query or 'stop' in query:
            speak("Turning Sleep Mode On! Goodbye Boss")
            break
