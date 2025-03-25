# Voice to Text Transcription Tool

A Python-based tool that uses OpenAI's Whisper model to transcribe audio files to text. The tool supports multiple languages and provides a simple command-line interface.

## Features

- Supports multiple languages (configurable via config.json)
- Uses OpenAI's Whisper model for high-quality transcription
- Shows a progress spinner during transcription
- Multiple output formats (TXT, JSON, SRT)
- Optional timestamps and confidence scores
- Configurable model size and expandable segments

## Requirements

- Python 3.x
- OpenAI Whisper
- CUDA-capable GPU (recommended for better performance)

## Installation

1. Clone this repository
2. Copy `config.example.json` to `config.json` and setup
3. Create a virtual environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Linux/Mac
   # or
   .venv\Scripts\activate  # On Windows
   ```
4. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Configuration

Edit `config.json` to customize the transcription settings:

### Basic Settings
- `language`: Target language code (e.g., "uk" for Ukrainian, "en" for English)
- `model`: Whisper model size ("tiny", "base", "small", "medium", "large-v3")
- `expandable_segments`: Enable/disable expandable segments for better memory management
- `unverified_ssl_context`: Enable/disable verify ssl certificate if you got `CERTIFICATE_VERIFY_FAILED` error

### Output Format Settings
The `output_format` section allows you to customize how the transcription is saved:

```json
{
    "output_format": {
        "type": "txt",
        "include_timestamps": false,
        "include_confidence": false
    }
}
```

Available options:
- `type`: Output format type (choose one):
  - `"txt"`: Plain text format
  - `"json"`: JSON format with full transcription data
  - `"srt"`: SubRip subtitle format
- `include_timestamps`: Add timestamps to the output (true/false)
- `include_confidence`: Include confidence scores for each segment (true/false, only for txt format)

Example configurations:

1. Basic text output:
```json
"output_format": {
    "type": "txt",
    "include_timestamps": false,
    "include_confidence": false
}
```

2. Text with timestamps and confidence:
```json
"output_format": {
    "type": "txt",
    "include_timestamps": true,
    "include_confidence": true
}
```

3. Full JSON output:
```json
"output_format": {
    "type": "json",
    "include_timestamps": true
}
```

4. SRT subtitles:
```json
"output_format": {
    "type": "srt"
}
```

## Usage

1. Run the script:
   ```bash
   python main.py
   ```
2. Enter the path to your audio file when prompted
3. Wait for the transcription to complete
4. The transcribed text will be saved in a file with the appropriate extension (.txt, .json, or .srt)

## License

This project is open source and available under the MIT License. 