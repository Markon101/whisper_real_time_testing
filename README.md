# Real Time Whisper Transcription

![Demo gif](demo.gif)

This is a demo of real time speech to text with OpenAI's Whisper model. It works by constantly recording audio in a thread and concatenating the raw bytes over multiple recordings.

To install dependencies simply run
```
pip install -r requirements.txt
```
in an environment of your choosing.

Whisper also requires the command-line tool [`ffmpeg`](https://ffmpeg.org/) to be installed on your system, which is available from most package managers:

```
# on Ubuntu or Debian
sudo apt update && sudo apt install ffmpeg

# on Arch Linux
sudo pacman -S ffmpeg

# on MacOS using Homebrew (https://brew.sh/)
brew install ffmpeg

# on Windows using Chocolatey (https://chocolatey.org/)
choco install ffmpeg

# on Windows using Scoop (https://scoop.sh/)
scoop install ffmpeg
```

For more information on Whisper please see https://github.com/openai/whisper

This version I forked and worked on does automatic typing in a focused text box (browser etc) and it works decently at the given sample rate and buffer sizes. Please note that Whisper is not really built for this, but it performs well enough to be extremely useful.

The code in this repository is public domain.
