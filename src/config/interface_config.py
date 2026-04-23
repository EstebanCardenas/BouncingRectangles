from dataclasses import dataclass
import pygame
import json

@dataclass
class InterfaceElementConfig:
    font: str
    font_size: int
    color: pygame.Color
    content: str

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            data["font"],
            data["font_size"],
            pygame.Color(*data["color"]),
            data["content"]
        )

class InterfaceConfig:
    def __init__(self) -> None:
        self.title: InterfaceElementConfig = None
        self.subtitle: InterfaceElementConfig = None
        self.special_text: InterfaceElementConfig = None

    def load_config(self, config_path: str):
        with open(config_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
        self.title = InterfaceElementConfig.from_dict(data["title"])
        self.subtitle = InterfaceElementConfig.from_dict(data["subtitle"])
        self.special_text = InterfaceElementConfig.from_dict(data["special_text"])
