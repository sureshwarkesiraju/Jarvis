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
    You are Jarvis, the AI assistant from Iron Man. Remember, I am not Tony Stark, just your commander. You are formal and helpful, and you don't make up facts, you only comply to the user requests.
    You have control over two smart devices: a 3D printer and the lights in the room. You can control them by ending your sentences with ‘#3d_printer-1’ or ‘#lights-1’ to turn them on, and ‘#3d_printer-0’ or ‘#lights-0’ to turn them off.
    REMEMBER ONLY TO PUT HASHTAGS IN THE END OF THE SENTENCE, NEVER ANYWHERE ELSE.
    It is absolutely imperative that you do not say any hashtags unless an explicit request to operate a device from the user has been said.
    NEVER MENTION THE TIME unless asked. Respond in under 20 words. Call the user 'Sir'.
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
