import sys
import json
import os
try:

    import requests
    import yaml

except ImportError:

    sys.exit('Unable to import some modules')


class ToledoApi:

    def __init__(self, session: requests.Session) -> None:

        try:

            with open(os.path.join(os.path.dirname(__file__), 'config.yaml'), 'r') as f:
                parser = yaml.safe_load(f)

        except FileNotFoundError:

            sys.exit('Unable to find find config.yaml')

        self._UPCOMING_URL = parser['API']['UpcomingEndpoint']
        self._ENROLLMENTS_URL = parser['API']['EnrollmentsEndpoint']
        self._EVENTS_URL = parser['API']['EventsEndpoint']
        self._TODO_URL = parser['API']['TodoEndpoint']

        self._TASK = parser['API_TO_DO']['Task']
        self._TEST = parser['API_TO_DO']['Test']
        self._VARIOUS = parser['API_TO_DO']['Various']

        self._SESSION = session

    def get_events(self, type: str) -> json:

        try:

            r = self._SESSION.get(
                url=self._EVENTS_URL
            )

            r.raise_for_status()

            events = json.loads(r.text)

            if type == 'message':

                return [event for event in events if event['eventType'] == 'message']
            elif type == 'update':

                return [event for event in events if event['eventType'] == 'update']
            else:

                raise Exception('Unsupported event type!')

        except Exception as ex:

            sys.exit(f'EVENTS: {ex}')

    def get_enrollments(self) -> json:

        try:

            r = self._SESSION.get(
                url=self._ENROLLMENTS_URL
            )

            r.raise_for_status()

            return json.loads(r.text)

        except Exception as ex:

            sys.exit(f'ENROLLMENTS: {ex}')

    def get_upcoming(self) -> json:

        try:

            r = self._SESSION.get(
                url=self._UPCOMING_URL
            )

            r.raise_for_status()

            return json.loads(r.text)

        except Exception as ex:

            sys.exit(f'UPCOMING: {ex}')

    def get_to_do(self, type: str) -> json:

        try:

            r = self._SESSION.get(
                url=self._TODO_URL
            )

            r.raise_for_status()

            todolist = json.loads(r.text)

            if type == 'task':

                contenttype = self._TASK

            elif type == 'test':

                contenttype = self._TEST

            else:

                raise Exception('Unsupported todo type!')

            return [item for item in todolist if item['contentInfo']['contentType'] == contenttype]

        except Exception as ex:

            sys.exit(f'TODO: {ex}')


def create_api_object(session: requests.Session):

    return ToledoApi(
        session=session
    )
    