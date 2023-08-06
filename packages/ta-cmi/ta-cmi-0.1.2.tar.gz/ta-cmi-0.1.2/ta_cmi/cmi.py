from typing import List

from aiohttp import ClientSession

from .baseApi import BaseAPI
from .device import Device, ReadOnlyClass


class CMI(BaseAPI, metaclass=ReadOnlyClass):
    """Main class to interact with CMI"""

    def __init__(self, host: str, username: str, password: str, session: ClientSession = None):
        """Initialize."""
        super().__init__(username, password, session)
        self.host = host
        self.username = username
        self.password = password

    async def getDevices(self) -> List[Device]:
        """List connected devices."""
        url: str = f"{self.host}/INCLUDE/can_nodes.cgi?_=1"
        data: str = await self._makeRequestNoJson(url)

        nodeIDs: List[str] = data.split(";")

        devices: List[Device] = []

        for nID in nodeIDs:
            if len(nID) == 0:
                continue
            devices.append(Device(nID, self.host, self.username, self.password))

        return devices
