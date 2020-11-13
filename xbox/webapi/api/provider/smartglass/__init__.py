"""
SmartGlass - Control Registered Devices
"""
from typing import List, Optional
from uuid import uuid4

from aiohttp import ClientResponse

from xbox.webapi.api.provider.baseprovider import BaseProvider
from xbox.webapi.api.provider.smartglass.models import (
    CommandResponse,
    GuideTab,
    InputKeyType,
    InstalledPackagesList,
    OperationStatusResponse,
    SmartglassConsoleList,
    SmartglassConsoleStatus,
    StorageDevicesList,
    VolumeDirection,
)


class SmartglassProvider(BaseProvider):
    SG_URL = "https://xccs.xboxlive.com"
    HEADERS_SG = {
        "x-xbl-contract-version": "4",
        "skillplatform": "RemoteManagement",
    }

    def __init__(self, client):
        """
        Initialize Baseclass, create smartglass session id

        Args: Instance of XBL client
        """
        super().__init__(client)
        self._smartglass_session_id = str(uuid4())

    async def get_console_list(
        self, include_storage_devices: bool = True, **kwargs
    ) -> SmartglassConsoleList:
        """
        Get Console list

        Args:
            include_storage_devices: Include a list of storage devices in the response

        Returns: Console List
        """
        params = {
            "queryCurrentDevice": "false",
            "includeStorageDevices": str(include_storage_devices).lower(),
        }
        resp = await self._fetch_list("devices", params, **kwargs)
        return SmartglassConsoleList.parse_raw(await resp.text())

    async def get_installed_apps(
        self, device_id: Optional[str] = None, **kwargs
    ) -> InstalledPackagesList:
        """
        Get Installed Apps

        Args:
            device_id: ID of console (from console list)

        Returns: Installed Apps
        """
        params = {}
        if device_id:
            params["deviceId"] = device_id
        resp = await self._fetch_list("installedApps", params, **kwargs)
        return InstalledPackagesList.parse_raw(await resp.text())

    async def get_storage_devices(self, device_id: str, **kwargs) -> StorageDevicesList:
        """
        Get Installed Apps

        Args:
            device_id: ID of console (from console list)

        Returns: Storage Devices list
        """
        params = {"deviceId": device_id}
        resp = await self._fetch_list("storageDevices", params, **kwargs)
        return StorageDevicesList.parse_raw(await resp.text())

    async def get_console_status(
        self, device_id: str, **kwargs
    ) -> SmartglassConsoleStatus:
        """
        Get Console Status

        Args:
            device_id: ID of console (from console list)

        Returns: Console Status
        """
        url = f"{self.SG_URL}/consoles/{device_id}"
        resp = await self.client.session.get(url, headers=self.HEADERS_SG, **kwargs)
        resp.raise_for_status()
        return SmartglassConsoleStatus.parse_raw(await resp.text())

    async def get_op_status(
        self, device_id: str, op_id: str, **kwargs
    ) -> OperationStatusResponse:
        """
        Get Operation Status

        Args:
            device_id: ID of console (from console list)
            op_id: Operation ID (from previous command)

        Returns: Operation Status
        """
        url = f"{self.SG_URL}/opStatus"
        headers = {
            "x-xbl-contract-version": "3",
            "x-xbl-opId": op_id,
            "x-xbl-deviceId": device_id,
        }
        resp = await self.client.session.get(url, headers=headers, **kwargs)
        resp.raise_for_status()
        return OperationStatusResponse.parse_raw(await resp.text())

    async def wake_up(self, device_id: str, **kwargs) -> CommandResponse:
        """
        Wake Up Console

        Args:
            device_id: ID of console (from console list)

        Returns: Command Response
        """
        return await self._send_one_shot_command(device_id, "Power", "WakeUp", **kwargs)

    async def turn_off(self, device_id: str, **kwargs) -> CommandResponse:
        """
        Turn Off Console

        Args:
            device_id: ID of console (from console list)

        Returns: Command Response
        """
        return await self._send_one_shot_command(
            device_id, "Power", "TurnOff", **kwargs
        )

    async def reboot(self, device_id: str, **kwargs) -> CommandResponse:
        """
        Reboot Console

        Args:
            device_id: ID of console (from console list)

        Returns: Command Response
        """
        return await self._send_one_shot_command(device_id, "Power", "Reboot", **kwargs)

    async def mute(self, device_id: str, **kwargs) -> CommandResponse:
        """
        Mute

        Args:
            device_id: ID of console (from console list)

        Returns: Command Response
        """
        return await self._send_one_shot_command(device_id, "Audio", "Mute", **kwargs)

    async def unmute(self, device_id: str, **kwargs) -> CommandResponse:
        """
        Unmute

        Args:
            device_id: ID of console (from console list)

        Returns: Command Response
        """
        return await self._send_one_shot_command(device_id, "Audio", "Unmute", **kwargs)

    async def volume(
        self, device_id: str, direction: VolumeDirection, amount: int = 1, **kwargs
    ) -> CommandResponse:
        """
        Adjust Volume

        Args:
            device_id: ID of console (from console list)

        Returns: Command Response
        """
        params = [{"direction": direction.value, "amount": str(amount)}]
        return await self._send_one_shot_command(
            device_id, "Audio", "Volume", params, **kwargs
        )

    async def play(self, device_id: str, **kwargs) -> CommandResponse:
        """
        Play (media controls)

        Args:
            device_id: ID of console (from console list)

        Returns: Command Response
        """
        return await self._send_one_shot_command(device_id, "Media", "Play", **kwargs)

    async def pause(self, device_id: str, **kwargs) -> CommandResponse:
        """
        Pause (media controls)

        Args:
            device_id: ID of console (from console list)

        Returns: Command Response
        """
        return await self._send_one_shot_command(device_id, "Media", "Pause", **kwargs)

    async def previous(self, device_id: str, **kwargs) -> CommandResponse:
        """
        Previous (media controls)

        Args:
            device_id: ID of console (from console list)

        Returns: Command Response
        """
        return await self._send_one_shot_command(
            device_id, "Media", "Previous", **kwargs
        )

    async def next(self, device_id: str, **kwargs) -> CommandResponse:
        """
        Next (media controls)

        Args:
            device_id: ID of console (from console list)

        Returns: Command Response
        """
        return await self._send_one_shot_command(device_id, "Media", "Next", **kwargs)

    async def go_home(self, device_id: str, **kwargs) -> CommandResponse:
        """
        Go Home

        Args:
            device_id: ID of console (from console list)

        Returns: Command Response
        """
        return await self._send_one_shot_command(device_id, "Shell", "GoHome", **kwargs)

    async def go_back(self, device_id: str, **kwargs) -> CommandResponse:
        """
        Go Back

        Args:
            device_id: ID of console (from console list)

        Returns:
            :class:`SmartglassConsoleStatus`: Command Response
        """
        return await self._send_one_shot_command(device_id, "Shell", "GoBack", **kwargs)

    async def show_guide_tab(
        self, device_id: str, tab: GuideTab = GuideTab.Guide, **kwargs
    ) -> CommandResponse:
        """
        Show Guide Tab

        Args:
            device_id: ID of console (from console list)

        Returns: Command Response
        """
        params = [{"tabName": tab.value}]
        return await self._send_one_shot_command(
            device_id, "Shell", "ShowGuideTab", params, **kwargs
        )

    async def press_button(
        self, device_id: str, button: InputKeyType, **kwargs
    ) -> CommandResponse:
        """
        Press Button

        Args:
            device_id: ID of console (from console list)

        Returns: Command Response
        """
        params = [{"keyType": button.value}]
        return await self._send_one_shot_command(
            device_id, "Shell", "InjectKey", params, **kwargs
        )

    async def insert_text(self, device_id: str, text: str, **kwargs) -> CommandResponse:
        """
        Insert Text

        Args:
            device_id: ID of console (from console list)

        Returns: Command Response
        """
        params = [{"replacementString": text}]
        return await self._send_one_shot_command(
            device_id, "Shell", "InjectString", params, **kwargs
        )

    async def launch_app(
        self, device_id: str, one_store_product_id: str, **kwargs
    ) -> CommandResponse:
        """
        Launch Application

        Args:
            device_id: ID of console (from console list)
            one_store_product_id: OneStoreProductID for the app to launch

        Returns: Command Response
        """
        params = [{"oneStoreProductId": one_store_product_id}]
        return await self._send_one_shot_command(
            device_id,
            "Shell",
            "ActivateApplicationWithOneStoreProductId",
            params,
            **kwargs,
        )

    async def show_tv_guide(self, device_id: str, **kwargs) -> CommandResponse:
        """
        Show TV Guide

        Args:
            device_id: ID of console (from console list)

        Returns: Command Response
        """
        return await self._send_one_shot_command(device_id, "TV", "ShowGuide", **kwargs)

    async def _fetch_list(
        self, list_name: str, params: Optional[dict] = None, **kwargs
    ) -> ClientResponse:
        """
        Fetch arbitrary list

        Args:
            list_name: name of list
            params: query params

        Returns:
            :class:`aiohttp.ClientResponse`: HTTP Response
        """
        url = f"{self.SG_URL}/lists/{list_name}"
        resp = await self.client.session.get(
            url, params=params, headers=self.HEADERS_SG, **kwargs
        )
        resp.raise_for_status()
        return resp

    async def _send_one_shot_command(
        self,
        device_id: str,
        command_type: str,
        command: str,
        params: Optional[List[dict]] = None,
        **kwargs,
    ) -> CommandResponse:
        """
        Send One Shot command to console

        Args:
            device_id: ID of console (from console list)
            type: type of command
            command: name of command
            params: command parameters

        Returns: Command Response
        """
        url = f"{self.SG_URL}/commands"
        body = {
            "destination": "Xbox",
            "type": command_type,
            "command": command,
            "sessionId": self._smartglass_session_id,
            "sourceId": "com.microsoft.smartglass",
            "parameters": params or [{}],
            "linkedXboxId": device_id,
        }
        resp = await self.client.session.post(
            url, json=body, headers=self.HEADERS_SG, **kwargs
        )
        resp.raise_for_status()
        return CommandResponse.parse_raw(await resp.text())
