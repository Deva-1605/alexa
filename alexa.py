import speech_recognition as sr
import pyttsx3
import datetime
import os
from youtubesearchpython import VideosSearch

# Initialize the text-to-speech engine
engine = pyttsx3.init()

# Set voice to female (if available)
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)  # Set to the second voice (typically female on most systems)

def speak(text):
    """Converts text to speech."""
    engine.say(text)
    engine.runAndWait()

def greet_user():
    """Greets the user based on the time of day."""
    hour = datetime.datetime.now().hour
    if hour < 12:
        speak("Good morning!")
    elif 12 <= hour < 18:
        speak("Good afternoon!")
    else:
        speak("Good evening!")
    speak("I am your assistant. How can I help you?")

def take_command():
    """Listens to the user's voice command and returns it as text."""
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    try:
        print("Recognizing...")
        command = recognizer.recognize_google(audio)
        print(f"You said: {command}")
        return command.lower()
    except sr.UnknownValueError:
        speak("Sorry, I didn't understand that. Please repeat.")
        return "None"

def youtube_search(query):
    """Searches YouTube for videos based on the user's query."""
    videos_search = VideosSearch(query, limit = 5)
    results = videos_search.result()
    
    if len(results['videos']) > 0:
        speak("Here are some results from YouTube:")
        for idx, video in enumerate(results['videos']):
            speak(f"Result {idx + 1}: {video['title']}.")
    else:
        speak("Sorry, I couldn't find any results on YouTube.")

def execute_command(command):
    """Executes tasks based on the command."""
    if "time" in command:
        current_time = datetime.datetime.now().strftime("%I:%M %p")
        speak(f"The current time is {current_time}.")
    elif "open notepad" in command:
        speak("Opening Notepad.")
        os.system("notepad")
    elif "search" in command:
        speak("What would you like to search for on YouTube?")
        search_query = take_command()
        if search_query != "None":
            youtube_search(search_query)
    elif "exit" in command or "quit" in command:
        speak("Goodbye!")
        exit()
    else:
        speak("I'm not sure how to help with that yet.")

# Main function
if __name__ == "__main__":
    greet_user()
    while True:
        user_command = take_command()
        if user_command != "None":
            execute_command(user_command)
