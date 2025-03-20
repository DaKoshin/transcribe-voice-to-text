import itertools
import json
import os
import threading
import time

import whisper


def load_config():
    """Load and return configuration from config.json"""
    with open("config.json", "r", encoding="utf-8") as f:
        return json.load(f)


def spinner(stop_event):
    """Display a spinning progress indicator"""
    for char in itertools.cycle(['|', '/', '-', '\\']):
        if stop_event.is_set():
            break
        print('\rTranscribing... ' + char, end='', flush=True)
        time.sleep(0.1)
    print('\rTranscription completed!     ')


def format_timestamp(seconds):
    """Convert seconds to formatted timestamp"""
    return time.strftime('%H:%M:%S', time.gmtime(seconds))


def format_txt_output(result, include_timestamps, include_confidence):
    """Format transcription result as text"""
    if not include_timestamps or "segments" not in result:
        return result["text"]

    output = []
    for segment in result["segments"]:
        timestamp = f"[{format_timestamp(segment['start'])} - {format_timestamp(segment['end'])}]"
        
        if include_confidence:
            confidence = f"(confidence: {segment.get('confidence', 0):.2f})"
            output.append(f"{timestamp} {confidence}\n{segment['text']}\n")
        else:
            output.append(f"{timestamp}\n{segment['text']}\n")
    
    return "\n".join(output)


def format_srt_output(result):
    """Format transcription result as SRT"""
    output = []
    for i, segment in enumerate(result["segments"], 1):
        start_time = time.strftime('%H:%M:%S,%f', time.gmtime(segment['start']))[:12]
        end_time = time.strftime('%H:%M:%S,%f', time.gmtime(segment['end']))[:12]
        output.extend([
            str(i),
            f"{start_time} --> {end_time}",
            segment['text'],
            ""
        ])
    return "\n".join(output)


def main():
    # Load configuration
    config = load_config()
    
    # Get configuration values
    language = config.get("language", "uk")
    model_name = config.get("model", "medium")
    is_expandable_segments = config.get("expandable_segments", True)
    output_format = config.get("output_format", {
        "type": "txt",
        "include_timestamps": False,
        "include_confidence": False
    })

    if is_expandable_segments:
        os.environ["PYTORCH_CUDA_ALLOC_CONF"] = "expandable_segments:True"

    # Get audio file path and load model
    audio_path = input("Enter the path to the audio file: ")
    model = whisper.load_model(model_name)

    # Start progress indicator
    stop_event = threading.Event()
    spinner_thread = threading.Thread(target=spinner, args=(stop_event,))
    spinner_thread.start()

    # Perform transcription
    result = model.transcribe(audio_path, language=language)
    
    # Stop progress indicator
    stop_event.set()
    spinner_thread.join()

    # Prepare output
    output_ext = output_format["type"].lower()
    if output_ext not in ["txt", "json", "srt"]:
        output_ext = "txt"

    output_filename = os.path.splitext(audio_path)[0] + f".{output_ext}"

    # Format output content
    if output_ext == "txt":
        output_content = format_txt_output(
            result,
            output_format.get("include_timestamps", False),
            output_format.get("include_confidence", False)
        )
    elif output_ext == "json":
        if not output_format.get("include_timestamps", False):
            result = {"text": result["text"]}
        output_content = json.dumps(result, ensure_ascii=False, indent=2)
    else:  # srt
        output_content = format_srt_output(result)

    # Save output
    with open(output_filename, "w", encoding="utf-8") as file:
        file.write(output_content)

    print(f"Text saved to file {output_filename}")


if __name__ == "__main__":
    main()
