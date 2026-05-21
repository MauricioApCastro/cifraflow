import threading

from PyQt6.QtCore import QObject, pyqtSignal


class VoiceTranscriptionService(QObject):
    transcript_ready = pyqtSignal(str)
    error_occurred = pyqtSignal(str)

    def __init__(self, sample_rate: int = 44100):
        super().__init__()
        self.sample_rate = sample_rate
        self.phrase_frames = []
        self.phrase_frame_count = 0
        self.silent_frame_count = 0
        self.is_enabled = False
        self.is_processing = False
        self.error_reported = False
        self.silence_threshold = 0.006
        self.trailing_silence_seconds = 0.35
        self.min_phrase_seconds = 0.35
        self.max_phrase_seconds = 10

    def start(self):
        self.clear_phrase()
        self.error_reported = False
        self.is_enabled = True

    def stop(self):
        self.clear_phrase()
        self.is_enabled = False

    def add_audio(self, audio_data):
        if not self.is_enabled:
            return

        rms = float((audio_data ** 2).mean() ** 0.5)
        frame_count = audio_data.shape[0]

        if not self.phrase_frames and rms < self.silence_threshold:
            return

        self.phrase_frames.append(audio_data)
        self.phrase_frame_count += frame_count

        if rms < self.silence_threshold:
            self.silent_frame_count += frame_count
        else:
            self.silent_frame_count = 0

        min_phrase_frames = int(self.sample_rate * self.min_phrase_seconds)
        trailing_silence_frames = int(self.sample_rate * self.trailing_silence_seconds)
        max_phrase_frames = int(self.sample_rate * self.max_phrase_seconds)

        phrase_has_minimum_size = self.phrase_frame_count >= min_phrase_frames
        phrase_finished = phrase_has_minimum_size and self.silent_frame_count >= trailing_silence_frames
        phrase_too_long = self.phrase_frame_count >= max_phrase_frames

        if not phrase_finished and not phrase_too_long:
            return

        if self.is_processing:
            return

        frames = list(self.phrase_frames)
        self.clear_phrase()
        self.is_processing = True
        threading.Thread(target=self.transcribe, args=(frames,), daemon=True).start()

    def clear_phrase(self):
        self.phrase_frames.clear()
        self.phrase_frame_count = 0
        self.silent_frame_count = 0

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
        except speech_recognition.UnknownValueError:
            self.error_occurred.emit("Nao entendi o audio. Tente falar mais perto do microfone.")
        except speech_recognition.RequestError as error:
            self.error_occurred.emit(f"Reconhecimento indisponivel: {error}")
        except Exception as error:
            if not self.error_reported:
                self.error_reported = True
                self.error_occurred.emit(f"Reconhecimento indisponível: {error}")
        finally:
            self.is_processing = False
