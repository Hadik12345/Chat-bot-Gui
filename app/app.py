from PyQt5.QtCore import QThreadPool
from .ui.mainwindow import MainWindow


class Application(MainWindow):
    """
    UI-only application shell
    """
    def __init__(self, p):
        super(Application, self).__init__(p)
        self.threadPool = QThreadPool(self)
        self.threadPool.setMaxThreadCount(1000)
        
        # Initialize UI components
        self.setup_ui_connections()

    def setup_ui_connections(self):
        pass
        