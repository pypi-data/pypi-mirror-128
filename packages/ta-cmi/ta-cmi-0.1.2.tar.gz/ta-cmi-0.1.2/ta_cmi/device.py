from typing import Dict, Any, List

from .baseApi import BaseAPI
from .channel import Channel

from .const import DEVICES, ReadOnlyClass, ChannelMode


class Device(BaseAPI, metaclass=ReadOnlyClass):
    """Class to interact with a device"""

    def __init__(self, nodeID: str, host: str, username: str, password: str):
        """Initialize."""
        super().__init__(username, password)
        self.id: str = nodeID
        self.host: str = host

        self.apiVersion: int = 0
        self.deviceType: str = "00"

        self.inputs: Dict[int, Channel] = {}
        self.outputs: Dict[int, Channel] = {}

    def _extractDeviceInfo(self, json: Dict[str, Any]):
        """Extract device info from request response."""
        self.apiVersion: int = json["Header"]["Version"]
        self.deviceType: str = json["Header"]["Device"]

    @staticmethod
    def _extractChannels(mode: ChannelMode, rawChannels: List[Dict[str, Any]]) -> Dict[int, Channel]:
        """Extract channel info from data array from request."""
        listOfChannels: Dict[int, Channel] = {}
        for chRaw in rawChannels:
            ch: Channel = Channel(mode, chRaw)
            listOfChannels[ch.index] = ch

        return listOfChannels

    async def update(self):
        """Update data."""
        url: str = f"{self.host}/INCLUDE/api.cgi?jsonparam=I,O&jsonnode={self.id}"
        res: Dict[str, Any] = await self._makeRequest(url)

        self._extractDeviceInfo(res)
        self.inputs: Dict[int, Channel] = self._extractChannels(ChannelMode.INPUT, res["Data"]["Inputs"])
        self.outputs: Dict[int, Channel] = self._extractChannels(ChannelMode.OUTPUT, res["Data"]["Outputs"])

    def getDeviceType(self) -> str:
        return DEVICES.get(self.deviceType, "Unknown")

    def __repr__(self) -> str:
        return f"Node {self.id}: Type: {self.getDeviceType()}, Inputs: {len(self.inputs)}, Outputs: {len(self.outputs)}"
