import json


class Device:

    def __init__(self, data: dict, restrore: bool = False):
        if data is not None:
            if restrore:
                for key, value in data.items():
                    self.__setattr__(key, value)
            else:
                self.abi_type: str = data.get('abiType')
                self.api_level: int = data.get('apiLevel')
                self.cpu_cores: int = data.get('cpuCores')
                self.cpu_frequency: int = data.get('cpuFrequency')
                self.default_orientation: str = data.get('defaultOrientation')
                self.dpi: int = data.get('dpi')
                self.has_on_screen_buttons: bool = data.get('hasOnScreenButtons')
                self.device_id: str = data.get('id')
                self.internal_orientation: str = data.get('internalOrientation')
                self.internal_storage_size: int = data.get('internalStorageSize')
                self.is_arm: bool = data.get('isArm')
                self.is_key_guard_disabled: bool = data.get('isKeyGuardDisabled')
                self.is_private: bool = data.get('isPrivate')
                self.is_rooted: bool = data.get('isRooted')
                self.is_tablet: bool = data.get('isTablet')
                self.manufacturer: list = data.get('manufacturer')[0]
                self.model_number: str = data.get('modelNumber')
                self.name: str = data.get('name')
                self.os_type: str = data.get('os')
                self.os_version: str = data.get('osVersion')
                self.pixels_per_point: int = data.get('pixelsPerPoint')
                self.ram_size: int = data.get('ramSize')
                self.resolution_height: int = data.get('resolutionHeight')
                self.resolution_width: int = data.get('resolutionWidth')
                self.screen_size: float = data.get('screenSize')
                self.sd_card_size: int = data.get('sdCardSize')
                self.supports_appium_web_app_testing: bool = data.get('supportsAppiumWebAppTesting')
                self.supports_global_proxy: bool = data.get('supportsGlobalProxy')
                self.supports_minicap_socket_connection: bool = data.get('supportsMinicapSocketConnection')
                self.supports_mock_locations: bool = data.get('supportsMockLocations')
                self.cpu_type: str = data.get('cpuType')
                self.device_family: str = data.get('deviceFamily')
                self.dpi_name: str = data.get('dpiName')
                self.is_alternative_io_enabled: bool = data.get('isAlternativeIoEnabled')
                self.supports_manual_web_testing: bool = data.get('supportsManualWebTesting')
                self.supports_multi_touch: bool = data.get('supportsMultiTouch')
                self.supports_xcui_test: bool = data.get('supportsXcuiTest')

    def __str__(self):
        return self.name

    def to_json(self):
        return json.dumps(self.__dict__)
