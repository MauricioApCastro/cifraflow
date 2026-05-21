import sys

from PyQt6.QtWidgets import QApplication

from controllers.song_controller import SongController
from views.main_window import MainWindow


def main():
    app = QApplication(sys.argv)
    app.setStyleSheet("""
        QMainWindow {
            background-color: #121212;
        }
        QWidget {
            background-color: #121212;
            color: #f5f5f5;
        }
        QToolBar {
            background-color: #1b1b1b;
            border: none;
            spacing: 8px;
        }
        QPushButton, QSpinBox {
            background-color: #2a2a2a;
            border: 1px solid #3a3a3a;
            border-radius: 4px;
            color: #f5f5f5;
            padding: 6px;
        }
        QSlider::groove:horizontal {
            background-color: #2a2a2a;
            height: 6px;
        }
        QSlider::handle:horizontal {
            background-color: #f5f5f5;
            margin: -5px 0;
            width: 12px;
        }
        QProgressBar {
            background-color: #2a2a2a;
            border: 1px solid #3a3a3a;
            border-radius: 4px;
        }
        QProgressBar::chunk {
            background-color: #4caf50;
        }
        QTextEdit {
            background-color: #121212;
            border: none;
            color: #f5f5f5;
            selection-background-color: #3a5f8f;
        }
    """)

    window = MainWindow()
    window.controller = SongController(window)
    window.show()
    app.exec()


if __name__ == "__main__":
    main()
