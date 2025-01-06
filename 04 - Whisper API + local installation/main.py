import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    raise ValueError("Missing OpenAI API key. Make sure it is set in the .env file.")

if __name__ == '__main__':

    # Initialize OpenAI client
    client = OpenAI(api_key=api_key)

    # Open the audio file
    audio_file = open("random_10_min_segment.mp3", "rb")

    # Perform the transcription
    transcript = client.audio.transcriptions.create(
        model="whisper-1",
        file=audio_file
    )

    # Save the transcription result to a text file
    with open("transcription_result.txt", "w") as text_file:
        text_file.write(transcript.text)

    print("Transcription saved to transcription_result.txt")
