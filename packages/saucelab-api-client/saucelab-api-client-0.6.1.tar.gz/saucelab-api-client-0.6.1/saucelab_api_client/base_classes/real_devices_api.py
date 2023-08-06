import json
import os
import random
import re
from datetime import datetime

from saucelab_api_client.category import Base
from saucelab_api_client.models.device import Device
from saucelab_api_client.models.real_device_job import RealDeviceJob
from saucelab_api_client.models.service import compare_version


class RealDevices(Base):
    __sub_host: str = '/v1/rdc'

    def __init__(self, session):
        super().__init__(session)
        self.__cache = session._device_cache

    def devices_list(self):
        """
        https://docs.saucelabs.com/dev/api/rdc/#get-devices

        Get the set of real devices located at the data center,
        as well as the operating system/browser combinations and identifying information for each device
        :return: List of devices on server
        """
        return [Device(device) for device in self._session.request('get', f'{self.__sub_host}/devices')]

    def get_device_by_id(self, device_id: str):
        """
        https://docs.saucelabs.com/dev/api/rdc/#get-a-specific-device

        Get information about the device specified in the request
        :param device_id: The unique identifier of a device in the Sauce Labs data center
        :return:
        """
        return self._valid(self._session.request('get', f'{self.__sub_host}/devices/{device_id}'), Device)

    def available_devices(self):
        """
        https://docs.saucelabs.com/dev/api/rdc/#get-a-specific-device

        :return: list of Device IDs for all devices in the data center that are currently free for testing
        """
        return self._session.request('get', f'{self.__sub_host}/devices/available')

    def jobs(self, offset: int = None, limit: int = None):
        """
        https://docs.saucelabs.com/dev/api/rdc/#get-real-device-jobs

        Get a list of jobs that are actively running on real devices in the data center
        :param offset: The maximum number of jobs to return
        :param limit: Limit results to those following this index number
        :return:
        """
        params = {key: value for key, value in {'offset': offset, 'limit': limit}.items() if value}
        return self._valid(self._session.request('get', f'{self.__sub_host}/jobs', params=params), RealDeviceJob,
                           key='entities')

    def job_by_id(self, job_id: str):
        """
        https://docs.saucelabs.com/dev/api/rdc/#get-a-specific-real-device-job

        Get information about a specific job running on a real device at the data center
        :param job_id: The unique identifier of a job running on a real device in the data center
        :return:
        """
        # return self._session.request('get', f'{self.__sub_host}/jobs/{job_id}')
        return self._valid(self._session.request('get', f'{self.__sub_host}/jobs/{job_id}'), return_class=RealDeviceJob)

    def filter_devices(self, abi_type=None, api_level=None, cpu_cores=None, cpu_frequency=None, cpu_type=None,
                       default_orientation=None, device_family=None, dpi=None, dpi_name=None,
                       has_on_screen_buttons=None, device_id=None, internal_orientation=None,
                       internal_storage_size=None, is_alternative_io_enabled=None, is_arm=None,
                       is_key_guard_disabled=None, is_private=None, is_rooted=None, is_tablet=None, manufacturer=None,
                       model_number=None, name=None, os_type=None, os_version=None, pixels_per_point=None,
                       ram_size=None, resolution_height=None, resolution_width=None, screen_size=None,
                       sd_card_size=None, supports_appium_web_app_testing=None, supports_global_proxy=None,
                       supports_manual_web_testing=None, supports_minicap_socket_connection=None,
                       supports_mock_locations=None, supports_multi_touch=None, supports_xcui_test=None,
                       min_cpu_cores=None, max_cpu_cores=None, min_cpu_frequency=None, max_cpu_frequency=None,
                       min_dpi=None, max_dpi=None, min_internal_storage_size=None, max_internal_storage_size=None,
                       model_number_contains=None, name_contains=None, name_not_contains=None,
                       model_number_not_contains=None, min_os_version=None, max_os_version=None,
                       min_pixels_per_point=None, max_pixels_per_point=None, min_ram_size=None, max_ram_size=None,
                       min_resolution_height=None, max_resolution_height=None, min_resolution_width=None,
                       max_resolution_width=None, min_screen_size=None, max_screen_size=None, min_sd_card_size=None,
                       max_sd_card_size=None, is_available=None, get_random_devices: int = None, name_regex=None
                       ):
        if get_random_devices is not None:
            if not isinstance(get_random_devices, int):
                raise ValueError('get_random_devices must be integer value')
        local_variables = locals()
        skip_params = ('self', 'local_variables', 'is_available', 'get_random_devices', 'wait_available', 'name_regex')
        main_dict = {key: value for key, value in local_variables.items()
                     if key not in skip_params and '__py' not in key and value is not None}
        main_property = {key: value for key, value in main_dict.items()
                         if key[:3] not in ('max', 'min') and 'contains' not in key}
        min_property = {key[4:]: value for key, value in main_dict.items() if key[:3] == 'min'}
        max_property = {key[4:]: value for key, value in main_dict.items() if key[:3] == 'max'}
        contains_property = {key.replace('_contains', ''): value for key, value in main_dict.items() if
                             'contains' in key and 'not_contains' not in key}
        not_contains_property = {key.replace('_not_contains', ''): value for key, value in main_dict.items() if
                                 '_not_contains' in key}
        if is_available is True:
            available_devices = self.available_devices()

        def device_filter(device: Device):
            if is_available is True:
                if device.device_id not in available_devices:
                    return False
            if all(tuple(str(device.__getattribute__(key)).lower() == str(value).lower()
                         if not isinstance(value, (list, tuple)) else
                         str(device.__getattribute__(key)).lower() in (param.lower() for param in value)
                         for key, value in main_property.items() if value is not None)):
                check_min = all(tuple(device.__getattribute__(key) >= value if key != 'os_version' else
                                      compare_version(device.__getattribute__(key), value) != 'less' for
                                      key, value in min_property.items() if value is not None))
                check_max = all(tuple(device.__getattribute__(key) <= value if key != 'os_version' else
                                      compare_version(device.__getattribute__(key), value) != 'more'
                                      for key, value in max_property.items() if value is not None))
                check_contains = all(tuple(value.lower() in device.__getattribute__(key).lower() for key, value in
                                           contains_property.items() if value is not None))
                check_not_contains = all(
                    tuple(value.lower() not in device.__getattribute__(key).lower() for key, value in
                          not_contains_property.items() if value is not None))
                regex = True
                if name_regex is not None:
                    regex = True if len(re.findall(name_regex, device.device_id)) > 0 else False
                return all((check_min, check_max, check_contains, check_not_contains, regex))
            return False

        result = list(filter(lambda x: device_filter(x), self.devices_list()))
        if get_random_devices is None:
            return result
        else:
            cache_device, need_update = None, False
            if os.path.isfile(self.__cache):
                cache_device = json.loads(open(self.__cache, 'r').read())
            if cache_device is not None:
                create_time = cache_device.get('create_time')
                if create_time is not None:
                    if (datetime.now() - datetime.fromtimestamp(create_time)).seconds > 10:
                        need_update = True
                    else:
                        return [Device(json.loads(from_cache), True) for from_cache in cache_device['devices']]
            if cache_device is None or need_update:
                devices, json_devices = [], []
                for _ in range(get_random_devices):
                    if len(result) > 0:
                        selected = random.choice(result)
                        devices.append(selected), json_devices.append(selected.to_json())
                        result.remove(selected)
                write_json = json.dumps({
                    'create_time': datetime.now().timestamp(),
                    'devices': json_devices
                })
                open(self.__cache, 'w').write(write_json)
                return devices
