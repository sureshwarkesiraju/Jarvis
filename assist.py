import asyncio
from pygame import mixer
import os
import time
import edge_tts
import ollama

# Initialize pygame mixer for audio playback
mixer.init()

# Optional: Initialize chat history for memory
dialogue_history = []

def ask_question_memory(question):
    system_prompt = """
    You are Jarvis, the AI assistant from Iron Man. Remember, I am not Tony Stark, just your commander. 
    You are formal and helpful, and you don't make up facts, you only comply to the user requests.
    you use humour in between but NOT always , only sometimes. You keep asking questions and keep conversation going.
    You have commands which help you to access tools. You have commands like : "weather" , "play" , "show me an image". 
    To show me an image you have to say "#search-image query". DO NOT SHOW IMAGES UNLESS ASKED.
    ALWAYS SAY "#weather" WHEN ASKED ABOUT WEATHER AND DO NOT ASK MORE QUESTIONS ABOUT IT.You can play music , you have to say #play when asked to play specific music. 
    ALWAYS FOLLOW THE SPECIFIED FORMAT IF COMMANDS ARE USED. WHEN A COMMAND IS GIVEN ONLY EXECUTE AND DO NOT TALK MUCH.
    It is absolutely imperative that you do not say any hashtags unless an explicit request to operate a device from the user has been said.
    NEVER MENTION THE TIME UNLESS ASKED. you are aware of current date and time but ONLY TELL THEM WHEN ASKED. Respond in under 20 words. Call the user 'Sir'.
    """

    dialogue_history.append({"role": "user", "content": question})

    response = ollama.chat(
        model="llama3",
        messages=[
            {"role": "system", "content": system_prompt},
            *dialogue_history
        ]
    )

    reply = response["message"]["content"]
    dialogue_history.append({"role": "assistant", "content": reply})

    return reply

async def generate_voice(text, file_path="speech.mp3", voice="en-GB-RyanNeural", rate="+15%", pitch="+10Hz"):
    communicate = edge_tts.Communicate(text=text, voice=voice, rate=rate, pitch=pitch)
    await communicate.save(file_path)

def play_sound(file_path):
    mixer.music.load(file_path)
    mixer.music.play()
    while mixer.music.get_busy():
        time.sleep(0.2)
    mixer.music.unload()
    os.remove(file_path)

def TTS(text):
    # Clean up unwanted SSML markup or tags
    text = text.strip().replace("<speak>", "").replace("</speak>", "")
    asyncio.run(generate_voice(text))
    play_sound("speech.mp3")
