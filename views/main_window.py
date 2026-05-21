from PyQt6.QtGui import QColor, QFont, QKeySequence, QShortcut, QTextCharFormat, QTextCursor
from PyQt6.QtWidgets import (
    QFileDialog,
    QLabel,
    QMainWindow,
    QProgressBar,
    QPushButton,
    QTextEdit,
    QToolBar,
)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("CifraFlow")
        self.resize(1200, 700)

        self.open_button = QPushButton("Abrir Música")
        self.microphone_button = QPushButton("Microfone")
        self.stage_mode_button = QPushButton("Modo Palco")
        self.microphone_status = QLabel("Microfone desligado")
        self.voice_status = QLabel("Aguardando voz")
        self.captured_text = QLabel("Captado: -")
        self.normal_font_size = 32
        self.stage_font_size = 46

        self.volume_bar = QProgressBar()
        self.volume_bar.setRange(0, 100)
        self.volume_bar.setValue(0)
        self.volume_bar.setTextVisible(False)
        self.volume_bar.setFixedWidth(180)

        self.song_text = QTextEdit()
        self.song_text.setReadOnly(True)
        self.song_text.setFont(QFont("Consolas", self.normal_font_size))
        self.stage_mode_shortcut = QShortcut(QKeySequence("F11"), self)

        self.toolbar = QToolBar()
        self.toolbar.setMovable(False)
        self.toolbar.addWidget(self.open_button)
        self.toolbar.addWidget(self.microphone_button)
        self.toolbar.addWidget(self.stage_mode_button)
        self.toolbar.addWidget(self.microphone_status)
        self.toolbar.addWidget(self.voice_status)
        self.toolbar.addWidget(self.captured_text)
        self.toolbar.addWidget(self.volume_bar)

        self.addToolBar(self.toolbar)
        self.setCentralWidget(self.song_text)
        self.stage_mode_button.clicked.connect(self.toggle_stage_mode)
        self.stage_mode_shortcut.activated.connect(self.toggle_stage_mode)

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
        self.clear_highlight()

    def set_microphone_status(self, status: str):
        self.microphone_status.setText(status)

    def set_voice_status(self, status: str):
        self.voice_status.setText(status)

    def set_captured_text(self, text: str):
        if not text:
            self.captured_text.setText("Captado: -")
            return

        display_text = text[:80] + "..." if len(text) > 80 else text
        self.captured_text.setText(f"Captado: {display_text}")

    def highlight_stanza(self, start_line: int, end_line: int):
        selections = []
        selection_format = QTextCharFormat()
        selection_format.setBackground(QColor("#3a5f8f"))
        selection_format.setForeground(QColor("#ffffff"))

        for line_index in range(start_line, end_line + 1):
            block = self.song_text.document().findBlockByLineNumber(line_index)
            if not block.isValid():
                continue

            cursor = QTextCursor(block)
            cursor.select(QTextCursor.SelectionType.LineUnderCursor)

            selection = QTextEdit.ExtraSelection()
            selection.cursor = cursor
            selection.format = selection_format
            selections.append(selection)

        block = self.song_text.document().findBlockByLineNumber(start_line)
        if block.isValid():
            cursor = QTextCursor(block)
            self.song_text.setTextCursor(cursor)

        self.song_text.setExtraSelections(selections)
        self.center_line(start_line)

    def center_line(self, line_index: int):
        block = self.song_text.document().findBlockByLineNumber(line_index)
        if not block.isValid():
            return

        block_top = self.song_text.document().documentLayout().blockBoundingRect(block).top()
        scroll_bar = self.song_text.verticalScrollBar()
        center_offset = self.song_text.viewport().height() // 3
        scroll_bar.setValue(int(block_top - center_offset))

    def clear_highlight(self):
        self.song_text.setExtraSelections([])

    def toggle_stage_mode(self):
        if self.isFullScreen():
            self.showNormal()
            self.toolbar.show()
            self.set_font_size(self.normal_font_size)
            self.stage_mode_button.setText("Modo Palco")
            return

        self.showFullScreen()
        self.toolbar.hide()
        self.set_font_size(self.stage_font_size)
        self.stage_mode_button.setText("Sair do Palco")

    def set_font_size(self, size: int):
        font = self.song_text.font()
        font.setPointSize(size)
        self.song_text.setFont(font)
