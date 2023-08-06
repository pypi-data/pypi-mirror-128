class Status:
    def __init__(self, data: dict):
        if data is not None:
            self.wait_time: float = data.get('wait_time')
            self.service_operational: bool = data.get('service_operational')
            self.status_message: str = data.get('status_message')

    def __str__(self):
        return self.status_message


class WebDriverPlatform:
    def __init__(self, data: dict):
        if data is not None:
            self.short_version: str = data.get('short_version')
            self.long_name: str = data.get('long_name')
            self.api_name: str = data.get('api_name')
            self.long_version: str = data.get('long_version')
            self.device: str = data.get('device')
            self.latest_stable_version: str = data.get('latest_stable_version')
            self.automation_backend: str = data.get('automation_backend')
            self.os_type: str = data.get('os')

    def __str__(self):
        return self.long_name


class AppiumPlatform:
    def __init__(self, data: dict):
        if data is not None:
            self.deprecated_backend_versions: list = data.get('deprecated_backend_versions')
            self.short_version: str = data.get('short_version')
            self.long_name: str = data.get('long_name')
            self.recommended_backend_version: str = data.get('recommended_backend_version')
            self.long_version: str = data.get('long_version')
            self.api_name: str = data.get('api_name')
            self.supported_backend_versions: list = data.get('supported_backend_versions')
            self.device: str = data.get('device')
            self.latest_stable_version: str = data.get('latest_stable_version')
            self.automation_backend: str = data.get('automation_backend')
            self.os_type: str = data.get('os')

    def __str__(self):
        return self.long_name
