from dataclasses import dataclass


@dataclass
class Post:
    id: int
    title: str
    content: str
    date: str


@dataclass
class Title:
    post_id: int
    content: str
