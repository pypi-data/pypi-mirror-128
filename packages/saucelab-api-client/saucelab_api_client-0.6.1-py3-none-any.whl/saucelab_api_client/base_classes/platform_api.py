from datetime import datetime

from saucelab_api_client.category import Base
from saucelab_api_client.models.platform_ import Status, WebDriverPlatform, AppiumPlatform


class Platform(Base):
    __sub_host = '/rest/v1/info'

    def get_status(self):
        """
        https://docs.saucelabs.com/dev/api/platform/#get-sauce-labs-teststatus

        Returns the current (30 second cache) availability of the Sauce Labs platform
        :return: Status or str
        """
        return self._valid(self._session.request('get', f'{self.__sub_host}/status'), Status)

    def get_supported_platforms(self, automation_api: str):
        """
        https://docs.saucelabs.com/dev/api/platform/#get-supported-platforms

        Returns the set of supported operating system and browser combinations for the specified automation framework
        :param automation_api: The framework for which you are requesting supported platforms. Valid values are:
                    - all
                    - appium
                    - webdriver
        :return:
        """
        response = self._session.request('get', f'{self.__sub_host}/platforms/{automation_api}')
        if isinstance(response, str):
            return response
        else:
            return tuple(WebDriverPlatform(automation) if automation['automation_backend'] == 'webdriver'
                         else AppiumPlatform(automation) for automation in response)

    def get_end_of_life_date_appium_versions(self):
        """
        https://docs.saucelabs.com/dev/api/platform/#get-end-of-life-dates-for-appium-versions

        Returns the expected date (in Unix time) on which Sauce Labs support for each
        Appium version is to be discontinued
        :return:
        """
        response = self._session.request('get', f'{self.__sub_host}/platforms/appium/eol')
        if isinstance(response, str):
            return response
        else:
            return {key: value if value is None else datetime.utcfromtimestamp(value) for key, value in
                    response.items()}
