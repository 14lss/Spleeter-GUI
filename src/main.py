import sys
import os.path
import subprocess
from PyQt6.QtCore import QSize, Qt
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QFileDialog, QWidget, QErrorMessage, QFrame, QLabel

class MainWindow(QMainWindow):
    def __init__(self):
        # Setup
        super().__init__()
        self.setWindowTitle("Spleeter")
        self.setFixedSize(QSize(382, 492))
        # Variables
        self.settings_file = None
        self.filename = ["Click to browse", 0]
        self.stems = 2
        self.initUI()
        self.load_settings()
    
    def initUI(self):
        # Main Stylesheet
        self.setStyleSheet("background-color: rgb(255, 255, 255);\nfont: 8pt \"Inter\";")

        # Tab Area
        self.tabArea = QFrame(self)
        self.tabArea.setGeometry(92, 16, 197, 36)
        self.tabArea.setFrameShape(QFrame.Shape.Box)
        self.tabArea.setFrameShadow(QFrame.Shadow.Raised)
        # Buttons
        self.upload_tab = QPushButton("Upload", self.tabArea)
        self.upload_tab.setGeometry(5, 4, 105, 28)
        self.upload_tab.setStyleSheet("background-color: rgb(0, 0, 0);\ncolor: rgb(255, 255, 255);")
        self.upload_tab.clicked.connect(self.close_settings)
        self.settings_tab = QPushButton("Settings", self.tabArea)
        self.settings_tab.setGeometry(114, 4, 78, 28)
        self.settings_tab.clicked.connect(self.open_settings)

        #---Main Area---#
        self.mainArea = QWidget(self)
        self.mainArea.setGeometry(0, 68, 382, 424)
        self.mainArea.setStyleSheet("background-color: rgb(247, 249, 251);")
        # Buttons
        self.split_button = QPushButton("Split Audio", self.mainArea)
        self.split_button.clicked.connect(self.split_audio)
        self.split_button.setGeometry(105, 374, 172, 30)
        self.split_button.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.file_button = QPushButton("Click to browse", self.mainArea)
        self.file_button.clicked.connect(self.get_file_path)
        self.file_button.setGeometry(32, 32, 318, 260)
        self.file_button.setStyleSheet("background-color: rgb(226, 230, 234);")

        #---Settings---#
        # Main Area
        self.settingsArea = QWidget(self)
        self.settingsArea.setGeometry(0, 68, 382, 424)
        self.settingsArea.setStyleSheet("background-color: rgb(247, 249, 251);")
        # Labels
        self.two_stems_label = QLabel("2 Stems (Vocals and accompaniment)", self.settingsArea)
        self.two_stems_label.setGeometry(0, 0, 382, 104)
        self.four_stems_label = QLabel("4 Stems (Vocals / drums / bass / other)", self.settingsArea)
        self.four_stems_label.setGeometry(0, 104, 382, 104)
        self.five_stems_label = QLabel("5 Stems (Vocals / drums / bass / piano / other))", self.settingsArea)
        self.five_stems_label.setGeometry(0, 208, 382, 104)
        # Buttons
        self.two_stems_button = QPushButton("Select",self.settingsArea)
        self.two_stems_button.setGeometry(290, 41, 75, 22)
        self.two_stems_button.clicked.connect(lambda: self.set_stems(self.two_stems_button))

        self.four_stems_button = QPushButton("Select",self.settingsArea)
        self.four_stems_button.setGeometry(290, 145, 75, 22)
        self.four_stems_button.clicked.connect(lambda: self.set_stems(self.four_stems_button))

        self.five_stems_button = QPushButton("Select",self.settingsArea)
        self.five_stems_button.setGeometry(290, 249, 75, 22)
        self.five_stems_button.clicked.connect(lambda: self.set_stems(self.five_stems_button))

        self.save_settings_button = QPushButton("Save", self.settingsArea)
        self.save_settings_button.setGeometry(153, 340, 76, 24)
        self.save_settings_button.clicked.connect(self.save_settings)
        # Lines
        self.line = QFrame(self.settingsArea)
        self.line.setFrameShape(QFrame.Shape.StyledPanel)
        self.line.setGeometry(0, 104, 382, 1)
        self.line.setFrameShadow(QFrame.Shadow.Sunken)
        self.line = QFrame(self.settingsArea)
        self.line.setFrameShape(QFrame.Shape.StyledPanel)
        self.line.setGeometry(0, 208, 382, 1)
        self.line = QFrame(self.settingsArea)
        self.line.setFrameShape(QFrame.Shape.StyledPanel)
        self.line.setGeometry(0, 312, 382, 1)
        #---Show GUI---#
        self.mainArea.show()
        self.tabArea.show()
        self.settingsArea.hide()
        self.update_colors()

    def save_settings(self):
        if os.path.isfile("./settings.txt") == False:
            self.settings_file = open("settings.txt","a")
            self.settings_file.write("stems: " + str(self.stems))
            self.settings_file.close()
        else:
            self.settings_file = open("settings.txt", "w")
            self.settings_file.write("stems: " + str(self.stems))
            self.settings_file.close()

    def load_settings(self):
        if os.path.isfile("./settings.txt") == False:
            self.settings_file = open("settings.txt","a")
            self.settings_file.write("stems: 2")
            self.settings_file.close()
        else:
            self.settings_file = open("settings.txt", "r")
            settings = self.settings_file.read()
            self.stems = int(settings[-1])
            self.settings_file.close()
            self.update_colors()

    def open_settings(self):
        self.settings_tab.setStyleSheet("background-color: rgb(0, 0, 0);\ncolor: rgb(255, 255, 255);")
        self.upload_tab.setStyleSheet("")
        self.settingsArea.show()
        self.mainArea.hide()

    def close_settings(self):
        self.upload_tab.setStyleSheet("background-color: rgb(0, 0, 0);\ncolor: rgb(255, 255, 255);")
        self.settings_tab.setStyleSheet("")
        self.settingsArea.hide()
        self.mainArea.show()

    def update_colors(self):
        self.two_stems_button.setStyleSheet("background-color: rgb(255, 22, 64);\ncolor: rgb(255, 255, 255);")
        self.four_stems_button.setStyleSheet("background-color: rgb(255, 22, 64);\ncolor: rgb(255, 255, 255);")
        self.five_stems_button.setStyleSheet("background-color: rgb(255, 22, 64);\ncolor: rgb(255, 255, 255);")
        if self.stems == 2:
            self.two_stems_button.setStyleSheet("background-color: rgb(17, 208, 117);\ncolor: rgb(255, 255, 255);")
        elif self.stems == 4:
            self.four_stems_button.setStyleSheet("background-color: rgb(17, 208, 117);\ncolor: rgb(255, 255, 255);")
        else:
            self.five_stems_button.setStyleSheet("background-color: rgb(17, 208, 117);\ncolor: rgb(255, 255, 255);")
    
    def set_stems(self, button):
        if button == self.two_stems_button:
            self.stems = 2
        elif button == self.four_stems_button:
            self.stems = 4
        else:
            self.stems = 5
        self.update_colors()

    def get_file_path(self):
        filename = QFileDialog.getOpenFileName(filter="Audio Files (*.mp3 *.wav *.aiff *.flac *.m4a *.ogg)")
        if filename[0] == "":
            self.filename = self.filename
        else:
            self.filename = filename
        self.file_button.setText(self.filename[0][self.filename[0].rfind("/") + 1:])

    def split_audio(self):
        if self.filename[0] == "File Name":
            error_dialog = QErrorMessage(self.centralWidget)
            error_dialog.setWindowTitle("Error")
            error_dialog.showMessage("No file has been selected")
        else:
            file = self.filename[0]
            file = file.replace("/","\\\\")
            subprocess.run(["python", "-mspleeter", "separate", "-oaudio_output", "-pspleeter:"+ str(self.stems) +"stems", file])

app = QApplication(sys.argv)
window = MainWindow()
window.show()
# Loop
app.exec()
