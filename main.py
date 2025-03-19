import itertools
import json
import os
import threading
import time

import whisper

# Reading configuration from config.json
with open("config.json", "r", encoding="utf-8") as f:
    config = json.load(f)

# Getting language and model name from configuration (default "uk" and "medium")
language = config.get("language", "uk")
model_name = config.get("model", "medium")
is_expandable_segments = config.get("expandable_segments", True)

if is_expandable_segments:
    os.environ["PYTORCH_CUDA_ALLOC_CONF"] = "expandable_segments:True"

# Getting audio file path from console
audio_path = input("Enter the path to the audio file: ")

# Loading the model
model = whisper.load_model(model_name)

# Function for progress indicator (spinner)
def spinner(stop_e):
    for c in itertools.cycle(['|', '/', '-', '\\']):
        if stop_e.is_set():
            break
        print('\rTranscribing... ' + c, end='', flush=True)
        time.sleep(0.1)
    print('\rTranscription completed!     ')


# Starting the spinner thread
stop_event = threading.Event()
spinner_thread = threading.Thread(target=spinner, args=(stop_event,))
spinner_thread.start()

# Starting audio file transcription with specified language
result = model.transcribe(audio_path, language=language)
text = result["text"]

# Stopping the spinner after transcription is complete
stop_event.set()
spinner_thread.join()

# Forming output filename (with the same base and .txt extension)
output_filename = os.path.splitext(audio_path)[0] + ".txt"

# Writing transcribed text to file
with open(output_filename, "w", encoding="utf-8") as file:
    file.write(text)

print(f"Text saved to file {output_filename}")
