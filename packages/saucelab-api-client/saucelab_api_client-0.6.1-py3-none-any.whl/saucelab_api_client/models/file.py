class File:
    def __init__(self, data: dict):
        if data is not None:
            self.file_id: str = data.get('id')
            self.owner: dict = data.get('owner')
            self.name: str = data.get('name')
            self.upload_timestamp: int = data.get('upload_timestamp')
            self.etag: str = data.get('etag')
            self.kind: str = data.get('kind')
            self.group_id: int = data.get('group_id')
            self.description = data.get('description')
            self.metadata: Metadata = Metadata(data.get('metadata'))
            self.access: dict = data.get('access')
            self.sha256: str = data.get('sha256')

    def __str__(self):
        return self.name


class Metadata:
    def __init__(self, data: dict):
        if data is not None:
            self.identifier: str = data.get('identifier')
            self.name: str = data.get('name')
            self.version: str = data.get('version')
            self.is_test_runner: bool = data.get('is_test_runner')
            self.icon = data.get('icon')
            self.short_version: str = data.get('short_version')
            self.is_simulator: bool = data.get('is_simulator')
            self.min_os: str = data.get('min_os')
            self.target_os: str = data.get('target_os')
            self.test_runner_plugin_path = data.get('test_runner_plugin_path')
            self.vesrion_code: int = data.get('vesrion_code')
            self.min_sdk: int = data.get('min_sdk')
            self.target_sdk: int = data.get('target_sdk')
            self.test_runner_class = data.get('test_runner_class')

    def __str__(self):
        return self.identifier


class FileSummary:
    def __init__(self, data: dict):
        if data is not None:
            self.app_storage_id: str = data.get('appStorageId')
            self.group_id: int = data.get('groupId')
            self.filename: str = data.get('filename')
            self.name: str = data.get('name')
            self.version: str = data.get('version')
            self.short_version: str = data.get('shortVersion')
            self.min_os_version: str = data.get('minOsVersion')
            self.target_os_version: str = data.get('targetOsVersion')

    def __str__(self):
        return self.name
