from cloudshell.traffic_generator.ixia.breaking_point.autoload.autoload_elements import Resource


class Chassis(Resource):
    MODEL = 'CHASSIS'
    NAME_TEMPLATE = 'Chassis {}'
    PREFIX = 'CH'

    def __init__(self, resource_id, unique_identifier):
        super(Chassis, self).__init__(resource_id, unique_identifier)

    @property
    def version(self):
        return self._get_attribute('Version')

    @version.setter
    def version(self, value):
        self._add_attribute('Version', value)


class Module(Resource):
    MODEL = 'Module'
    NAME_TEMPLATE = 'Module {}'
    PREFIX = 'M'

    def __init__(self, resource_id, unique_identifier):
        super(Module, self).__init__(resource_id, unique_identifier)


class Port(Resource):
    MODEL = 'Port'
    NAME_TEMPLATE = 'Port {}'
    PREFIX = 'P'

    def __init__(self, resource_id, unique_identifier):
        super(Port, self).__init__(resource_id, unique_identifier)


if __name__ == '__main__':
    ch = Chassis(1, '123')
    ch.version='dsdsdsd34343'
    m = Module(2, '234')
    m.add_parent(ch)
    p1 = Port(-1, '345')
    p2 = Port(2, 'fff')
    p3 = Port(-1, 'gggg')
    p1.add_parent(m)
    p2.add_parent(m)
    p3.add_parent(m)

    print(ch.attributes)
    print(p2.relative_address)
    print(p2.name)
    print(p3.name)
    print(p3.relative_address)
