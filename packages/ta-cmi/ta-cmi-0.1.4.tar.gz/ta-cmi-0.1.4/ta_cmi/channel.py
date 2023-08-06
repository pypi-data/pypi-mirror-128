from typing import Dict, Any

from .const import ChannelMode, ChannelType, Languages, ReadOnlyClass, UNITS_DE, UNITS_EN


class Channel(metaclass=ReadOnlyClass):
    """Class to display a input or output"""

    def __init__(self, mode: ChannelMode, json: Dict[str, Any]):
        """Initialize and parse json to get properties"""
        self.mode: ChannelMode = mode
        self.type: ChannelType = json["AD"]
        self.index: int = json["Number"]
        self.value: float = json["Value"]["Value"]
        self.unit: str = json["Value"]["Unit"]

    def getUnit(self, language: Languages = Languages.EN) -> str:
        if language == Languages.EN:
            return UNITS_EN.get(self.unit, "Unknown")
        else:
            return UNITS_DE.get(self.unit, "Unknown")

    def __repr__(self) -> str:
        return f"Channel {self.index}: Type: {self.type}, Mode: {self.mode}, Value: {self.value} {self.getUnit()}"
