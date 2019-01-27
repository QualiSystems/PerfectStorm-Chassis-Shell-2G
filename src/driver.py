
from cloudshell.shell.core.driver_context import AutoLoadAttribute
from cloudshell.shell.core.resource_driver_interface import ResourceDriverInterface
from cloudshell.tg.breaking_point.helpers.context_utils import get_api

from cloudshell.traffic import tg_helper

from bp_chassis.runners.bp_autoload_runner import BPAutoloadRunner


class PerfectStormChassisDriver(ResourceDriverInterface):
    SUPPORTED_OS = 'Breaking Point'

    def __init__(self):
        pass

    def initialize(self, context):
        """
        :type context: cloudshell.shell.core.driver_context.InitCommandContext
        """
        self.logger = tg_helper.get_logger(context)
        self.autoload_runner = BPAutoloadRunner(context, self.logger, get_api(context), self.SUPPORTED_OS)

    def cleanup(self):
        pass

    def get_inventory(self, context):
        """ Return device structure with all standard attributes
        :type context: cloudshell.shell.core.driver_context.AutoLoadCommandContext
        :rtype: cloudshell.shell.core.driver_context.AutoLoadDetails
        """

        auto_load_details = self.autoload_runner.discover()

        address = context.resource.address
        user = context.resource.attributes['PerfectStorm Chassis Shell 2G.User']
        encripted_password = context.resource.attributes['PerfectStorm Chassis Shell 2G.Password']
        password = get_api(context).DecryptPassword(encripted_password).Value
        import paramiko
        self.ssh = paramiko.SSHClient()
        self.ssh.load_system_host_keys()
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.ssh.connect(hostname=address, username=user, password=password)
        self.chan = self.ssh.invoke_shell()
        self.ssh_call('bpsh')
        self.ssh_call('set chassis [$bps getChassis]')
        modules = {}
        for resource in auto_load_details.resources:
            if resource.model == 'PerfectStorm Chassis Shell 2G.GenericTrafficGeneratorModule':
                relative_address = resource.relative_address
                modules[relative_address] = self.ssh_call('$chassis getCardMode ' + relative_address[1:]).split()[0]
        for resource in auto_load_details.resources:
            if resource.model == 'PerfectStorm Chassis Shell 2G.GenericTrafficGeneratorPort':
                port_module = resource.relative_address.split('/')[0]
                if port_module in modules.keys():
                    auto_load_details.attributes.append(AutoLoadAttribute(
                        relative_address=resource.relative_address,
                        attribute_name='CS_TrafficGeneratorPort.Configured Controllers',
                        attribute_value=modules[port_module]))
        return auto_load_details

    def ssh_call(self, string, *args):
        command = '{}\n'.format(string % args)
        self.logger.debug('sending %s', command.rstrip())
        command_len = self.chan.send(command)
        resp = ''
        while not resp.endswith('% '):
            resp += self.chan.recv(9999)
        ret_value = str(resp[command_len:-3].decode("utf-8").strip())
        self.logger.debug('received %s', ret_value)
        return ret_value
