
import speech_recognition as sr
import pyttsx3
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import webbrowser
import datetime
import wikipedia
import os

# Download nltk data (only once)
nltk.download('punkt')
nltk.download('stopwords')

class SimpleNLPVoiceChatbot:
    def __init__(self):
        self.engine = pyttsx3.init()
        self.engine.setProperty('rate', 160)
        self.engine.setProperty('volume', 0.9)
        voices = self.engine.getProperty('voices')
        self.engine.setProperty('voice', voices[1].id if len(voices) > 1 else voices[0].id)

        self.recognizer = sr.Recognizer()
        self.stop_words = set(stopwords.words('english'))

    def speak(self, text):
        print(f"AI: {text}")
        self.engine.say(text)
        self.engine.runAndWait()

    def take_command(self):
        with sr.Microphone() as source:
            print("Listening...")
            self.recognizer.adjust_for_ambient_noise(source, duration=0.8)
            audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=7)
        try:
            query = self.recognizer.recognize_google(audio)
            print(f"User said: {query}")
            return query.lower()
        except sr.UnknownValueError:
            self.speak("Sorry, I didn't catch that. Please say that again.")
            return None
        except sr.RequestError:
            self.speak("Sorry, my speech service is down.")
            return None

    def process_command(self, query):
        if query is None:
            return True
        tokens = word_tokenize(query)
        command_words = [w for w in tokens if w.isalpha() and w not in self.stop_words]

        if any(greet in command_words for greet in ['hello', 'hi', 'hey']):
            self.speak("Hello! How can I assist you today?")

        elif 'time' in command_words:
            now = datetime.datetime.now().strftime('%I:%M %p')
            self.speak(f"The time is {now}")

        elif 'date' in command_words:
            today = datetime.datetime.now().strftime('%A, %B %d, %Y')
            self.speak(f"Today is {today}")

        elif 'wikipedia' in command_words:
            try:
                topic = query.replace('wikipedia', '').strip()
                summary = wikipedia.summary(topic, sentences=2)
                self.speak(summary)
            except Exception:
                self.speak("Sorry, I couldn't find that on Wikipedia.")

        elif 'open' in command_words:
            sites = {
                'google': 'https://www.google.com',
                'youtube': 'https://www.youtube.com',
                'github': 'https://github.com'
            }
            for site in sites:
                if site in command_words:
                    self.speak(f"Opening {site}")
                    webbrowser.open(sites[site])
                    break
        elif any(exit_word in command_words for exit_word in ['exit', 'quit', 'stop', 'bye']):
            self.speak("Goodbye! Have a nice day.")
            return False
        else:
            self.speak("Sorry, I didn't understand that command.")
        return True

    def run(self):
        self.speak("Hi! I'm your simplified voice assistant. Please speak a command.")
        while True:
            query = self.take_command()
            if not self.process_command(query):
                break

if __name__ == '__main__':
    bot = SimpleNLPVoiceChatbot()
    bot.run()
