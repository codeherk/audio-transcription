import whisper
import sys
import logging
from pydub import AudioSegment
from datetime import datetime
import ollama

# Model name used for Ollama translation
MODEL = "llama3.2"

# Configure logging to log to both console and a file
log_filename = datetime.now().strftime("transcription_%Y-%m-%d_%H-%M-%S.log")
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(),  # Log to console
        logging.FileHandler(log_filename)  # Log to a file
    ]
)

def convert_m4a_to_wav(m4a_filepath, wav_filepath):
    """
    Converts an M4A audio file to WAV format.

    Args:
        m4a_filepath: Path to the input M4A file.
        wav_filepath: Path to save the output WAV file.
    """
    logging.info(f"Starting conversion of '{m4a_filepath}' to WAV format.")
    try:
        sound = AudioSegment.from_file(m4a_filepath, format="m4a")
        sound.export(wav_filepath, format="wav")
        logging.info(f"Successfully converted '{m4a_filepath}' to '{wav_filepath}'.")
    except Exception as e:
        logging.error(f"Error converting '{m4a_filepath}': {e}")
        raise

def translate_to_english(spanish_text)-> ollama.GenerateResponse:
    """
    Translates Spanish text to English using the Ollama model.

    Args:
        spanish_text: Text in Spanish to be translated.
    """
    logging.info("Translating Spanish text to English.")
    # Use the Ollama model for translation
    translation = ollama.generate(
        model=MODEL,
        prompt=f"You are a translator. Translate the following Spanish text to English. Return only the translation:\n\n{spanish_text}",
    )
    logging.info("Translation completed successfully.")
    return translation
   
def transcribe_audio(file_path, source_language):
    """
    Transcribes an audio file using the Whisper model.

    Args:
        file_path: Path to the audio file.
        source_language: Language of the audio file (e.g., 'es' for Spanish).
    """
    logging.info(f"Starting transcription for file: {file_path}")

    # Load the Whisper model
    model = whisper.load_model("base")
    logging.info("Whisper model loaded successfully.")

    # If file extension is m4a, convert to wav first
    if file_path.endswith(".m4a"):
        wav_file_path = file_path.replace(".m4a", ".wav")
        convert_m4a_to_wav(file_path, wav_file_path)
        file_path = wav_file_path        

    # Transcribe the audio file
    result: dict[str, str | list]
    
    try:
        # TODO: Look into using Apple MPS GPU and remove fp16 arugment.
        result = model.transcribe(file_path, language=source_language, fp16=False)
        logging.info("Transcription completed successfully.")
    except Exception as e:
        logging.error(f"Error during transcription: {e}")
        raise
    
    # Print the detected language
    logging.info(f"Detected language: {result['language']}")

    transcription = result["text"]
    if not transcription:
        logging.warning("No transcription available.")
        return
    
    # Print the transcription
    print("Transcription:")
    print(transcription)

    # TODO: Return transcription and refactor below into functions

    en_transcription : str | None = None

    # If the language is Spanish, translate to English with ollama
    if result["language"] == "es":
        logging.info("Detected language is Spanish.")
        try:
            ollama_response = translate_to_english(transcription)
            en_transcription = ollama_response["response"]
            print("Translated Text:")
            print(en_transcription)
        except Exception as e:
            logging.error(f"Error during translation: {e}")
            raise
    else:
        logging.info("No translation needed as the language is not Spanish.")
    
    # Save the transcription to a file along with the audio file name without extension
    audio_file_name = file_path.split("/")[-1].split(".")[0]
    transcription_file_path = f"{audio_file_name}-transcribed.txt"
    logging.info(f"Saving transcription to '{transcription_file_path}'")

    with open(transcription_file_path, "w") as f:
        # Write the transcription to the file
        f.write(f"Source Audio File: {audio_file_name}\n")
        f.write("Transcription:\n")
        f.write(result["text"])
        if en_transcription:
            f.write("\n\nTranslated Text:\n")
            f.write(en_transcription)
    logging.info(f"Transcription saved successfully to '{transcription_file_path}'.")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        logging.error("Invalid number of arguments. Usage: python main.py <audio_file_path> <source_language>")
        sys.exit(1)
    
    audio_file_path = sys.argv[1]
    source_language = sys.argv[2]
    
    try:
        if source_language not in ["es", "en"]:  # Add more supported languages as needed
            logging.error("Unsupported source language. Supported languages are: 'es', 'en'.")
            sys.exit(1)
        
        transcribe_audio(audio_file_path, source_language)
    except Exception as e:
        logging.error(f"An error occurred: {e}")
        sys.exit(1)