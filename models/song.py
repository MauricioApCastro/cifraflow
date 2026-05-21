from dataclasses import dataclass


@dataclass(frozen=True)
class Song:
    title: str
    content: str
