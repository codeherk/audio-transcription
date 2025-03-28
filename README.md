# audio-transcription

This repository contains a Python script that transcribes audio files using the OpenAI Whisper and conditionally translates using Ollama's LLM (llama3.2). The script takes an audio file as input, converts it to text using the model, and saves the transcription to a text file. 

- If the audio file is in a different format, the script will convert it to WAV format before transcription. 
- If the audio file is in a different language, the script will also translate the transcription to English.
  - Supported languages for translation:
    - Spanish
- Currently, the script supports the following audio formats: MP3, WAV, and OGG. 

## Requirements
- Python 3.8 or higher
- Ollama
  - llama3.2 model pulled: `ollama pull llama3.2:1b`
- ffmpeg

## Usage
Create the virtual environment:
```bash
make create-venv
```

Activate the virtual environment:
```bash
source venv/bin/activate
```

Install dependencies:
```bash
make install
```

Serve ollama model:
```bash
ollama serve llama3.2
```

Run the script:
```bash
make run AUDIO_FILE=<path_to_audio_file>
```

## Make Targets
The following make targets are available for use in this repository:

| Target        | Description                                                                      |
|---------------|----------------------------------------------------------------------------------|
| `create-venv` | Creates a virtual environment for the project.                                   |
| `install`     | Installs the required Python dependencies and sets up the environment.           |
| `freeze`      | Freezes the current state of the virtual environment to a requirements.txt file. |
| `run`         | Runs the transcription script on the specified audio file.                       |
| `clean`       | Removes temporary files and cleans up the workspace.                             |