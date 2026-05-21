from PyQt6.QtCore import QTimer

from services.text_file_reader import TextFileReader
from views.main_window import MainWindow


class SongController:
    def __init__(self, view: MainWindow):
        self.view = view
        self.reader = TextFileReader()
        self.scroll_timer = QTimer()

        self.view.open_button.clicked.connect(self.open_song)
        self.view.start_button.clicked.connect(self.start_scroll)
        self.view.pause_button.clicked.connect(self.pause_scroll)
        self.view.decrease_font_button.clicked.connect(self.view.decrease_font_size)
        self.view.increase_font_button.clicked.connect(self.view.increase_font_size)
        self.view.fullscreen_button.clicked.connect(self.view.toggle_fullscreen)
        self.view.fullscreen_shortcut.activated.connect(self.view.toggle_fullscreen)
        self.view.speed_slider.valueChanged.connect(self.update_scroll_speed)
        self.scroll_timer.timeout.connect(self.scroll_text)

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
