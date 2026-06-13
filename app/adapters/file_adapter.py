"""Common file adapter interface."""

from abc import ABC, abstractmethod


class FileAdapter(ABC):
    @abstractmethod
    def to_html_table(self, file_path: str) -> str:
        """Convert a file into a standard HTML table string."""
