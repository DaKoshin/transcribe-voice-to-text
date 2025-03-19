# Voice to Text Transcription Tool

A Python-based tool that uses OpenAI's Whisper model to transcribe audio files to text. The tool supports multiple languages and provides a simple command-line interface.

## Features

- Supports multiple languages (configurable via config.json)
- Uses OpenAI's Whisper model for high-quality transcription
- Shows a progress spinner during transcription
- Automatically saves output to a text file
- Configurable model size and expandable segments

## Requirements

- Python 3.x
- OpenAI Whisper
- CUDA-capable GPU (recommended for better performance)

## Installation

1. Clone this repository
2. Create a virtual environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Linux/Mac
   # or
   .venv\Scripts\activate  # On Windows
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Configuration

Edit `config.json` to customize the transcription settings:
- `language`: Target language code (e.g., "uk" for Ukrainian, "en" for English)
- `model`: Whisper model size ("tiny", "base", "small", "medium", "large-v3")
- `expandable_segments`: Enable/disable expandable segments for better memory management

## Usage

1. Run the script:
   ```bash
   python main.py
   ```
2. Enter the path to your audio file when prompted
3. Wait for the transcription to complete
4. The transcribed text will be saved in a .txt file with the same name as the input file

## License

This project is open source and available under the MIT License. 