from __future__ import annotations
from typing import TypeVar
import datetime

E = TypeVar('E', bound="Embed")

class Embed:
    def __init__(self, title: str = None, description: str = None, color = None, timestamp = None):
        self.title = None if title is None else title
        self.description = None if description is None else description
        self.color = 0x2f3136 if color is None else color
        self._timestamp = None if timestamp is None else timestamp
        self.__built = {"type": "rich", "title": self.title, "description": self.description, "color": self.color}

    @property
    def timestamp(self) -> datetime.datetime:
        return self._timestamp

    @timestamp.setter
    def timestamp(self, value: datetime.datetime):
        if isinstance(value, datetime.datetime):
            if value.tzinfo is None:
                value = value.astimezone()
            self._timestamp = value
        elif isinstance(value, None):
            self._timestamp = None
        else:
            raise TypeError(f"Expected datetime.datetime object, received {value.__class__.__name__}")

    def add_field(self, name: str = None, value: str = None, inline: bool = False) -> E:
        """Adds a field object to the Embed"""
        if name is None:
            raise ValueError("Embed.field name expected string, received NoneType.")
        if value is None:
            raise ValueError("Embed.field value expected string, received NoneType.")
        if name is None and value is None:
            raise ValueError("Embed.field object cannot be empty.")

        try:
            self.__built['fields'].append({"name": name, "value": value, "inline": inline})
        except KeyError:
            self.__built['fields'] = [{"name": name, "value": value, "inline": inline}]

        return self

    def set_footer(self, text: str = None, icon_url: str = None) -> E:
        if text is None and icon_url is None:
            raise ValueError("Embed.footer object cannot be empty.")

        try:
            self.__built['footer']['text'] = text
            if icon_url is not None:
                self.__built['footer']['icon_url'] = icon_url
        except KeyError:
            self.__built['footer'] = {"text": text}
            if icon_url is not None:
                self.__built['footer']['icon_url'] = icon_url

        return self

    def set_author(self, name: str = None, url: str = None, icon_url: str = None) -> E:
        if name is None and url is None and icon_url is None:
            raise ValueError("Embed.author object cannot be empty.")

        try:
            if name is not None:
                self.__built['author']['name'] = name
            if url is not None:
                self.__built['author']['url'] = url
            if icon_url is not None:
                self.__built['author']['icon_url'] = icon_url
        except KeyError:
            self.__built['author'] = {}
            if name is not None:
                self.__built['author']['name'] = name
            if url is not None:
                self.__built['author']['url'] = url
            if icon_url is not None:
                self.__built['author']['icon_url'] = icon_url

        return self

    def set_image(self, image_url: str):
        self.__built['image'] = {}
        self.__built['image']['url'] = image_url

        return self

    def set_thumbnail(self, thumbnail_url: str):
        self.__built['thumbnail'] = {}
        self.__built['thumbnail']['url'] = thumbnail_url

    def build(self) -> dict:
        if self._timestamp is not None:
            if self._timestamp.tzinfo:
                self.__built['timestamp'] = self._timestamp.astimezone(tz=datetime.timezone.utc).isoformat()
            else:
                self.__built['timestamp'] = self._timestamp.replace(tzinfo=datetime.timezone.utc).isoformat()
        return self.__built