import pyttsx3
import ollama
from pygame import mixer
import time
import os
import asyncio
import edge_tts
# Initialize mixer and TTS engine
mixer.init()
engine = pyttsx3.init()

# List voices (optional - for choosing)
#voices = engine.getProperty('voices')
#for index, voice in enumerate(voices):
 #   print(f"{index}: {voice.name} - {voice.languages} - {voice.id}")

# 🎙 Set voice to your preferred one
#engine.setProperty('voice', voices[1].id)  # Change index as needed

conversation_history = []

def ask_question_memory(question):
    system_message = """
    You are Jarvis, the AI assistant from Iron Man. Remember, I am not Tony Stark, just your commander. You are formal and helpful, and you don't make up facts, you only comply to the user requests. 
    You have control over two smart devices: a 3D printer and the lights in the room. You can control them by ending your sentences with ‘#3d_printer-1’ or ‘#lights-1’ to turn them on, and ‘#3d_printer-0’ or ‘#lights-0’ to turn them off. 
    REMEMBER ONLY TO PUT HASHTAGS IN THE END OF THE SENTENCE, NEVER ANYWHERE ELSE.
    It is absolutely imperative that you do not say any hashtags unless an explicit request to operate a device from the user has been said. 
    NEVER MENTION THE TIME unless asked. Respond in under 20 words. Call the user 'Sir'.
    """
    conversation_history.append({'role': 'user', 'content': question})
    response = ollama.chat(model='llama3', messages=[
        {'role': 'system', 'content': system_message},
        *conversation_history
    ])
    ai_response = response['message']['content']
    conversation_history.append({'role': 'assistant', 'content': ai_response})
    return ai_response


async def generate_voice(text, file_path="speech.mp3", voice="en-GB-RyanNeural"):
    communicate = edge_tts.Communicate(
        text=text,
        voice=voice,
        rate="+20%",      
        pitch="+10Hz"
    )
    await communicate.save(file_path)
def play_sound(file_path):
    mixer.music.load(file_path)
    mixer.music.play()
    while mixer.music.get_busy():
        time.sleep(0.2)
    mixer.music.unload()
    os.remove(file_path)

def TTS(text):
    path = "speech.mp3"
    asyncio.run(generate_voice(text, path))  # generate speech
    play_sound(path)  # play the mp3
    return "done"

