"""Task domain model."""

from dataclasses import dataclass


@dataclass
class Task:
    id: int
    title: str
    description: str = ""
    completed: bool = False

    def mark_completed(self) -> None:
        self.completed = True

    def toggle_completed(self) -> None:
        self.completed = not self.completed
