//jarvis
import speech_recognition as sr 
import webbrowser
import pyttsx3
import musicLibrary        //this is my module of music library
import requests
from openai import OpenAI

recognizer = sr.Recognizer()
engine = pyttsx3.init()
newsapi = "YOUR_API"        

def speak(text):
    engine.say(text)
    engine.runAndWait()

def processOpenAI(command):
    client = OpenAI(
        api_key="YOUR_API"
    )

    completion = client.chat.completions.create(
        model = "gpt-3.5-turbo",
        messages = [
            {"role": "system","content": "You are a virtual assistant named jarvis skilled in gernal tasks like Alexa and Google loud.Give short responses please"},
            {"role": "user","content": command}
        ]
    )

    return (completion.choice[0].message.content)

def processCommand(c):
    if "open google" in c.lower():
        webbrowser.open("http://google.com")

    elif "open facebook" in c.lower():
        webbrowser.open("http://facebook.com")

    elif "open linkedin" in c.lower():
        webbrowser.open("http://linkedin.com")

    elif "open instagram" in c.lower():
        webbrowser.open("http://instagram.com")

    elif "open youtube" in c.lower():
        webbrowser.open("http://youtube.com")

    elif "open whatsapp" in c.lower():
        webbrowser.open("http://whatsapp.com")

    elif c.lower().startswith("play"):
        song = c.lower().split(" ")[1]
        link = musicLibrary.music[song]
        webbrowser.open(link)
    
    elif "news" in c.lower():
        r = requests.get(f"https://newsapi.org/v2/top-headlines?country=in&apiKey={newsapi}")
        if r.status_code == 200:
            data = r.json()
            articles = data.get('articles',[])
            for article in articles:
                speak(article['title'])

    else:
        output = (processOpenAI(c))
        speak(output)

if __name__== "__main__":
    speak("Say Jarvis!")
    while True:
        # listen for the wakeup word "jarvis"
        # take audio form microphone
        r = sr.Recognizer()
        
        # reconize speech
        print("Recognizing")
        try:
            with sr.Microphone() as source:
                print("Listening.....")
                audio = r.listen(source ,timeout=4,phrase_time_limit=3)
                word = r.recognize_google(audio)
            if(word.lower() == "jarvis"):
                speak("yes sir")
                # listen for command
                with sr.Microphone() as source:
                    print("Jarvis is listning")
                    audio = r.listen(source)
                    command = r.recognize_google(audio)

                    processCommand(command)
        

        except sr.UnknownValueError:
            print("Could not understand audio")

        except sr.RequestError:
            print("Could not request speech recognition")

        except Exception as e:
            print("error;{0}".format(e))
