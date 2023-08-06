class Job:
    def __init__(self, data: dict):
        if data is not None:
            self.browser_short_version: str = data.get('browser_short_version')
            self.video_url: str = data.get('video_url')
            self.creation_time: int = data.get('creation_time')
            self.custom_data = data.get('custom-data')
            self.browser_version: str = data.get('browser_version')
            self.owner: str = data.get('owner')
            self.automation_backend: str = data.get('automation_backend')
            self.job_id: str = data.get('id')
            self.collects_automator_log: bool = data.get('collects_automator_log')
            self.record_screenshots: bool = data.get('record_screenshots')
            self.record_video: bool = data.get('record_video')
            self.build = data.get('build')
            self.passed = data.get('passed')
            self.public: str = data.get('public')
            self.assigned_tunnel_id = data.get('assigned_tunnel_id')
            self.status: str = data.get('status')
            self.log_url: str = data.get('log_url')
            self.start_time: int = data.get('start_time')
            self.proxied: bool = data.get('proxied')
            self.modification_time: int = data.get('modification_time')
            self.tags: list = data.get('tags')
            self.name: str = data.get('name')
            self.commands_not_successful: int = data.get('commands_not_successful')
            self.consolidated_status: str = data.get('consolidated_status')
            self.selenium_version = data.get('selenium_version')
            self.manual: bool = data.get('manual')
            self.end_time: int = data.get('end_time')
            self.error: str = data.get('error')
            self.os: str = data.get('os')
            self.breakpointed = data.get('breakpointed')
            self.browser: str = data.get('browser')

    def __str__(self):
        return self.name


class JobSearch:
    def __init__(self, data: dict):
        if data is not None:
            self.status: str = data.get('status')
            self.base_config: JobBaseConfig = JobBaseConfig(data.get('base_config'))
            self.command_counts: dict = data.get('command_counts')
            self.deletion_time = data.get('deletion_time')
            self.url = data.get('url')
            self.org_id: str = data.get('org_id')
            self.creation_time: int = data.get('creation_time')
            self.job_id: str = data.get('id')
            self.team_id: str = data.get('team_id')
            self.performance_enabled = data.get('performance_enabled')
            self.assigned_tunnel_id = data.get('assigned_tunnel_id')
            self.container: bool = data.get('container')
            self.group_id: str = data.get('group_id')
            self.public: str = data.get('public')
            self.breakpointed = data.get('breakpointed')


class JobBaseConfig:
    def __init__(self, data: dict):
        if data is not None:
            self.sauce_options: dict = data.get('sauce:options')
            self.appium_new_command_timeout: int = data.get('appium:newCommandTimeout')
            self.browser_name: str = data.get('browserName')
            self.appium_device_name: str = data.get('appium:deviceName')
            self.appium_platform_version: str = data.get('appium:platformVersion')
            self.platform_name: str = data.get('platformName')


class JobAssets:
    def __init__(self, data: dict):
        if data is not None:
            self.video_mp4: str = data.get('video.mp4')
            self.selenium_log: str = data.get('selenium-log')
            self.sauce_log: str = data.get('sauce-log')
            self.video: str = data.get('video')
            self.logcat_log: str = data.get('logcat.log')
            self.screenshots: list = data.get('screenshots')
            self.automator_log: str = data.get('automator.log')
            self.network_har: str = data.get('network.har')
            self.performance_json: str = data.get('performance.json')
