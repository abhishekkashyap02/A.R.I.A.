import speech_recognition as sr
import os
import webbrowser
import openai
from config import apikey
import datetime
import random

# ==================== CONFIG ====================
WAKE_WORD = "aria"
chatStr = ""

# ==================== TEXT TO SPEECH ====================
def say(text):
    os.system(f'say "{text}"')

# ==================== VOICE INPUT ====================
def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        audio = r.listen(source)

    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language="en-in")
        print(f"User said: {query}")
        return query
    except Exception:
        return ""

# ==================== AI CHAT ====================
def chat(query):
    global chatStr
    openai.api_key = apikey

    chatStr += f"User: {query}\nA.R.I.A.: "

    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=chatStr,
        temperature=0.7,
        max_tokens=256
    )

    reply = response["choices"][0]["text"].strip()
    say(reply)

    chatStr += reply + "\n"
    return reply

# ==================== AI CONTENT GENERATION ====================
def ai(prompt):
    openai.api_key = apikey

    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=prompt,
        temperature=0.7,
        max_tokens=256
    )

    if not os.path.exists("Openai"):
        os.mkdir("Openai")

    filename = f"Openai/prompt_{random.randint(1, 100000)}.txt"
    with open(filename, "w") as f:
        f.write(response["choices"][0]["text"])

    say("Content generated and saved.")

# ==================== MAIN ====================
if __name__ == "__main__":
    print("A.R.I.A. started")
    say("A R I A online. Say Aria to activate me.")

    while True:
        query = takeCommand().lower()

        # Wake word check
        if WAKE_WORD not in query:
            continue

        query = query.replace(WAKE_WORD, "").strip()

        if not query:
            say("Yes, how can I help?")
            continue

        # ---------------- COMMANDS ----------------
        sites = [
            ["youtube", "https://www.youtube.com"],
            ["wikipedia", "https://www.wikipedia.com"],
            ["google", "https://www.google.com"]
        ]

        opened_site = False
        for site in sites:
            if f"open {site[0]}" in query:
                say(f"Opening {site[0]}")
                webbrowser.open(site[1])
                opened_site = True
                break

        if opened_site:
            continue

        if "open music" in query:
            musicPath = "/Users/harry/Downloads/downfall-21371.mp3"
            os.system(f"open {musicPath}")

        elif "time" in query:
            hour = datetime.datetime.now().strftime("%H")
            minute = datetime.datetime.now().strftime("%M")
            say(f"The time is {hour} {minute}")

        elif "using artificial intelligence" in query:
            ai(query)

        elif "reset chat" in query:
            chatStr = ""
            say("Chat history cleared")

        elif "quit" in query or "exit" in query:
            say("Shutting down. Goodbye.")
            exit()

        else:
            chat(query)
