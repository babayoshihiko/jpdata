<<<<<<< HEAD
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
=======
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
>>>>>>> 938923c19db61fdb69ac69a5c871d6ac7300fbca
        self.manager.run()