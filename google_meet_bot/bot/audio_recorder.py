# recorder/audio_recorder.py

import pyaudio
import wave
from pydantic import BaseModel
import threading

from bot.models import AudioRecorderConfig


class AudioRecorder:
    def __init__(self, config: AudioRecorderConfig):
        self.config = config
        self.frames = []
        self.recording = False
        self.stream = None
        self.audio = None

    def start_recording(self):
        """Starts the audio recording in a separate thread."""
        self.recording = True
        self.frames = []
        self.audio = pyaudio.PyAudio()

        self.stream = self.audio.open(
            format=pyaudio.paInt16,
            channels=2,
            rate=44100,
            input=True,
            frames_per_buffer=1024,
        )

        print("Recording audio...")

        def record():
            while self.recording:
                try:
                    data = self.stream.read(1024)
                    self.frames.append(data)
                except Exception as exc:
                    print(f"Error recording audio: {exc}")
                    break

        self.record_thread = threading.Thread(target=record)
        self.record_thread.start()

    def stop_recording(self):
        """Stops the audio recording."""
        self.recording = False
        if self.stream:
            self.stream.stop_stream()
            self.stream.close()
        if self.audio:
            self.audio.terminate()

        # Wait for the thread to finish recording
        self.record_thread.join()

        # Save the recorded audio to a file
        with wave.open(self.config.output_file, "wb") as wf:
            wf.setnchannels(2)
            wf.setsampwidth(self.audio.get_sample_size(pyaudio.paInt16))
            wf.setframerate(44100)
            wf.writeframes(b"".join(self.frames))

        print(f"Recording saved as {self.config.output_file}")


def record_audio(config: AudioRecorderConfig) -> AudioRecorder:
    """Start recording audio."""
    recorder = AudioRecorder(config)
    recorder.start_recording()
    return recorder
