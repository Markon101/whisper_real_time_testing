import asyncio
import pyaudio
import numpy as np
import pyautogui
from queue import Queue
from threading import Thread
import whisper

# Constants for audio stream
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000
CHUNK = 16384  # This can be adjusted

# Initialize Whisper model
model = whisper.load_model("base")  # Base model for efficiency

# Function for continuous audio capture
def audio_capture(audio_queue):
    audio = pyaudio.PyAudio()
    stream = audio.open(format=FORMAT, channels=CHANNELS,
                        rate=RATE, input=True,
                        frames_per_buffer=CHUNK)
    print("Audio capture started...")
    while True:
        data = stream.read(CHUNK, exception_on_overflow=False)
        audio_queue.put(data)

# Function for transcription and typing
async def transcribe_and_type(audio_queue):
    while True:
        if not audio_queue.empty():
            audio_chunk = audio_queue.get()
            # Convert byte data to numpy array and make it writable
            audio_data = np.frombuffer(audio_chunk, dtype=np.int16).copy()
            # Convert data to float32 as expected by PyTorch
            audio_data = audio_data.astype(np.float32)
            # Normalize audio data
            audio_data /= np.iinfo(np.int16).max
            # Transcribe audio
            try:
                result = model.transcribe(audio_data)
                text = result["text"]
                print(f"Transcribed: {text}")
                pyautogui.write(text)  # Using pyautogui for typing
            except Exception as e:
                print(f"Error during transcription: {e}")

# Main function
def main():
    audio_queue = Queue()
    audio_thread = Thread(target=audio_capture, args=(audio_queue,))
    audio_thread.start()
    asyncio.run(transcribe_and_type(audio_queue))

if __name__ == "__main__":
    main()

