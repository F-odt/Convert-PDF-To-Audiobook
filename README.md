PDF to Speech and Transcription

This program extracts text from a PDF file, converts it to speech, 
plays the generated audio, and then transcribes the audio using the Speechmatics API. 
The transcription is displayed in the console.

Installation

   1. Clone the repository or download the source code.

   2. Install the required Python packages:
      pip install PyPDF2 pygame python-dotenv speechmatics pydub gtts
   3. Create a .env file in the root directory and add your Speechmatics API token:
      SPEECHMATICS_AUTH_TOKEN=your_speechmatics_auth_token

Explanation

    app.py: The main application script that performs text extraction, text-to-speech conversion, audio playback, and transcription.
    .env: Environment file to store the Speechmatics API token.

Functions
extract_text_from_pdf(file_path)

Extracts text from a PDF file.

    Parameters:
        file_path (str): Path to the PDF file.

    Returns:
        str: Extracted text from the PDF.

convert_text_to_speech(text, language="en")

Converts text to speech and saves it as an MP3 file.

    Parameters:
        text (str): Text to convert to speech.
        language (str): Language of the text.

    Returns:
        str: Path to the saved MP3 file.

play_audio(audio_file)

Plays an audio file using pygame.

    Parameters:
        audio_file (str): Path to the audio file.

transcribe_audio(audio_file, auth_token, language="en")

Transcribes an audio file using the Speechmatics API.

    Parameters:
        audio_file (str): Path to the audio file.
        auth_token (str): Authentication token for the Speechmatics API.
        language (str): Language of the transcription.

    Returns:
        str: Transcription of the audio file.

main()

Main function to extract text from a PDF, convert it to speech, play the audio, and transcribe it.
