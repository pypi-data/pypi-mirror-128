from saucelab_api_client.category import Base
from saucelab_api_client.models.performance import Performance, PerformanceJob


class PerformanceApi(Base):
    __sub_host = '/v2/performance/metrics'

    def get_performance_test_results(self, page_url: str = None, metric_names: str = None, start_date: str = None,
                                     end_date: str = None):
        """
        https://docs.saucelabs.com/dev/api/performance/#get-performance-test-results

        Retrieves the results of performance tests run by the requesting account and returns the
        metric values for those tests.
        :param page_url: Filter results to return only tests run on a specific URL
        :param metric_names: Provide a list of specific metric values to return
        :param start_date: Filter results based on tests run on or after this date
        :param end_date: Filter results based on tests run on or before this date
        :return:
        """
        params = {key: value for key, value in locals().items() if value is not None and key != 'self'}
        return self._valid(self._session.request('get', f'{self.__sub_host}/', params=params), Performance, 'items')

    def get_performance_test_results_for_test(self, job_id: str, full: bool = True):
        """
        https://docs.saucelabs.com/performance/one-page/#get-performance-results-for-a-specific-test

        Retrieves the results of a specific performance test run by the requesting account
        :param job_id: The unique identifier of the requested test results
        :param full: Set to false to return only basic job data, excluding metric values. Defaults to true
        :return:
        """
        params = {'full': full}
        return self._valid(self._session.request('get', f'{self.__sub_host}/{job_id}', params=params), PerformanceJob)
