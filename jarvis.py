from RealtimeSTT import AudioToTextRecorder
import assist
import time
import tools

if __name__ == '__main__':
    recorder = AudioToTextRecorder(
        spinner=False,
        model="tiny.en",
        language="en",
        post_speech_silence_duration=0.2,
        silero_sensitivity=0.5
    )

    hot_words = ["jarvis"]
    conversation_active = False

    print("Jarvis is online. Say 'Hey Jarvis' to activate...")

    while True:
        current_text = recorder.text().lower()
        print("Heard:", current_text)

        # Wake word activates conversation mode
        if not conversation_active and any(hot_word in current_text for hot_word in hot_words):
            conversation_active = True


        # If active, process further inputs
        if conversation_active and current_text:
            print("User:", current_text)

            if any(kw in current_text for kw in ["sleep", "quiet"]):
                assist.TTS("Understood, Sir. Going silent.")
                conversation_active = False
                continue

            elif any(kw in current_text for kw in ["mute"]):
                conversation_active = False
                continue

            elif any(kw in current_text for kw in ["shutdown", "Quit"]):
                assist.TTS("Understood, Sir. Going offline , Take care sir.")
                conversation_active = False
                exit(0)

            recorder.stop()
            current_text = current_text + " " + time.strftime("%Y-%m-%d %H-%M-%S")
            response = assist.ask_question_memory(current_text)
            print("Jarvis:", response)
            speech = response.split('#')[0]
            assist.TTS(speech)

            if len(response.split('#')) > 1:
                command = response.split('#')[1]
                tools.parse_command(command)

            recorder.start()
