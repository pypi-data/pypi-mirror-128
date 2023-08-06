class Insight:
    def __init__(self, data: dict):
        if data is not None:
            self.insight_id: str = data.get('id')
            self.owner: str = data.get('owner')
            self.ancestor: str = data.get('ancestor')
            self.name: str = data.get('name')
            self.build: str = data.get('build')
            self.creation_time: str = data.get('creation_time')
            self.start_time: str = data.get('start_time')
            self.end_time: str = data.get('end_time')
            self.duration: int = data.get('duration')
            self.status: str = data.get('status')
            self.error: str = data.get('error')
            self.os: str = data.get('os')
            self.os_normalized: str = data.get('os_normalized')
            self.browser: str = data.get('browser')
            self.browser_normalized: str = data.get('browser_normalized')
            self.details_url: str = data.get('details_url')

    def __str__(self):
        return self.name


class RealDeviceInsight:
    def __init__(self, data: dict):
        if data is not None:
            if isinstance(data.get('test_cases'), (list, tuple)):
                self.test_cases: list[TestCase] = [TestCase(test_case) for test_case in data['test_cases']]
            else:
                self.test_cases = []
            self.total: int = data.get('total')
            self.statuses: TestCasesStatuses = TestCasesStatuses(data.get('statuses'))
            self.avg_runtime: int = data.get('avg_runtime')

    def filter_by_complete_rate(self, reverse: bool = False):
        return sorted(self.test_cases, key=lambda x: x.complete_rate, reverse=reverse)

    def filter_by_pass_rate(self, reverse: bool = False):
        return sorted(self.test_cases, key=lambda x: x.pass_rate, reverse=reverse)


class TestCase:
    def __init__(self, data: dict):
        if data is not None:
            self.name: str = data.get('name')
            self.statuses: TestCasesStatuses = TestCasesStatuses(data.get('statuses'))
            self.total_runs: int = data.get('total_runs')
            self.complete_rate: float = data.get('complete_rate')
            self.error_rate: float = data.get('error_rate')
            self.fail_rate: float = data.get('fail_rate')
            self.pass_rate: float = data.get('pass_rate')
            self.avg_duration: float = data.get('avg_duration')
            self.median_duration: float = data.get('median_duration')
            self.total_duration: int = data.get('total_duration')

    def __str__(self):
        return self.name


class TestCasesStatuses:
    def __init__(self, data: dict):
        if data is not None:
            self.complete: int = data.get('complete', 0)
            self.passed: int = data.get('passed', 0)
            self.failed: int = data.get('failed', 0)


class CsvClass:
    def __init__(self, csv_content: bytes):
        data = csv_content.decode('utf-8').split('\r\n')
        self.results = [CsvResult(row) for row in data[1:] if row != '']
        self.tests_number = len(self.results)

    def filter_by_complete_rate(self, reverse: bool = False):
        return sorted(self.results, key=lambda x: x.complete_rate, reverse=reverse)

    def filter_by_pass_rate(self, reverse: bool = False):
        return sorted(self.results, key=lambda x: x.pass_rate, reverse=reverse)


class CsvResult:
    def __init__(self, csv_row: str):
        if '"' in csv_row:
            name_split = csv_row.split('"')
            name = name_split[1]
            name_split.remove(name)
            data = ''.join(name_split).split(',')
            data[1] = name
        else:
            data = csv_row.split(',')
        for index, value in enumerate(data):
            if value.isnumeric():
                data[index] = int(value)
        self.row_id, self.name, self.total_runs, self.total_duration, self.avg_duration, self.median_duration, \
        self.pass_rate, self.fail_rate, self.error_rate, self.complete_rate, self.status_passed, \
        self.status_failed, self.status_error, self.status_complete = data

    def __str__(self):
        return self.name
