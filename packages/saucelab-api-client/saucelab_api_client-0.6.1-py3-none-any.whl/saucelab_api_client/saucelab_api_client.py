from saucelab_api_client.base_classes.accounts_api import Accounts
from saucelab_api_client.base_classes.insights_api import Insights
from saucelab_api_client.base_classes.insights_real_devices_api import InsightsRealDeviceApi
from saucelab_api_client.base_classes.job_api import JobsApi
from saucelab_api_client.base_classes.performance_api import PerformanceApi
from saucelab_api_client.base_classes.platform_api import Platform
from saucelab_api_client.base_classes.real_devices_api import RealDevices
from saucelab_api_client.base_classes.sauce_connect_api import SauceConnectApi
from saucelab_api_client.base_classes.storage_api import Storage
from saucelab_api_client.session import Session


class SauceLab(Session):

    @property
    def devices(self):
        return RealDevices(self)

    @property
    def insights(self):
        return Insights(self)

    @property
    def storage(self):
        return Storage(self)

    @property
    def accounts(self):
        return Accounts(self)

    @property
    def platform(self):
        return Platform(self)

    @property
    def jobs(self):
        return JobsApi(self)

    @property
    def performance(self):
        return PerformanceApi(self)

    @property
    def sauce_connect(self):
        return SauceConnectApi(self)

    @property
    def real_devices_insights(self):
        return InsightsRealDeviceApi(self)
