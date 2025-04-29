from PyQt5 import QtWidgets
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QSize, Qt
from .uilib.window import Dialog
from .uilib.util import shadowify


class CreatePlaylistDialog(Dialog):
    def __init__(self, p):
        super(CreatePlaylistDialog, self).__init__(p)
        self.hlay = QtWidgets.QHBoxLayout()
        self.input_lay = QtWidgets.QVBoxLayout()
        self.cover_button_lay = QtWidgets.QVBoxLayout()

        self.addCoverButton = QtWidgets.QPushButton(self)
        self.addCoverButton.setIcon(QIcon("res/icons/create_playlist_add_cover.svg"))
        self.addCoverButton.setFixedSize(128, 128)
        self.addCoverButton.setIconSize(QSize(32, 32))
        self.addCoverButton.setObjectName("add-cover")

        self.addCoverLabel = QtWidgets.QLabel("Add a cover image\n(optional)")
        self.addCoverLabel.setAlignment(Qt.AlignCenter)

        self.playlistName = QtWidgets.QLineEdit(self)
        self.playlistName.setPlaceholderText("Give this playlist a name")
        self.playlistDesc = QtWidgets.QTextEdit(self)
        self.playlistDesc.setPlaceholderText("Give this playlist a description (optional)")
        shadowify(self.addCoverButton)
        shadowify(self.playlistName)
        shadowify(self.playlistDesc)

        self.input_lay.addWidget(self.playlistName)
        self.input_lay.addSpacing(10)
        self.input_lay.addWidget(self.playlistDesc)
        self.cover_button_lay.addWidget(self.addCoverButton, alignment=Qt.AlignHCenter)
        self.hlay.addLayout(self.cover_button_lay)
        self.hlay.addSpacing(25)
        self.hlay.addLayout(self.input_lay)
        self.mainLayout.addLayout(self.hlay)
        self.dialogButtonLayout.addWidget(self.addCoverLabel, alignment=Qt.AlignLeft)
        self.showDialogButtons()


