from saucelab_api_client.session import Session


class Base:

    def __init__(self, session):
        self._session: Session = session

    @staticmethod
    def _valid(response, return_class, key: str = None):
        if isinstance(response, str):
            return response
        elif key:
            return return_class(response[key]) if isinstance(response[key], dict) else \
                [return_class(elem) for elem in response[key]]
        else:
            return return_class(response) if isinstance(response, dict) else [return_class(elem) for elem in response]
