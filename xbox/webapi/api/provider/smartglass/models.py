from datetime import datetime
from enum import Enum
from typing import List, Optional

from xbox.webapi.common.models import CamelCaseModel

# Responses


class ConsoleType(str, Enum):
    XboxOne = "XboxOne"
    XboxOneS = "XboxOneS"
    XboxOneSDigital = "XboxOneSDigital"
    XboxOneX = "XboxOneX"
    XboxSeriesS = "XboxSeriesS"
    XboxSeriesX = "XboxSeriesX"


class PowerState(str, Enum):
    Unknown = "Unknown"
    On = "On"
    Off = "Off"
    ConnectedStandby = "ConnectedStandby"
    SystemUpdate = "SystemUpdate"


class PlaybackState(str, Enum):
    Unknown = "Unknown"
    Playing = "Playing"
    Paused = "Paused"
    Stopped = "Stopped"


class ErrorCode(str, Enum):
    OK = "OK"
    CurrentConsoleNotFound = "CurrentConsoleNotFound"
    RemoteManagementDisabled = "RemoteManagementDisabled"
    XboxDataNotFound = "XboxDataNotFound"
    XboxNotPaired = "XboxNotPaired"


class OpStatus(str, Enum):
    Paused = "Paused"
    OffConsoleError = "OffConsoleError"
    Pending = "Pending"
    TimedOut = "TimedOut"
    Error = "Error"
    Succeeded = "Succeeded"


class SmartglassApiStatus(CamelCaseModel):
    error_code: str
    error_message: Optional[str]


class StorageDevice(CamelCaseModel):
    storage_device_id: str
    storage_device_name: str
    is_default: bool
    total_space_bytes: float
    free_space_bytes: float


class SmartglassConsole(CamelCaseModel):
    id: str
    name: str
    console_type: ConsoleType
    power_state: PowerState
    console_streaming_enabled: bool
    digital_assistant_remote_control_enabled: bool
    remote_management_enabled: bool
    storage_devices: Optional[List[StorageDevice]]


class SmartglassConsoleList(CamelCaseModel):
    agent_user_id: Optional[str]
    result: List[SmartglassConsole]
    status: SmartglassApiStatus


class SmartglassConsoleStatus(CamelCaseModel):
    power_state: PowerState
    console_streaming_enabled: bool
    digital_assistant_remote_control_enabled: bool
    remote_management_enabled: bool
    focus_app_aumid: str
    is_tv_configured: bool
    login_state: Optional[str]
    playback_state: PlaybackState
    power_state: PowerState
    storage_devices: Optional[List[StorageDevice]]
    status: SmartglassApiStatus


class InstalledPackage(CamelCaseModel):
    one_store_product_id: Optional[str]
    title_id: int
    aumid: Optional[str]
    last_active_time: Optional[datetime]
    is_game: bool
    name: Optional[str]
    content_type: str
    instance_id: str
    storage_device_id: str
    unique_id: str
    legacy_product_id: Optional[str]
    version: int
    size_in_bytes: int
    install_time: datetime
    update_time: Optional[datetime]
    parent_id: Optional[str]


class InstalledPackagesList(CamelCaseModel):
    result: List[InstalledPackage]
    status: SmartglassApiStatus
    agent_user_id: Optional[str]


class StorageDevicesList(CamelCaseModel):
    device_id: str
    result: List[StorageDevice]
    status: SmartglassApiStatus


class OpStatusNode(CamelCaseModel):
    operation_status: OpStatus
    op_id: str
    originating_session_id: str
    command: str
    succeeded: bool
    console_status_code: Optional[int]
    xccs_error_code: Optional[ErrorCode]
    h_result: Optional[int]
    message: Optional[str]


class OperationStatusResponse(CamelCaseModel):
    op_status_list: List[OpStatusNode]
    status: SmartglassApiStatus


class CommandDestination(CamelCaseModel):
    id: str
    name: str
    power_state: PowerState
    remote_management_enabled: bool
    console_streaming_enabled: bool
    console_type: ConsoleType
    wireless_warning: Optional[str]
    out_of_home_warning: Optional[str]


class CommandResponse(CamelCaseModel):
    result: Optional[str]
    ui_text: Optional[str]
    destination: CommandDestination
    user_info: Optional[str]
    op_id: str
    status: SmartglassApiStatus


# Requests


class VolumeDirection(str, Enum):
    Up = "Up"
    Down = "Down"


class InputKeyType(str, Enum):
    Guide = "Guide"
    Menu = "Menu"
    View = "View"
    A = "A"
    B = "B"
    X = "X"
    Y = "Y"
    Up = "Up"
    Down = "Down"
    Left = "Left"
    Right = "Right"


class GuideTab(str, Enum):
    Guide = "Guide"
