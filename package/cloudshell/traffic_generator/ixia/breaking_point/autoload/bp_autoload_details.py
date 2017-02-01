class BPAutoloadDetails(object):
    def __init__(self, root_builder, chassis_builder, modules_builder, ports_builder):
        self._elements = {}

    def build_root(self):
        pass

    def build_chassis(self):
        pass

    def build_modules(self):
        pass

    def build_ports(self):
        pass

    def discover(self):
        self._elements.update(self.build_root())
        self._elements.update(self.build_chassis())
        self._elements.update(self.build_modules())
        self._elements.update(self.build_ports())
