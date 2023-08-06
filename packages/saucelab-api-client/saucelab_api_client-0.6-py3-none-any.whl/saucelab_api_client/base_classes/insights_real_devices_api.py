from datetime import datetime

from saucelab_api_client.category import Base
from saucelab_api_client.models.insights import RealDeviceInsight, CsvClass
from saucelab_api_client.models.service import get_dict_from_locals


class InsightsRealDeviceApi(Base):
    __sub_host = '/v2/insights/rdc'

    def get_insights(self, start: datetime, end: datetime, limit: int = 25, offset: int = 0,
                     org_id: str = None, csv: bool = False):
        start, end = int(start.timestamp()), int(end.timestamp())
        if org_id is None:
            org_id = self._session.accounts.account_user.get_active_user().organization.organization_id
        params = get_dict_from_locals(locals())
        params.update({'sort': 'desc', 'sort_by': 'name', 'since': start, 'until': end})
        if csv:
            return CsvClass(self._session.request('get', f'{self.__sub_host}/test-cases/csv', params=params,
                                                  return_type='content'))
        else:
            return self._valid(self._session.request('get', f'{self.__sub_host}/test-cases', params=params),
                               RealDeviceInsight)
