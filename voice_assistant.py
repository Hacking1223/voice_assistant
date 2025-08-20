import datetime
import webbrowser
import sys
import numpy as np
import sounddevice as sd
import speech_recognition as sr
import pyttsx3
import wikipedia

# ----------- Setup -----------
recognizer = sr.Recognizer()
tts = pyttsx3.init()
tts.setProperty("rate", 160)  # speed of speech

def speak(text):
    """Speak the given text and also print it."""
    print("Assistant:", text)
    tts.say(text)
    tts.runAndWait()

def record_audio(duration=4, fs=16000):
    """Record audio using sounddevice and return an AudioData object."""
    try:
        print(f"🎙 Recording {duration} seconds...")
        recording = sd.rec(int(duration * fs), samplerate=fs, channels=1, dtype="int16")
        sd.wait()
        raw_bytes = recording.tobytes()
        return sr.AudioData(raw_bytes, fs, 2)
    except Exception as e:
        print("Recording error:", e)
        speak("I could not access the microphone.")
        return None

def listen(duration=4):
    """Listen for a few seconds and convert speech to text."""
    audio = record_audio(duration)
    if audio is None:
        return ""
    try:
        text = recognizer.recognize_google(audio, language="en-IN")
        return text.lower()
    except sr.UnknownValueError:
        return ""
    except sr.RequestError:
        speak("Check your internet connection.")
        return ""

def handle_command(text):
    """Take action based on recognized text."""
    if not text:
        speak("I didn't catch that. Please try again.")
        return False

    print("You said:", text)

    if "time" in text:
        now = datetime.datetime.now().strftime("%I:%M %p")
        speak(f"The time is {now}.")
    elif "open youtube" in text:
        speak("Opening YouTube.")
        webbrowser.open("https://www.youtube.com")
    elif text.startswith("search "):
        query = text.replace("search", "").strip()
        if query:
            speak(f"Searching for {query}")
            webbrowser.open(f"https://www.google.com/search?q={query}")
    elif "exit" in text or "quit" in text or "stop" in text:
        speak("Goodbye!")
        return True
    else:
        # Try answering with Wikipedia
        try:
            summary = wikipedia.summary(text, sentences=2)
            speak(summary)
        except Exception:
            speak("I couldn't find an answer. Let me search the web.")
            webbrowser.open(f"https://www.google.com/search?q={text}")
    return False

def main():
    speak("Hello, I am your assistant. Say 'exit' to stop.")
    while True:
        speak("Listening now.")
        text = listen(duration=4)
        if handle_command(text):
            break

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Stopped by user")
        sys.exit(0)