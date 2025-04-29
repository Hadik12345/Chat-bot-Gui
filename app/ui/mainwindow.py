from PyQt5 import QtWidgets
from .uilib.window import Window, DialogContainer
from .playerpanel import PlayerPanelLayout
from .sidetab import SideTab, SideTabButton
from .pages import Page, LibraryPage, PlaylistPage, FavouritePage, HistoryPage


class MainWindow(Window):
    def __init__(self, p):
        super(MainWindow, self).__init__(p)
        self.titlebar.windowNotch.setTitle("Jarvis")
        self.vlay = QtWidgets.QVBoxLayout(self)
        self.upper_hlay = QtWidgets.QHBoxLayout()
        self.sideTab = SideTab(self)
        
        self.playerPanelLayout = PlayerPanelLayout()
        self.pageContainer = QtWidgets.QStackedWidget(self)

        self.libraryPage = LibraryPage(self, "Home")
        self.playlistPage = PlaylistPage(self, "Playlist")
        self.favouritePage = FavouritePage(self, "Player")
        self.historyPage = HistoryPage(self, "Alarms & Reminders")


        for page in self.findChildren(Page):
            self.pageContainer.addWidget(page)

        for idx, button in enumerate(self.sideTab.findChildren(SideTabButton)):
            button.setTabIndex(idx)
            button.onClicked.connect(self.pageContainer.setCurrentIndex)

        self.upper_hlay.addWidget(self.sideTab)
        self.upper_hlay.addWidget(self.pageContainer)

        self.vlay.addLayout(self.upper_hlay)
        self.vlay.addLayout(self.playerPanelLayout)
        self.raiseBaseWidget()