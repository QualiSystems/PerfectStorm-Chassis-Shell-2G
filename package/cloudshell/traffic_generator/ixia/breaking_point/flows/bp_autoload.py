from cloudshell.traffic_generator.ixia.breaking_point.rest_actions.status_actions import StatusActions
from cloudshell.traffic_generator.ixia.breaking_point.rest_api.rest_session_manager import RestSessionManager


class BPAutoload(object):
    def __init__(self, session_manager, logger):
        """
        :param session_manager:
        :type session_manager: RestSessionManager
        :param logger:
        :return:
        """
        self._session_manager = session_manager
        self._logger = logger

    def do_autoload(self):
        with self._session_manager.new_session() as session:
            status_actions = StatusActions(session, self._logger)
            blade = status_actions.get_chassis_info()
            ports = status_actions.get_ports_info()
            return ''
