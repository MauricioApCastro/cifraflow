from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QTextOption
from PyQt6.QtWidgets import (
    QFileDialog,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QPushButton,
    QSlider,
    QSpinBox,
    QTextEdit,
    QToolBar,
    QWidget,
)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("CifraFlow")
        self.resize(1200, 700)

        self.open_button = QPushButton("Abrir Música")
        self.start_button = QPushButton("Iniciar")
        self.pause_button = QPushButton("Pausar")

        self.font_size_input = QSpinBox()
        self.font_size_input.setRange(10, 36)
        self.font_size_input.setValue(18)

        self.speed_slider = QSlider(Qt.Orientation.Horizontal)
        self.speed_slider.setRange(1, 100)
        self.speed_slider.setValue(50)
        self.speed_slider.setFixedWidth(160)

        self.song_text = QTextEdit()
        self.song_text.setReadOnly(True)
        self.song_text.setWordWrapMode(QTextOption.WrapMode.WordWrap)
        self.song_text.setFont(QFont("Consolas", self.font_size_input.value()))

        toolbar = QToolBar()
        toolbar.setMovable(False)
        toolbar.addWidget(self.open_button)
        toolbar.addWidget(self.start_button)
        toolbar.addWidget(self.pause_button)

        font_container = QWidget()
        font_layout = QHBoxLayout(font_container)
        font_layout.setContentsMargins(8, 0, 0, 0)
        font_layout.addWidget(QLabel("Fonte"))
        font_layout.addWidget(self.font_size_input)
        toolbar.addWidget(font_container)

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

    def set_font_size(self, size: int):
        font = self.song_text.font()
        font.setPointSize(size)
        self.song_text.setFont(font)
