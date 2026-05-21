from pathlib import Path

from models.song import Song


class TextFileReader:
    def read(self, file_path: str) -> Song:
        path = Path(file_path)
        content = path.read_text(encoding="utf-8")
        return Song(title=path.stem, content=content)
