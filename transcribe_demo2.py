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
CHUNK = 8192*4 # audio chunk size

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
    audio_buffer = np.array([], dtype=np.float32)
    while True:
        if not audio_queue.empty():
            audio_chunk = audio_queue.get()
            audio_data = np.frombuffer(audio_chunk, dtype=np.int16).copy()
            audio_data = audio_data.astype(np.float32)
            audio_data /= np.iinfo(np.int16).max
            audio_buffer = np.concatenate((audio_buffer, audio_data))

            # Process the buffer if it's long enough
            if len(audio_buffer) >= RATE * 6:  # One second of audio
                try:
                    result = model.transcribe(audio_buffer)
                    text = result["text"]
                    print(f"Transcribed: {text}")
                    pyautogui.write(text)
                    audio_buffer = np.array([], dtype=np.float32)  # Clear the buffer
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

