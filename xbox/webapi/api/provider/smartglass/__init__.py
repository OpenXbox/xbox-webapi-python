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

        Args:
            client (:class:`XboxLiveClient`): Instance of client
        """
        super().__init__(client)
        self._smartglass_session_id = str(uuid4())

    async def get_console_list(
        self, include_storage_devices: bool = True
    ) -> SmartglassConsoleList:
        """
        Get Console list

        Args:
            include_storage_devices: Include a list of storage devices in the response

        Returns:
            :class:`SmartglassConsoleList`: Console List
        """
        params = {
            "queryCurrentDevice": "false",
            "includeStorageDevices": str(include_storage_devices).lower(),
        }
        resp = await self._fetch_list("devices", params)
        return SmartglassConsoleList.parse_raw(await resp.text())

    async def get_installed_apps(self, device_id: str) -> InstalledPackagesList:
        """
        Get Installed Apps

        Args:
            device_id: ID of console (from console list)

        Returns:
            :class:`InstalledPackagesList`: Installed Apps
        """
        params = {"deviceId": device_id}
        resp = await self._fetch_list("installedApps", params)
        return InstalledPackagesList.parse_raw(await resp.text())

    async def get_storage_devices(self, device_id: str) -> StorageDevicesList:
        """
        Get Installed Apps

        Args:
            device_id: ID of console (from console list)

        Returns:
            :class:`StorageDevicesList`: Storage Devices
        """
        params = {"deviceId": device_id}
        resp = await self._fetch_list("storageDevices", params)
        return StorageDevicesList.parse_raw(await resp.text())

    async def get_console_status(self, device_id: str) -> SmartglassConsoleStatus:
        """
        Get Console Status

        Args:
            device_id: ID of console (from console list)

        Returns:
            :class:`SmartglassConsoleStatus`: Console Status
        """
        url = f"{self.SG_URL}/consoles/{device_id}"
        resp = await self.client.session.get(url, headers=self.HEADERS_SG)
        resp.raise_for_status()
        return SmartglassConsoleStatus.parse_raw(await resp.text())

    async def get_op_status(
        self, device_id: str, op_id: str
    ) -> OperationStatusResponse:
        """
        Get Operation Status

        Args:
            device_id: ID of console (from console list)
            op_id: Operation ID (from previous command)

        Returns:
            :class:`OperationStatusResponse`: Operation Status
        """
        url = f"{self.SG_URL}/opStatus"
        headers = {
            "x-xbl-contract-version": "3",
            "x-xbl-opId": op_id,
            "x-xbl-deviceId": device_id,
        }
        resp = await self.client.session.get(url, headers=headers)
        resp.raise_for_status()
        return OperationStatusResponse.parse_raw(await resp.text())

    async def wake_up(self, device_id: str) -> CommandResponse:
        """
        Wake Up Console

        Args:
            device_id: ID of console (from console list)

        Returns:
            :class:`SmartglassConsoleStatus`: Command Response
        """
        return await self._send_one_shot_command(device_id, "Power", "WakeUp")

    async def turn_off(self, device_id: str) -> CommandResponse:
        """
        Turn Off Console

        Args:
            device_id: ID of console (from console list)

        Returns:
            :class:`SmartglassConsoleStatus`: Command Response
        """
        return await self._send_one_shot_command(device_id, "Power", "TurnOff")

    async def reboot(self, device_id: str) -> CommandResponse:
        """
        Reboot Console

        Args:
            device_id: ID of console (from console list)

        Returns:
            :class:`SmartglassConsoleStatus`: Command Response
        """
        return await self._send_one_shot_command(device_id, "Power", "Reboot")

    async def mute(self, device_id: str) -> CommandResponse:
        """
        Mute

        Args:
            device_id: ID of console (from console list)

        Returns:
            :class:`SmartglassConsoleStatus`: Command Response
        """
        return await self._send_one_shot_command(device_id, "Audio", "Mute")

    async def unmute(self, device_id: str) -> CommandResponse:
        """
        Unmute

        Args:
            device_id: ID of console (from console list)

        Returns:
            :class:`SmartglassConsoleStatus`: Command Response
        """
        return await self._send_one_shot_command(device_id, "Audio", "Unmute")

    async def volume(
        self, device_id: str, direction: VolumeDirection, amount: int = 1
    ) -> CommandResponse:
        """
        Adjust Volume

        Args:
            device_id: ID of console (from console list)

        Returns:
            :class:`SmartglassConsoleStatus`: Command Response
        """
        params = [{"direction": direction.value, "amount": str(amount)}]
        return await self._send_one_shot_command(device_id, "Audio", "Volume", params)

    async def play(self, device_id: str) -> CommandResponse:
        """
        Play (media controls)

        Args:
            device_id: ID of console (from console list)

        Returns:
            :class:`SmartglassConsoleStatus`: Command Response
        """
        return await self._send_one_shot_command(device_id, "Media", "Play")

    async def pause(self, device_id: str) -> CommandResponse:
        """
        Pause (media controls)

        Args:
            device_id: ID of console (from console list)

        Returns:
            :class:`SmartglassConsoleStatus`: Command Response
        """
        return await self._send_one_shot_command(device_id, "Media", "Pause")

    async def previous(self, device_id: str) -> CommandResponse:
        """
        Previous (media controls)

        Args:
            device_id: ID of console (from console list)

        Returns:
            :class:`SmartglassConsoleStatus`: Command Response
        """
        return await self._send_one_shot_command(device_id, "Media", "Previous")

    async def next(self, device_id: str) -> CommandResponse:
        """
        Next (media controls)

        Args:
            device_id: ID of console (from console list)

        Returns:
            :class:`SmartglassConsoleStatus`: Command Response
        """
        return await self._send_one_shot_command(device_id, "Media", "Next")

    async def go_home(self, device_id: str) -> CommandResponse:
        """
        Go Home

        Args:
            device_id: ID of console (from console list)

        Returns:
            :class:`SmartglassConsoleStatus`: Command Response
        """
        return await self._send_one_shot_command(device_id, "Shell", "GoHome")

    async def go_back(self, device_id: str) -> CommandResponse:
        """
        Go Back

        Args:
            device_id: ID of console (from console list)

        Returns:
            :class:`SmartglassConsoleStatus`: Command Response
        """
        return await self._send_one_shot_command(device_id, "Shell", "GoBack")

    async def show_guide_tab(
        self, device_id: str, tab: GuideTab = GuideTab.Guide
    ) -> CommandResponse:
        """
        Show Guide Tab

        Args:
            device_id: ID of console (from console list)

        Returns:
            :class:`SmartglassConsoleStatus`: Command Response
        """
        params = [{"tabName": tab.value}]
        return await self._send_one_shot_command(
            device_id, "Shell", "ShowGuideTab", params
        )

    async def press_button(
        self, device_id: str, button: InputKeyType
    ) -> CommandResponse:
        """
        Press Button

        Args:
            device_id: ID of console (from console list)

        Returns:
            :class:`SmartglassConsoleStatus`: Command Response
        """
        params = [{"keyType": button.value}]
        return await self._send_one_shot_command(
            device_id, "Shell", "InjectKey", params
        )

    async def insert_text(self, device_id: str, text: str) -> CommandResponse:
        """
        Insert Text

        Args:
            device_id: ID of console (from console list)

        Returns:
            :class:`SmartglassConsoleStatus`: Command Response
        """
        params = [{"replacementString": text}]
        return await self._send_one_shot_command(
            device_id, "Shell", "InjectString", params
        )

    async def launch_app(
        self, device_id: str, one_store_product_id: str
    ) -> CommandResponse:
        """
        Launch Application

        Args:
            device_id: ID of console (from console list)
            one_store_product_id: OneStoreProductID for the app to launch

        Returns:
            :class:`SmartglassConsoleStatus`: Command Response
        """
        params = [{"oneStoreProductId": one_store_product_id}]
        return await self._send_one_shot_command(
            device_id, "Shell", "ActivateApplicationWithOneStoreProductId", params
        )

    async def show_tv_guide(self, device_id: str) -> CommandResponse:
        """
        Show TV Guide

        Args:
            device_id: ID of console (from console list)

        Returns:
            :class:`SmartglassConsoleStatus`: Command Response
        """
        return await self._send_one_shot_command(device_id, "TV", "ShowGuide")

    async def _fetch_list(
        self, list_name: str, params: Optional[dict] = None
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
            url, params=params, headers=self.HEADERS_SG
        )
        resp.raise_for_status()
        return resp

    async def _send_one_shot_command(
        self,
        device_id: str,
        command_type: str,
        command: str,
        params: Optional[List[dict]] = None,
    ) -> CommandResponse:
        """
        Send One Shot command to console

        Args:
            device_id: ID of console (from console list)
            type: type of command
            command: name of command
            params: command parameters

        Returns:
            :class:`CommandResponse`: Command Response
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
        resp = await self.client.session.post(url, json=body, headers=self.HEADERS_SG)
        resp.raise_for_status()
        return CommandResponse.parse_raw(await resp.text())
