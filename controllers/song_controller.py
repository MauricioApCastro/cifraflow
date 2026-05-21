from PyQt6.QtCore import QTimer

from services.audio_capture_service import AudioCaptureService
from services.text_file_reader import TextFileReader
from views.main_window import MainWindow


class SongController:
    def __init__(self, view: MainWindow):
        self.view = view
        self.reader = TextFileReader()
        self.audio_capture = AudioCaptureService()
        self.scroll_timer = QTimer()
        self.silence_timer = QTimer()
        self.silence_timer.setSingleShot(True)
        self.silence_timer.setInterval(3000)

        self.view.open_button.clicked.connect(self.open_song)
        self.view.start_button.clicked.connect(self.start_scroll)
        self.view.pause_button.clicked.connect(self.pause_scroll)
        self.view.decrease_font_button.clicked.connect(self.view.decrease_font_size)
        self.view.increase_font_button.clicked.connect(self.view.increase_font_size)
        self.view.fullscreen_button.clicked.connect(self.view.toggle_fullscreen)
        self.view.fullscreen_shortcut.activated.connect(self.view.toggle_fullscreen)
        self.view.microphone_button.clicked.connect(self.toggle_microphone)
        self.view.speed_slider.valueChanged.connect(self.update_scroll_speed)
        self.audio_capture.volume_changed.connect(self.handle_microphone_volume)
        self.audio_capture.error_occurred.connect(self.handle_microphone_error)
        self.scroll_timer.timeout.connect(self.scroll_text)
        self.silence_timer.timeout.connect(self.pause_scroll_for_silence)

    def open_song(self):
        file_path = self.view.choose_text_file()
        if not file_path:
            return

        song = self.reader.read(file_path)
        self.view.set_song_content(song.title, song.content)
        self.pause_scroll()

    def start_scroll(self):
        self.scroll_timer.start(self.scroll_interval())

    def pause_scroll(self):
        self.scroll_timer.stop()

    def update_scroll_speed(self, value: int):
        self.scroll_timer.setInterval(self.scroll_interval(value))

    def scroll_text(self):
        scroll_bar = self.view.song_text.verticalScrollBar()
        if scroll_bar.value() >= scroll_bar.maximum():
            self.pause_scroll()
            return

        scroll_bar.setValue(scroll_bar.value() + 1)

    def scroll_interval(self, speed: int | None = None) -> int:
        if speed is None:
            speed = self.view.speed_slider.value()

        return max(10, 110 - speed)

    def toggle_microphone(self):
        if self.audio_capture.is_active():
            self.audio_capture.stop()
            self.silence_timer.stop()
            self.view.microphone_status.setText("Microfone desligado")
            self.view.sound_status.setText("Silêncio")
            return

        self.audio_capture.start()
        if self.audio_capture.is_active():
            self.view.microphone_status.setText("Microfone ligado")

    def handle_microphone_error(self, message: str):
        self.audio_capture.stop()
        self.silence_timer.stop()
        if "Microfone não encontrado" in message:
            self.view.microphone_status.setText("Microfone não encontrado")
        else:
            self.view.microphone_status.setText("Microfone desligado")

        self.view.volume_bar.setValue(0)
        self.view.sound_status.setText("Silêncio")
        print(f"Erro no microfone: {message}")

    def handle_microphone_volume(self, volume: int):
        self.view.volume_bar.setValue(volume)

        if not self.audio_capture.is_active():
            return

        sensitivity = self.view.microphone_sensitivity_slider.value()
        if volume > sensitivity:
            self.silence_timer.stop()
            self.view.sound_status.setText("Som detectado")
            if not self.scroll_timer.isActive():
                self.start_scroll()
            return

        self.view.sound_status.setText("Silêncio")
        if self.scroll_timer.isActive() and not self.silence_timer.isActive():
            self.silence_timer.start()

    def pause_scroll_for_silence(self):
        self.pause_scroll()
        self.view.sound_status.setText("Rolagem pausada por silêncio")
