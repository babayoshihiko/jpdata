from .manager import JPDataManager

class jpdata:
    def __init__(self, iface):
        self.iface = iface
        self.manager = JPDataManager(iface)

    def initGui(self):
        self.manager.init_gui()

    def unload(self):
        self.manager.unload()

    def run(self):
        self.manager.run()