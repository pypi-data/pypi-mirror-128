from saucelab_api_client.models.device import Device
from saucelab_api_client.models.file import FileSummary


class RealDeviceJob:
    def __init__(self, data: dict):
        self.application_summary: FileSummary = FileSummary(data.get('application_summary'))
        self.assigned_tunnel_id = data.get('assigned_tunnel_id')
        self.device_type: str = data.get('device_type')
        self.owner_sauce: str = data.get('owner_sauce')
        self.automation_backend: str = data.get('automation_backend')
        self.base_config: dict = data.get('base_config')
        self.build = data.get('build')
        self.collects_automator_log: bool = data.get('collects_automator_log')
        self.consolidated_status: str = data.get('consolidated_status')
        self.creation_time: int = data.get('creation_time')
        self.device_descriptor: Device = Device(data.get('device_descriptor'))
        self.end_time: int = data.get('end_time')
        self.error = data.get('error')
        self.job_id: str = data.get('id')
        self.framework_log_url: str = data.get('framework_log_url')
        self.device_log_url: str = data.get('device_log_url')
        self.requests_url: str = data.get('requests_url')
        self.test_cases_url = data.get('test_cases_url')
        self.manual: bool = data.get('manual')
        self.modification_time: int = data.get('modification_time')
        self.name: str = data.get('name')
        self.os: str = data.get('os')
        self.os_version: str = data.get('os_version')
        self.device_name: str = data.get('device_name')
        self.passed = data.get('passed')
        self.proxied: bool = data.get('proxied')
        self.record_screenshots: bool = data.get('record_screenshots')
        self.screenshots: list = data.get('screenshots')
        self.record_video: bool = data.get('record_video')
        self.start_time: int = data.get('start_time')
        self.status: str = data.get('status')
        self.tags: list = data.get('tags')
        self.video_url: str = data.get('video_url')
        self.remote_app_file_url: str = data.get('remote_app_file_url')
        self.appium_session_id: str = data.get('appium_session_id')
        self.device_session_id = data.get('device_session_id')
        self.client: str = data.get('client')

    def __str__(self):
        return self.name
