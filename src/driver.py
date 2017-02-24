from cloudshell.networking.devices.driver_helper import get_logger_with_thread_id, get_api
from cloudshell.shell.core.driver_context import AutoLoadDetails, AutoLoadResource
from cloudshell.shell.core.resource_driver_interface import ResourceDriverInterface
from cloudshell.tg.breaking_point.runners.bp_autoload_runner import BPAutoloadRunner


class BreakingPointChassisDriver(ResourceDriverInterface):
    SUPPORTED_OS = 'Breaking Point'

    def __init__(self):
        pass

    def initialize(self, context):
        """
        :type context: cloudshell.shell.core.driver_context.InitCommandContext
        """
        pass

    def cleanup(self):
        pass

    def get_inventory(self, context):
        """ Return device structure with all standard attributes
        :type context: cloudshell.shell.core.driver_context.AutoLoadCommandContext
        :rtype: cloudshell.shell.core.driver_context.AutoLoadDetails
        """

        # logger = get_logger_with_thread_id(context)
        # api = get_api(context)
        # autoload_runner = BPAutoloadRunner(context, logger, api, self.SUPPORTED_OS)
        # return autoload_runner.discover()
        chassis = AutoLoadResource('Breaking Point Chassis', 'Chassis0', 'CH0', 'CH0')
        details = AutoLoadDetails([chassis], [])

        return details
