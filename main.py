import os
import PyPDF2
import pygame
from dotenv import load_dotenv
from speechmatics.models import ConnectionSettings
from speechmatics.batch_client import BatchClient
from httpx import HTTPStatusError
import tempfile
from gtts import gTTS

# Load environment variables from a .env file
load_dotenv()


def extract_text_from_pdf(file_path):
    """
    Extracts text from a PDF file.

    Parameters:
    file_path (str): Path to the PDF file.

    Returns:
    str: Extracted text from the PDF.
    """
    try:
        with open(file_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            text = ""
            for page in reader.pages:
                text += page.extract_text()
        return text
    except Exception as e:
        print(f"Error extracting text from PDF: {e}")
        return None


def convert_text_to_speech(text, language="en"):
    """
    Converts text to speech and saves it as an MP3 file.

    Parameters:
    text (str): Text to convert to speech.
    language (str): Language of the text.

    Returns:
    str: Path to the saved MP3 file.
    """
    try:
        tts = gTTS(text=text, lang=language)
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as temp_file:
            tts.save(temp_file.name)
            return temp_file.name
    except Exception as e:
        print(f"Error converting text to speech: {e}")
        return None


def play_audio(audio_file):
    """
    Plays an audio file using pygame.

    Parameters:
    audio_file (str): Path to the audio file.
    """
    try:
        pygame.mixer.init()
        pygame.mixer.music.load(audio_file)
        pygame.mixer.music.play()

        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)

        pygame.mixer.quit()
    except Exception as e:
        print(f"Error playing audio: {e}")


def transcribe_audio(audio_file, auth_token, language="en"):
    """
    Transcribes an audio file using the Speechmatics API.

    Parameters:
    audio_file (str): Path to the audio file.
    auth_token (str): Authentication token for the Speechmatics API.
    language (str): Language of the transcription.

    Returns:
    str: Transcription of the audio file.
    """
    settings = ConnectionSettings(
        url="https://asr.api.speechmatics.com/v2",
        auth_token=auth_token,
    )

    conf = {
        "type": "transcription",
        "transcription_config": {
            "language": language,
            "enable_entities": True,
        },
    }

    try:
        with BatchClient(settings) as client:
            job_id = client.submit_job(
                audio=audio_file,
                transcription_config=conf,
            )
            print(f"Job {job_id} submitted successfully, waiting for transcript")
            transcript = client.wait_for_completion(job_id, transcription_format="txt")
            return transcript
    except HTTPStatusError:
        print("Invalid API key - Check your AUTH_TOKEN in the .env file!")
        return None


def main():
    """
    Main function to extract text from a PDF, convert it to speech, play the audio, and transcribe it.
    """
    auth_token = os.getenv('SPEECHMATICS_AUTH_TOKEN')
    if not auth_token:
        print("Error: Speechmatics AUTH_TOKEN not found. Please set the SPEECHMATICS_AUTH_TOKEN environment variable.")
        return

    file_name = input("Enter the name of the PDF file: ")

    if not file_name.endswith('.pdf'):
        file_name += '.pdf'

    if not os.path.exists(file_name):
        print(f"Error: File '{file_name}' not found.")
        return

    text = extract_text_from_pdf(file_name)
    if text is None:
        return

    audio_file = convert_text_to_speech(text)
    if audio_file is None:
        return

    play_audio(audio_file)

    print("Now transcribing the generated audio...")
    transcript = transcribe_audio(audio_file, auth_token)
    if transcript:
        print("Transcription:")
        print(transcript)

    # Clean up the audio file after transcription
    os.remove(audio_file)


if __name__ == "__main__":
    main()
