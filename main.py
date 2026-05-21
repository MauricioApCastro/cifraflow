from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("CifraFlow")
        self.resize(1200, 700)
        self.setCentralWidget(QWidget())


def main():
    app = QApplication([])
    app.setStyleSheet("""
        QMainWindow {
            background-color: #121212;
        }
        QWidget {
            background-color: #121212;
            color: #f5f5f5;
        }
    """)

    window = MainWindow()
    window.show()
    app.exec()


if __name__ == "__main__":
    main()
