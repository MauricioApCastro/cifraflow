import threading

from PyQt6.QtCore import QObject, pyqtSignal


class VoiceTranscriptionService(QObject):
    transcript_ready = pyqtSignal(str)
    error_occurred = pyqtSignal(str)

    def __init__(self, sample_rate: int = 44100):
        super().__init__()
        self.sample_rate = sample_rate
        self.frames = []
        self.is_enabled = False
        self.is_processing = False
        self.error_reported = False

    def start(self):
        self.frames.clear()
        self.error_reported = False
        self.is_enabled = True

    def stop(self):
        self.frames.clear()
        self.is_enabled = False

    def add_audio(self, audio_data):
        if not self.is_enabled or self.is_processing:
            return

        self.frames.append(audio_data)
        frame_count = sum(frame.shape[0] for frame in self.frames)
        if frame_count < self.sample_rate * 2:
            return

        frames = self.frames
        self.frames = []
        self.is_processing = True
        threading.Thread(target=self.transcribe, args=(frames,), daemon=True).start()

    def transcribe(self, frames):
        try:
            import numpy
            import speech_recognition

            audio = numpy.concatenate(frames, axis=0).reshape(-1)
            audio = numpy.clip(audio, -1.0, 1.0)
            pcm_audio = (audio * 32767).astype(numpy.int16).tobytes()

            recognizer = speech_recognition.Recognizer()
            audio_data = speech_recognition.AudioData(pcm_audio, self.sample_rate, 2)
            transcript = recognizer.recognize_google(audio_data, language="pt-BR")
            self.transcript_ready.emit(transcript)
        except Exception as error:
            if not self.error_reported:
                self.error_reported = True
                self.error_occurred.emit(f"Reconhecimento indisponível: {error}")
        finally:
            self.is_processing = False
