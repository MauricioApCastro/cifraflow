from pathlib import Path
import re
import unicodedata

from services.audio_capture_service import AudioCaptureService
from services.voice_transcription_service import VoiceTranscriptionService
from views.main_window import MainWindow


class SongController:
    def __init__(self, view: MainWindow):
        self.view = view
        self.audio_capture = AudioCaptureService()
        self.voice_transcription = VoiceTranscriptionService(self.audio_capture.sample_rate)
        self.lyric_lines = []
        self.current_line_position = 0

        self.view.open_button.clicked.connect(self.open_song)
        self.view.microphone_button.clicked.connect(self.toggle_microphone)
        self.audio_capture.volume_changed.connect(self.view.volume_bar.setValue)
        self.audio_capture.audio_data_changed.connect(self.voice_transcription.add_audio)
        self.audio_capture.error_occurred.connect(self.handle_microphone_error)
        self.voice_transcription.transcript_ready.connect(self.follow_lyrics_from_voice)
        self.voice_transcription.error_occurred.connect(self.handle_transcription_error)

    def open_song(self):
        file_path = self.view.choose_text_file()
        if not file_path:
            return

        path = Path(file_path)
        content = path.read_text(encoding="utf-8")
        self.lyric_lines = self.build_lyric_lines(content)
        self.current_line_position = 0
        self.view.set_song_content(path.stem, content)
        self.highlight_current_line()
        self.view.set_voice_status("Aguardando frase")

    def toggle_microphone(self):
        if self.audio_capture.is_active():
            self.audio_capture.stop()
            self.voice_transcription.stop()
            self.view.set_microphone_status("Microfone desligado")
            return

        self.audio_capture.start()
        if self.audio_capture.is_active():
            self.voice_transcription.start()
            self.view.set_microphone_status("Microfone ligado")
            self.view.set_voice_status("Aguardando frase")

    def follow_lyrics_from_voice(self, transcript: str):
        self.view.set_captured_text(transcript)
        spoken_words = self.normalize_text(transcript).split()
        if not spoken_words or not self.lyric_lines:
            self.view.set_voice_status("Não reconhecido")
            return

        if not self.current_line_finished(spoken_words):
            self.view.set_voice_status("Aguardando frase")
            return

        self.current_line_position = min(self.current_line_position + 1, len(self.lyric_lines) - 1)
        self.highlight_current_line()
        self.view.set_voice_status("Próxima frase marcada")

    def current_line_finished(self, spoken_words: list[str]) -> bool:
        current_words = self.lyric_lines[self.current_line_position]["words"]
        if not current_words:
            return False

        return current_words[-1] in spoken_words

    def build_lyric_lines(self, content: str) -> list[dict]:
        lyric_lines = []

        for line_index, line in enumerate(content.splitlines()):
            clean_line = line.strip()
            if (
                not clean_line
                or self.is_chord_line(clean_line)
                or self.is_marker_line(clean_line)
            ):
                continue

            words = self.normalize_text(clean_line).split()
            if not words:
                continue

            lyric_lines.append(
                {
                    "line_index": line_index,
                    "words": words,
                }
            )

        return lyric_lines

    def highlight_current_line(self):
        if not self.lyric_lines:
            return

        line_index = self.lyric_lines[self.current_line_position]["line_index"]
        self.view.highlight_stanza(line_index, line_index)

    def normalize_text(self, text: str) -> str:
        text = unicodedata.normalize("NFD", text)
        text = "".join(character for character in text if unicodedata.category(character) != "Mn")
        text = text.lower()
        text = re.sub(r"[^a-z0-9\s]", " ", text)
        return " ".join(text.split())

    def is_chord_line(self, line: str) -> bool:
        chord_pattern = re.compile(r"^[A-G](#|b)?(m|maj|min|dim|aug|sus|add)?\d*(/[A-G](#|b)?)?$")
        tokens = line.replace("|", " ").split()
        return bool(tokens) and all(chord_pattern.match(token) for token in tokens)

    def is_marker_line(self, line: str) -> bool:
        return bool(re.match(r"^\[[^\]]+\]$", line.strip()))

    def handle_microphone_error(self, message: str):
        self.audio_capture.stop()
        self.voice_transcription.stop()
        self.view.volume_bar.setValue(0)
        self.view.set_microphone_status("Microfone não encontrado")
        print(f"Erro no microfone: {message}")

    def handle_transcription_error(self, message: str):
        self.view.set_voice_status("Aguardando frase")
        print(message)
