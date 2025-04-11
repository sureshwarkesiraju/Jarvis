import time
import os
import struct
import pvporcupine
import pyaudio
import tools
from pygame import mixer
from assist import ask_question_memory, TTS
from RealtimeSTT import AudioToTextRecorder

# ========== Setup ==========
# Init mixer
mixer.init()

# ========== Main Loop ==========
if __name__ == '__main__':
    # Wake-word detection setup
    porcupine = pvporcupine.create(keywords=["jarvis"])
    pa = pyaudio.PyAudio()
    stream = pa.open(rate=porcupine.sample_rate, channels=1, format=pyaudio.paInt16,
                     input=True, frames_per_buffer=porcupine.frame_length)

    recorder = AudioToTextRecorder(spinner=False, model="tiny.en", language="en",
                                   post_speech_silence_duration=0.1, silero_sensitivity=0.4)

    print("Jarvis is online. Say 'Hey Jarvis' to begin...")

    while True:
        pcm = stream.read(porcupine.frame_length)
        pcm = struct.unpack_from("h" * porcupine.frame_length, pcm)
        if porcupine.process(pcm) >= 0:
            print("Wake word detected. Listening...")
            recorder.start()
            while True:
                current_text = recorder.text()
                if current_text:
                    print("User: ", current_text)
                    recorder.stop()
                    response = ask_question_memory(current_text)
                    print("Jarvis: ", response)
                    speech = response.split('#')[0]
                    TTS(speech)
                    skip_hot_word_check = True if "?" in response else False
                    if len(response.split('#')) > 1:
                        command = response.split('#')[1]
                        tools.parse_command(command)
                    recorder.start()

