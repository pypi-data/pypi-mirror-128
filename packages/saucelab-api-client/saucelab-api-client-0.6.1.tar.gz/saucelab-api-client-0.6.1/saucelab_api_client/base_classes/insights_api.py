from datetime import datetime

from saucelab_api_client.category import Base
from saucelab_api_client.models.insights import Insight
from saucelab_api_client.models.service import get_dict_from_locals, get_datetime_for_insights


class Insights(Base):
    __sub_host = '/v1/analytics'

    def test_results(self, start: datetime, end: datetime, scope=None, owner=None, status=None, build=None, from_=None,
                     max_results=None, missing_build=None, query=None, desc=None, error=None):
        """
        https://docs.saucelabs.com/dev/api/insights/#get-test-results

        Returns run data for all tests that match the request criteria
        :param start: The starting date of the period during which the test runs executed, in YYY-MM-DDTHH:MM:SSZ
                            or Unix time format.
        :param end: The ending date of the period during which the test runs executed, in YYY-MM-DDTHH:MM:SSZ
                            or Unix time format.
        :param scope: Specifies the scope of the owner parameter
        :param owner: The name of one or more users in the requestor's organization who executed the requested tests.
                            This parameter is required if the scope parameter is set to single.
        :param status: Limit results to only those with a specified status
        :param build: Limit results to those grouped by this build name
        :param from_: Begin results list from this record number
        :param max_results: The maximum number of results to return
        :param missing_build: Requires no value. If this parameter is included in the query string,
                            results will only include tests with no assigned build
        :param query: Limit results to only those with this test name
        :param desc: Set to true to sort results in descending order by creation time. Default value is false
        :param error: Limit results to only those that threw this error message
        :return:
        """
        start, end = get_datetime_for_insights(start, end)
        params = get_dict_from_locals(locals())

        return self._valid(self._session.request('get', f'{self.__sub_host}/tests', params=params), Insight, 'items')

    def get_summary_of_test_metric(self, start: datetime, end: datetime, scope=None, owner=None, status=None,
                                   query=None, os=None, browser=None):
        """
        https://docs.saucelabs.com/dev/api/insights/#get-summary-of-test-metrics

        Returns an aggregate of metric values for runs of a specified test during the specified time period
        :param start: The starting date of the period during which the test runs executed, in YYY-MM-DDTHH:MM:SSZ
                            or Unix time format.
        :param end: The ending date of the period during which the test runs executed, in YYY-MM-DDTHH:MM:SSZ
                            or Unix time format.
        :param scope: Specifies the scope of the owner parameter
        :param owner: The name of one or more users in the requestor's organization who executed the requested tests.
                            This parameter is required if the scope parameter is set to single.
        :param status: Limit results to only those with a specified status
        :param query: The name of the test for which results are requested
        :param os: Limit results to only those run on the specified operating systems
        :param browser: Limit results to only those run on the specified browsers
        :return:
        """
        start, end = get_datetime_for_insights(start, end)
        params = get_dict_from_locals(locals())

        return self._session.request('get', f'{self.__sub_host}/insights/test-metrics', params=params)

    def get_test_trends(self, start: datetime, end: datetime, interval: str, scope=None, owner=None, status=None,
                        os=None, browser=None):
        """
        https://docs.saucelabs.com/dev/api/insights/#get-test-trends

        Returns a set of data "buckets" representing tests that were run in each time interval defined
        by the request parameters
        :param start: The starting date of the period during which the test runs executed, in YYY-MM-DDTHH:MM:SSZ
                            or Unix time format.
        :param end: The ending date of the period during which the test runs executed, in YYY-MM-DDTHH:MM:SSZ
                            or Unix time format.
        :param interval: The amount of time representing the boundary of each data bucket
        :param scope: Specifies the scope of the owner parameter
        :param owner: The name of one or more users in the requestor's organization who executed the requested tests.
                            This parameter is required if the scope parameter is set to single.
        :param status: Limit results to only those with a specified status
        :param os: Limit results to only those run on the specified operating systems
        :param browser: Limit results to only those run on the specified browsers
        :return:
        """
        start, end = get_datetime_for_insights(start, end)
        params = get_dict_from_locals(locals())

        return self._session.request('get', f'{self.__sub_host}/trends/tests', params=params)

    def get_builds_and_tests(self, start: datetime, end: datetime, scope=None, owner=None, status=None, os=None,
                             browser=None):
        """
        https://docs.saucelabs.com/dev/api/insights/#get-builds-and-tests

        Returns the set of all tests run within the specified time period, grouped by whether
        each test was part of a build or not
        :param start: The starting date of the period during which the test runs executed, in YYY-MM-DDTHH:MM:SSZ
                            or Unix time format.
        :param end: The ending date of the period during which the test runs executed, in YYY-MM-DDTHH:MM:SSZ
                            or Unix time format.
        :param scope: Specifies the scope of the owner parameter
        :param owner: The name of one or more users in the requestor's organization who executed the requested tests.
                            This parameter is required if the scope parameter is set to single.
        :param status: Limit results to only those with a specified status
        :param os: Limit results to only those run on the specified operating systems
        :param browser: Limit results to only those run on the specified browsers
        :return:
        """
        start, end = get_datetime_for_insights(start, end)
        params = get_dict_from_locals(locals())

        return self._session.request('get', f'{self.__sub_host}/trends/builds_tests', params=params)

    def get_error_trends(self, start: datetime, end: datetime, scope=None, owner=None, status=None, os=None,
                         browser=None):
        """
        https://docs.saucelabs.com/dev/api/insights/#get-error-trends


        Returns an array of errors that occurred on all tests run within the specified time period.
        :param start: The starting date of the period during which the test runs executed, in YYY-MM-DDTHH:MM:SSZ
                            or Unix time format.
        :param end: The ending date of the period during which the test runs executed, in YYY-MM-DDTHH:MM:SSZ
                            or Unix time format.
        :param scope: Specifies the scope of the owner parameter
        :param owner: The name of one or more users in the requestor's organization who executed the requested tests.
                            This parameter is required if the scope parameter is set to single.
        :param status: Limit results to only those with a specified status
        :param os: Limit results to only those run on the specified operating systems
        :param browser: Limit results to only those run on the specified browsers
        :return:
        """
        start, end = get_datetime_for_insights(start, end)
        params = get_dict_from_locals(locals())

        return self._session.request('get', f'{self.__sub_host}/trends/errors', params=params)
