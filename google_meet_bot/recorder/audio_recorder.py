# recorder/audio_recorder.py

import pyaudio
import wave
from pydantic import BaseModel
from typing import Union

class AudioRecorderConfig(BaseModel):
    duration: int = 10  # Duration in seconds
    output_file: str = "output.wav"

def record_audio(config: AudioRecorderConfig) -> None:
    """
    Record audio from the system's microphone.

    :param config: Configuration object containing duration and output file.
    """
    try:
        # Initialize PyAudio
        audio = pyaudio.PyAudio()

        # Open a stream for recording system audio
        stream = audio.open(format=pyaudio.paInt16, channels=2, rate=44100, input=True, frames_per_buffer=1024)

        print("Recording audio...")

        frames = []
        for _ in range(0, int(44100 / 1024 * config.duration)):
            data = stream.read(1024)
            frames.append(data)

        print("Recording finished.")

        # Stop and close the stream
        stream.stop_stream()
        stream.close()
        audio.terminate()

        # Save the recorded audio to a file
        wf = wave.open(config.output_file, 'wb')
        wf.setnchannels(2)
        wf.setsampwidth(audio.get_sample_size(pyaudio.paInt16))
        wf.setframerate(44100)
        wf.writeframes(b''.join(frames))
        wf.close()

    except Exception as exc:
        print(f"Error recording audio: {exc}")
        raise exc
