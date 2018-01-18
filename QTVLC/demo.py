from PyQt5.QtWidgets import QDockWidget, QMainWindow, QApplication, QWidget, QLabel,QFrame
from PyQt5.QtCore import Qt
from PyQt5 import QtWidgets
import vlc
import sys

# The Path to the movie to Play
MOVIE_PATH = "/Absolute/Path/To/Your/Movie/test.mp4"

class MainWindow(QMainWindow):
    def __init__(self, instance, media_player):
        super(MainWindow, self).__init__(None)

        self.player = VLCPlayer(self, instance, media_player)
        self.setCentralWidget(self.player)

        self.dock_a = SomeDockWidget(self, "Dock A")
        self.dock_b = SomeDockWidget(self, "Dock B")
        self.addDockWidget(Qt.LeftDockWidgetArea, self.dock_a)
        self.addDockWidget(Qt.RightDockWidgetArea, self.dock_b)
        self.show()


class SomeDockWidget(QDockWidget):
    def __init__(self, parent, text):
        super(SomeDockWidget, self).__init__(parent)
        self.setWidget(QLabel(text))
        self.show()


class VLCPlayer(QWidget):
    def __init__(self, parent, instance, media_player):
        super(VLCPlayer, self).__init__(parent)
        self.videoframe = None
        self.instance = instance
        self.media_player = media_player

        self.init_ui()

    def init_ui(self):
        """
        Attaching the VLC window to a platform specific container.
        :return:
        """
        if sys.platform == "darwin":  # for MacOS
            self.mac_frame = QFrame()
            self.videoframe = QtWidgets.QMacCocoaViewContainer(0, self)

        else:
            self.videoframe = QFrame()

        if sys.platform.startswith('linux'):  # for Linux using the X Server
            self.media_player.set_xwindow(self.videoframe.winId())

        elif sys.platform == "win32":  # for Windows
            self.media_player.set_hwnd(self.videoframe.winId())

        elif sys.platform == "darwin":  # for MacOS
            self.media_player.set_nsobject(int(self.mac_frame.winId()))
            self.videoframe.setCocoaView(self.media_player.get_nsobject())

        self.vboxlayout = QtWidgets.QVBoxLayout()
        self.vboxlayout.addWidget(self.videoframe)
        self.setLayout(self.vboxlayout)

    def open_movie(self, path):
        self.media = self.instance.media_new(path)
        self.media_player.set_media(self.media)
        self.media.parse()
        self.media_player.play()


if __name__ == '__main__':
    vlc_instance = vlc.Instance()
    vlc_media_player = vlc_instance.media_player_new()

    app = QApplication(sys.argv)
    main = MainWindow(vlc_instance, vlc_media_player)
    main.show()

    main.player.open_movie(MOVIE_PATH)
    sys.exit(app.exec_())