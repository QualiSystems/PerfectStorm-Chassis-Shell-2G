from cloudshell.traffic_generator.ixia.breaking_point.rest_actions.auth_actions import AuthActions
from cloudshell.traffic_generator.ixia.breaking_point.rest_api.rest_json_client import RestJsonClient


class RestSession(object):
    def __init__(self, hostname, username, password, logger):
        self._hostname = hostname
        self._username = username
        self._password = password
        self._logger = logger
        self._session = RestJsonClient(self._hostname)
        self._auth_actions = AuthActions(self._session, self._logger)

    def __enter__(self):
        self._auth_actions.login(self._username, self._password)
        return self._session

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._auth_actions.logout()


class RestSessionManager(object):
    def __init__(self, hostname, username, password, logger):
        self._hostname = hostname
        self._username = username
        self._password = password
        self._logger = logger

    def new_session(self):
        return RestSession(self._hostname, self._username, self._password, self._logger)
