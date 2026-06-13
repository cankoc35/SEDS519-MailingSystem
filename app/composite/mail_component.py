"""Common mail component interface."""

from abc import ABC, abstractmethod


class MailComponent(ABC):
    @abstractmethod
    def display_name(self) -> str:
        """Return a short name that can be shown in the mail view."""

    @abstractmethod
    def to_dict(self) -> dict:
        """Return a simple representation for API responses or tests."""
