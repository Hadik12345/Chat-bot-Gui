from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt, pyqtSignal, QSize, QPoint
from PyQt5.QtGui import QPixmap, QIcon
from .uilib.util import setElide, mask_image_rndcb, shadowify


class SearchBar(QtWidgets.QLineEdit):
    def __init__(self, p):
        super(SearchBar, self).__init__(p)
        self.hlay = QtWidgets.QHBoxLayout(self)
        self.hlay.setContentsMargins(4, 0, 0, 0)
        self.searchButton = QtWidgets.QPushButton(self)
        self.searchButton.setIcon(QIcon("res/icons/search.svg"))
        self.searchButton.setCursor(Qt.PointingHandCursor)
        self.hlay.addWidget(self.searchButton, alignment=Qt.AlignLeft)

class ChatItem_jarvis(QtWidgets.QFrame):
    

    def __init__(self, p, media):
        
        super(ChatItem_jarvis, self).__init__(p)
        # --- Changes Start Here ---
        # Remove fixed/max size constraints
        self.setMinimumHeight(50) # Keep minimum height if desired for spacing
        self.setMinimumWidth(400) # Removed

        # Set size policy to allow growth/shrinkage based on content
        # Preferred policy lets the widget determine its ideal size via sizeHint()
        # Allow vertical expansion for wrapped text
        self.setSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding) # Changed vertical policy
        # Set a maximum width if you still want to prevent it from becoming excessively wide
        # For example, constrain it to the parent's width or a reasonable maximum:
        # self.setMaximumWidth(p.width() - 50) # Example: Constrain to parent width minus some margin
        # Or a fixed large value if preferred over infinite growth:
        self.setMaximumWidth(800) # Keep or adjust as needed
        self.setObjectName("track-item3")
        self.vlay = QtWidgets.QVBoxLayout(self)
        self.vlay.setContentsMargins(10, 10, 10, 10) # Added some margins for better look
        self.vlay.setSpacing(5)

        self.media = media
        message = media
        # Assuming media is the string message

        if message is None:
            pass
        else :
            self.title = QtWidgets.QLabel(self)
            self.title.setObjectName("track-item-title3")
            # --- Enable Word Wrap ---
            self.title.setWordWrap(True)
            # --- Adjust Size Policy for Label ---
            # Let the label expand vertically as needed, but horizontally follow the parent
            self.title.setSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.MinimumExpanding)
            # --- Alignment ---
            # AlignCenter might look odd with multiple lines, consider AlignLeft
            self.title.setAlignment(Qt.AlignLeft | Qt.AlignVCenter) # Changed alignment
            self.vlay.addWidget(self.title) # Removed alignment here, let label handle it
            shadowify(self) # Apply shadow if needed
            self.setTitle(f"<b>{user}:</b> {message}")
             # Or handle this case, e.g., show a placeholder

    def setTitle(self, title):
        self.title.setText(title)
        # Optionally set a tooltip anyway
        self.title.setToolTip(title)

        
        


class ChatItem(QtWidgets.QFrame):
    def __init__(self, p, media):
        super(ChatItem, self).__init__(p)
        self.is_user_message = False # Initialize flag

        # --- Sizing Adjustments ---
        self.setMinimumHeight(50)
        # Preferred horizontal allows shrinking/growing based on content width
        # Expanding vertical allows growing for wrapped text
        self.setSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        # No maximum width set here, allowing it to use available space

        self.vlay = QtWidgets.QVBoxLayout(self)
        self.vlay.setContentsMargins(10, 10, 10, 10)
        self.vlay.setSpacing(5)

        self.media = media
        message = media.get("Message", "") # Use .get for safety
        user = media.get("User", "Unknown") # Use .get and provide default

        # Determine user type early for object names
        if user == "Jarvis":
            self.is_user_message = False
            self.setObjectName("chat-item-assistant")
        else:
            self.is_user_message = True
            self.setObjectName("chat-item-user")

        if not message:
             # Handle empty message - maybe show a placeholder or make frame invisible?
             # For now, let's create an empty label to avoid errors later
             self.title = QtWidgets.QLabel("", self)
             self.vlay.addWidget(self.title)
             # Optionally hide the frame if message is empty: self.setVisible(False)
             return

        self.title = QtWidgets.QLabel(self)
        self.title.setWordWrap(True)

        # --- Change Vertical Size Policy ---
        # Set Preferred horizontally (respects width changes)
        # Set Expanding vertically (takes needed vertical space for wrapped text)
        self.title.setSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding) # Changed vertical policy
        # --- End Change ---

        # Set object names and alignment based on user type
        if self.is_user_message:
            self.title.setObjectName("chat-label-user")
            self.title.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        else: # Assistant message
            self.title.setObjectName("chat-label-assistant")
            self.title.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)

        self.vlay.addWidget(self.title)
        shadowify(self) # Apply shadow if needed
        self.setTitle(f"<b>{user}:</b> {message}")


    def setTitle(self, title):
        # Ensure self.title exists before using it
        if hasattr(self, 'title') and self.title:
            self.title.setText(title)
            self.title.setToolTip(title)




class TrackItem(QtWidgets.QFrame):
    onPlay = pyqtSignal(object)

    def __init__(self, p, media):
        super(TrackItem, self).__init__(p)
        self.setFixedSize(128, 170)
        self.setObjectName("track-item")
        self.vlay = QtWidgets.QVBoxLayout(self)
        self.vlay.setContentsMargins(0, 0, 0, 0)
        self.vlay.setSpacing(0)

        self.media = media

        title = media.title
        artist = media.artist
        cover = media.art

        self.searchid = (str(title) if title else "") + (str(artist) if artist else "")
        self.searchid = self.searchid.lower() if self.searchid else ""
        self.searchid = self.searchid.lower()

        if cover is None:
            cover = "res/icons/cd.png"
        self.cover = QtWidgets.QLabel(self)
        self.cover.setFixedSize(128, 128)
        self.cover.setPixmap(mask_image_rndcb(cover, size=128, radius=8))

        self.title = QtWidgets.QLabel(self)
        self.title.setObjectName("track-item-title")
        self.title.resize(150, self.title.height())
        self.artist = QtWidgets.QLabel(self)
        self.artist.setObjectName("track-item-artist")
        self.title.resize(150, self.artist.height())
        self.setTitle(title)
        self.setArtist(artist)

        self.vlay.addWidget(self.cover, alignment=Qt.AlignCenter | Qt.AlignTop)
        self.vlay.addWidget(self.title, alignment=Qt.AlignCenter)
        self.vlay.addSpacing(-10)
        self.vlay.addWidget(self.artist, alignment=Qt.AlignCenter)

        shadowify(self)

    def mouseDoubleClickEvent(self, a0) -> None:
        self.onPlay.emit(self.media)
        QtWidgets.QFrame.mouseDoubleClickEvent(self, a0)

    def setCover(self, imgpath):
        self.cover.setPixmap(mask_image_rndcb(imgpath, size=128, radius=8))

    def setTitle(self, title):
        setElide(self.title, title)
        if "…" in self.title.text():
            self.title.setToolTip(title)

    def setArtist(self, artist):
        setElide(self.artist, artist)
        if "…" in self.artist.text():
            self.artist.setToolTip(artist)


class PlaylistItem(QtWidgets.QFrame):
    def __init__(self, p, title, date, desc="", count="--", duration="--:--"):
        super(PlaylistItem, self).__init__(p)
        self.setFixedSize(250, 128)
        self.setObjectName("playlist-item")
        self.hlay = QtWidgets.QHBoxLayout(self)
        self.hlay.setContentsMargins(0, 0, 0, 0)
        self.vlay = QtWidgets.QVBoxLayout()
        self.vlay.setAlignment(Qt.AlignTop)
        self.vlay.setContentsMargins(0, 8, 0, 0)

        self.cover = QtWidgets.QLabel(self)
        self.cover.setFixedSize(128, 128)
        self.cover.setPixmap(mask_image_rndcb("res/icons/cd.png", 128, 8))

        self.title = QtWidgets.QLabel(title, self)
        self.title.setObjectName("playlist-title")

        self.date = QtWidgets.QLabel(date, self)
        self.date.setObjectName("playlist-properties-label")

        self.count = QtWidgets.QLabel(count, self)
        self.count.setObjectName("playlist-properties-label")

        self.duration = QtWidgets.QLabel(duration, self)
        self.duration.setObjectName("playlist-properties-label")

        self.vlay.addWidget(self.title)
        self.vlay.addWidget(self.date)
        self.vlay.addWidget(self.count)
        self.vlay.addWidget(self.duration)

        self.hlay.addWidget(self.cover)
        self.hlay.addSpacing(8)
        self.hlay.addLayout(self.vlay)

        self.setToolTip(desc)
        shadowify(self)

    def setCover(self, imgpath):
        self.cover.setPixmap(mask_image_rndcb(imgpath, size=128, radius=8))

    def setTitle(self, title):
        setElide(self.title, title)

    def setCount(self, count):
        setElide(self.count, f"{count} tracks")

    def setDuration(self, duration):
        setElide(self.duration, f"{duration} long")


class ControlButton(QtWidgets.QPushButton):
    def __init__(self, iconSize=16, *args, **kwargs):
        super(ControlButton, self).__init__(*args, **kwargs)
        self.iconSize = iconSize
        self.setIconSize(QSize(iconSize, iconSize))

    def changeIcon(self, newIconPath):
        self.setIcon(QIcon(newIconPath))
        self.setIconSize(QSize(self.iconSize, self.iconSize))


class PlaybackModeControlButton(ControlButton):
    onStateChanged = pyqtSignal(int)

    """
    normal = 0
    repeatTrack = 1
    shuffle = 2
    repeatPlaylist = 3
    """

    def __init__(self, *args, **kwargs):
        super(PlaybackModeControlButton, self).__init__(*args, **kwargs)
        self.current_state = 0
        self.clicked.connect(self.change_state)

    def set_state(self, state: int):
        self.current_state = state
        self.update_icon()
        self.onStateChanged.emit(self.current_state)

    def change_state(self):
        if self.current_state < 3:
            self.current_state += 1
        else:
            self.current_state = 0
        self.update_icon()
        self.onStateChanged.emit(self.current_state)

    def update_icon(self):
        if self.current_state == 0:
            self.changeIcon("res/icons/repeatoff.svg")
            self.setToolTip("Repeat off")
        elif self.current_state == 1:
            self.changeIcon("res/icons/repeatone.svg")
            self.setToolTip("Repeat this track")
        elif self.current_state == 2:
            self.changeIcon("res/icons/shuffle.svg")
            self.setToolTip("Shuffle")
        else:
            self.changeIcon("res/icons/repeat")
            self.setToolTip("Repeat on")


class Seekbar(QtWidgets.QSlider):
    seek = pyqtSignal(int)

    def __init__(self, *args, **kwargs):
        super(Seekbar, self).__init__(*args, **kwargs)
        self.seeking = False
        self.valueChanged.connect(self.on_seek)

    def on_seek(self, value):
        if self.seeking:
            self.seek.emit(value)

    def updatePosition(self, position):
        if not self.seeking:
            self.setValue(position)

    def mousePressEvent(self, ev) -> None:
        self.seeking = True
        QtWidgets.QSlider.mousePressEvent(self, ev)

    def mouseReleaseEvent(self, ev) -> None:
        self.seeking = False
        QtWidgets.QSlider.mouseReleaseEvent(self, ev)


class ToolTip(QtWidgets.QFrame):
    def __init__(self, p, text="Placeholder"):
        super(ToolTip, self).__init__(p)
        self.text = QtWidgets.QLabel(self)
        self.text.setAlignment(Qt.AlignCenter)
        self.setWindowFlags(Qt.ToolTip)
        self.setText(text)

    def setText(self, text):
        self.text.setText(text)
        self.text.adjustSize()
        self.setFixedSize(self.text.size())


class ScrollableButton(ControlButton):
    onValueChanged = pyqtSignal(int)

    def __init__(self, *args, **kwargs):
        super(ScrollableButton, self).__init__(*args, **kwargs)
        self.currentVolume = 50
        self.minr, self.maxr = 0, 100
        self.tooltip = ToolTip(self)

    def setRange(self, minimum, maximum):
        self.minr, self.maxr = minimum, maximum

    def enterEvent(self, a0) -> None:
        self.tooltip.setText(str(self.currentVolume))
        self.tooltip.show()
        self.tooltip.move(self.mapToGlobal(QPoint(self.pos().x() + (self.width() // 2) - (self.tooltip.width() // 2)
                                                  - 5, self.pos().y() - 45)))
        ControlButton.enterEvent(self, a0)

    def leaveEvent(self, a0) -> None:
        self.tooltip.hide()
        ControlButton.leaveEvent(self, a0)

    def wheelEvent(self, event) -> None:
        if event.angleDelta().y() > 0:
            if not (self.currentVolume + 1) > self.maxr:
                self.currentVolume += 1
        else:
            if not (self.currentVolume - 1) < self.minr:
                self.currentVolume -= 1
        self.onValueChanged.emit(self.currentVolume)
        self.tooltip.setText(str(self.currentVolume))
        ControlButton.wheelEvent(self, event)


class DropDownMenu(QtWidgets.QMenu):
    def __init__(self, *args, **kwargs):
        super(DropDownMenu, self).__init__(*args, **kwargs)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Popup | Qt.NoDropShadowWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)


class DropDown(QtWidgets.QPushButton):
    def __init__(self, p):
        super(DropDown, self).__init__(p)
        self.hlay = QtWidgets.QHBoxLayout(self)
        self.icon_ = QtWidgets.QLabel(self)
        self.text_ = QtWidgets.QLabel(self)
        self.hlay.addWidget(self.text_, alignment=Qt.AlignCenter)
        self.hlay.addWidget(self.icon_, alignment=Qt.AlignRight)
        self.menu_ = DropDownMenu(self)
        self.setMenu(self.menu_)

        self.iconPath = None
        self.clicked.connect(self.menu_.exec_)

    def setText(self, text: str) -> None:
        self.text_.setText(text)

    def setIcon(self, icon: str) -> None:
        self.iconPath = icon
        icon = QPixmap(icon)
        icon = icon.scaled(32, 32, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.icon_.setPixmap(icon)

    def setIconSize(self, size: int) -> None:
        icon = QPixmap(self.iconPath)
        icon = icon.scaled(size, size, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.icon_.setPixmap(icon)
