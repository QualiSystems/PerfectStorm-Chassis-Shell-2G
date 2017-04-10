from cloudshell.shell.core.resource_driver_interface import ResourceDriverInterface
from cloudshell.tg.breaking_point.helpers.context_utils import get_logger_with_thread_id, get_api
from bp_chassis.runners.bp_autoload_runner import BPAutoloadRunner


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

        logger = get_logger_with_thread_id(context)
        api = get_api(context)
        autoload_runner = BPAutoloadRunner(context, logger, api, self.SUPPORTED_OS)
        return autoload_runner.discover()