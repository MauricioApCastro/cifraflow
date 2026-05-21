from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QKeySequence, QShortcut, QTextOption
from PyQt6.QtWidgets import (
    QFileDialog,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QProgressBar,
    QPushButton,
    QSlider,
    QTextEdit,
    QToolBar,
    QWidget,
)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("CifraFlow")
        self.resize(1200, 700)
        self.font_size = 18

        self.open_button = QPushButton("Abrir Música")
        self.start_button = QPushButton("Iniciar")
        self.pause_button = QPushButton("Pausar")
        self.decrease_font_button = QPushButton("-")
        self.increase_font_button = QPushButton("+")
        self.fullscreen_button = QPushButton("Tela Cheia")
        self.microphone_button = QPushButton("Microfone")
        self.microphone_status = QLabel("Microfone desligado")

        self.volume_bar = QProgressBar()
        self.volume_bar.setRange(0, 100)
        self.volume_bar.setValue(0)
        self.volume_bar.setTextVisible(False)
        self.volume_bar.setFixedWidth(120)

        self.speed_slider = QSlider(Qt.Orientation.Horizontal)
        self.speed_slider.setRange(1, 100)
        self.speed_slider.setValue(50)
        self.speed_slider.setFixedWidth(160)

        self.song_text = QTextEdit()
        self.song_text.setReadOnly(True)
        self.song_text.setFont(QFont("Consolas", self.font_size))
        self.center_text_document()

        self.fullscreen_shortcut = QShortcut(QKeySequence("F11"), self)

        toolbar = QToolBar()
        toolbar.setMovable(False)
        toolbar.addWidget(self.open_button)
        toolbar.addWidget(self.start_button)
        toolbar.addWidget(self.pause_button)
        toolbar.addWidget(self.decrease_font_button)
        toolbar.addWidget(self.increase_font_button)
        toolbar.addWidget(self.fullscreen_button)
        toolbar.addWidget(self.microphone_button)
        toolbar.addWidget(self.microphone_status)
        toolbar.addWidget(self.volume_bar)

        speed_container = QWidget()
        speed_layout = QHBoxLayout(speed_container)
        speed_layout.setContentsMargins(8, 0, 0, 0)
        speed_layout.addWidget(QLabel("Velocidade"))
        speed_layout.addWidget(self.speed_slider)
        toolbar.addWidget(speed_container)

        self.addToolBar(toolbar)
        self.setCentralWidget(self.song_text)

    def choose_text_file(self) -> str:
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Abrir Música",
            "musicas",
            "Arquivos de texto (*.txt)",
        )
        return file_path

    def set_song_content(self, title: str, content: str):
        self.setWindowTitle(f"CifraFlow - {title}")
        self.song_text.setPlainText(content)
        self.center_text_document()

    def increase_font_size(self):
        self.set_font_size(self.font_size + 2)

    def decrease_font_size(self):
        self.set_font_size(self.font_size - 2)

    def set_font_size(self, size: int):
        self.font_size = max(10, min(48, size))
        font = self.song_text.font()
        font.setPointSize(self.font_size)
        self.song_text.setFont(font)

    def center_text_document(self):
        text_options = self.song_text.document().defaultTextOption()
        text_options.setWrapMode(QTextOption.WrapMode.WordWrap)
        text_options.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        self.song_text.document().setDefaultTextOption(text_options)

    def toggle_fullscreen(self):
        if self.isFullScreen():
            self.showNormal()
            return

        self.showFullScreen()
