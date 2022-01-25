# TV Show Renamer Program
# Author: Thomas Alex
# License: For personal use only

import os
import requests
import bs4
import re
import csv
import sys
import json
import logging
import qdarkstyle
import webbrowser
from PyQt5.QtWidgets import *
from main_ui import Ui_MainWindow
from PyQt5 import QtCore, QtGui, QtWidgets

logging.basicConfig(filename="logs.log", level=logging.INFO)

QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True) #enable highdpi scaling
QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True) #use highdpi icons

class MainUI(Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.app = QtWidgets.QApplication(sys.argv)
        self.lightTheme = qdarkstyle.load_stylesheet(palette=qdarkstyle.LightPalette)
        self.DarkTheme = qdarkstyle.load_stylesheet(palette=qdarkstyle.DarkPalette)
        self.applyUserTheme()
        self.MainWindow = QtWidgets.QMainWindow()
        self.ui = Ui_MainWindow()
        self.MainWindow.setWindowIcon(QtGui.QIcon('logo.png'))
        self.setupUi(self.MainWindow)
        
        self.directory_textedit.setPlainText(self.getPreviousDirectory())

        self.browse_btn.clicked.connect(self.SelectDirectory)
        self.renameShows_btn.clicked.connect(self.executeRenamer)
        self.show_comboBox.addItems(self.retrieveShowList())
        self.show_comboBox.setCurrentText(self.getPreviousShow())

        # Menu bar Items
        self.actionAbout.triggered.connect(self.aboutPage)
        self.actionClose.triggered.connect(self.closeApplication)
        self.actionLight_theme.triggered.connect(self.enableLightTheme)
        self.actionDark_theme.triggered.connect(self.enableDarkTheme)
        self.actionClassic_theme.triggered.connect(self.enableClassicTheme)


    def aboutPage(self):
        webbrowser.open_new_tab("https://github.com/Thomasalex2/tv-show-renamer")


    def closeApplication(self):
        sys.exit()

    
    def enableLightTheme(self):
        self.app.setStyleSheet(self.lightTheme)
        self.setUserTheme(self.lightTheme)


    def enableDarkTheme(self):
        self.app.setStyleSheet(self.DarkTheme)
        self.setUserTheme(self.DarkTheme)


    def enableClassicTheme(self):
        self.app.setStyleSheet("")
        self.setUserTheme("")


    def setUserTheme(self, theme):
        if theme == self.lightTheme:
            self.setUserPreferences("theme-settings", "light")
        elif theme == self.DarkTheme:
            self.setUserPreferences("theme-settings", "dark")
        else:
            self.setUserPreferences("theme-settings", "")


    def applyUserTheme(self):
        if self.getUserPreferences("theme-settings") != "":
            theme = self.getUserPreferences("theme-settings")
            if theme == "light":
                self.enableLightTheme()
            elif theme == "dark":
                self.enableDarkTheme()
            else:
                self.enableClassicTheme()


    def setPreviousDirectory(self, folderPath):
        self.setUserPreferences("previous-directory", folderPath)


    def getPreviousDirectory(self):
        return self.getUserPreferences("previous-directory")


    def setPreviousShow(self, show):
        self.setUserPreferences("previous-show", show)


    def getPreviousShow(self):
        return self.getUserPreferences("previous-show")


    def setUserPreferences(self, settingCategory, settings):
        with open("settings.json", "r") as f:
            data = json.load(f)
        with open("settings.json", "w") as f:
            data[settingCategory] = settings
            newSettings = json.dumps(data)
            f.write(newSettings)


    def getUserPreferences(self, setting):
        if os.path.isfile("settings.json"):
            with open("settings.json", "r") as f:
                data = json.load(f)
                try:
                    preferred_setting = data[setting]
                    return preferred_setting
                except KeyError:
                    with open("settings.json", "w") as f: 
                        f.write(json.dumps({setting: ""}))
                    return ""
        else:
            with open("settings.json", "w") as f: 
                f.write(json.dumps({"theme-settings": "", "previous-directory": "", "previous-show": ""}))
            return ""



    def show(self):
        self.MainWindow.show()
        sys.exit(self.app.exec_())


    def alertMessageBox(self, title, body):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Warning)
        msg.setWindowTitle("Alert")
        msg.setText(title)
        msg.setText(body)
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec_()


    def infoMessageBox(self, title, body):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setWindowTitle("Done")
        msg.setText(title)
        msg.setText(body)
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec_()

    def confirmationMessageBox(self, body):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Question)
        msg.setWindowTitle("Confirm Rename")
        msg.setText(body)
        msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        msg.buttonClicked.connect(self.msgButtonClick)
        self.returnValue = msg.exec_()


    def msgButtonClick(self, i):
        logging.info("Button clicked is:" + str(i.text()))


    def retrieveShowList(self):
        try:
            reader = csv.reader(open('TV Show Database.csv'))
        except FileNotFoundError:
            self.alertMessageBox("CSV file Not found", "Database file not found. Please add it to the same directory")
            logging.info("Database file not found. Please add it to the same directory")
            exit()
        self.ShowDB = {}
        for row in reader:
            key = row[0]
            self.ShowDB[key] = row[1:]
        show_names = (tuple(self.ShowDB.keys()))
        return list(show_names)


    def SelectDirectory(self):
        folderPath = QtWidgets.QFileDialog.getExistingDirectory(None, 'Select Directory', self.getPreviousDirectory())
        self.directory_textedit.setPlainText(folderPath)
        logging.info(f"Selected folder path: {folderPath}")
        self.setPreviousDirectory(folderPath)


    def executeRenamer(self):
        if self.directory_textedit.toPlainText() == "":
            self.alertMessageBox("Invalid Entry", "Directory is not entered")
            return
        elif os.path.exists(self.directory_textedit.toPlainText()) == False:
            self.alertMessageBox("Invalid Entry", "Directory does not Exist")
            return

        self.required_verification = self.confirmation_checkBox.isChecked()
        logging.info("Confirmation Required: " + str(self.required_verification))
        logging.info("Entered Renamer Function")
        self.RetrievefromInternet()


    def checkCorrectShow(self, old_name, show_name):
        formatted_old_name = "".join(ch for ch in old_name if ch.isalnum()).lower()
        formatted_new_name = "".join(ch for ch in show_name if ch.isalnum()).lower()
        if formatted_new_name in formatted_old_name:
            logging.info("Show chosen seems correct")
            return True
        else:
            logging.info("Show chosen seems wrong. Verification is required")
            return False


    def RetrievefromInternet(self):

        logging.info(f"Chosen Directory: {self.directory_textedit.toPlainText()}")
        logging.info(f"Selected Show: {self.show_comboBox.currentText()}")
        logging.info(f"Fetching Link: {self.ShowDB[self.show_comboBox.currentText()][0]}")

        dest_directory = self.directory_textedit.toPlainText()
        name_of_series = self.show_comboBox.currentText()
        download_page = self.ShowDB[self.show_comboBox.currentText()][0]

        self.setPreviousShow(name_of_series)

        all_episode_titles = []
        try:
            res = requests.get(download_page)
            res.raise_for_status()
        except Exception:
            self.alertMessageBox("Unable to retrieve URL", "Unable to access the database URL. Please check the Internet connection")
            return

        soup = bs4.BeautifulSoup(res.text, "html.parser")

        # HTML Attributes

        episode_list = soup.select('tbody .vevent')
        for episode in episode_list:
            episode_no = episode.find('td').getText()
            episode_name = episode.find('td', attrs={'class': 'summary'}).getText()
            all_episode_titles.append([episode_no, episode_name.strip('"')])

            # Uncomment below to check if retrieval from wiki page is correct and functioning
            # logging.info(formatted_name,'\n')

        logging.info('\n')
        old_names_list = os.listdir(dest_directory)
        no_of_operations = len(old_names_list)
        no_of_operations_done = 0
        pattern = re.compile(r'\bS(\d\d)(|.)E(\d\d)\b', re.IGNORECASE)

        for old_name in old_names_list:

            extract = pattern.search(old_name)

            if extract == None:
                logging.info("Filenames are not in the expected format\n")
                self.alertMessageBox("Incorrect File Names", "Filenames are not in the expected format")
                return

            season = extract.group(1)
            identifier = extract.group(3)
            episode_detected = False
            current_season = 0

            for episode in all_episode_titles:
                if int(episode[0]) == 1:
                    current_season += 1
                if current_season == int(season):
                    if int(episode[0]) == int(identifier):
                        episode_title = episode[1]
                        episode_detected = True
                        break
                    
            if episode_detected == False:
                self.alertMessageBox("Episode not found", f"Unable to fetch episode name for\n{old_name}")
                continue

            episode_title = "".join(ch for ch in episode_title if ch not in '<>:"\/|?*')
            file_format = old_name.split('.')[-1]

            new_name = name_of_series + \
                f' - S{season}E{identifier} - {episode_title}.{file_format}'
            logging.info(f'{old_name}\n --> {new_name}')

            filename_verified = self.checkCorrectShow(old_name, name_of_series)

            if self.required_verification == True or filename_verified == False:
                self.confirmationMessageBox(f'{old_name}\n--> {new_name}')
                if self.returnValue == QMessageBox.Ok:
                    verification = 'Y'
                elif self.returnValue == QMessageBox.Cancel:
                    verification = 'N'
            elif filename_verified == True:
                verification = 'Y'

            if verification.upper() == 'Y':
                old_path = os.path.join(dest_directory, old_name)
                new_path = os.path.join(dest_directory, new_name)
                os.rename(old_path, new_path)
                no_of_operations_done += 1
                logging.info('Successfully Renamed\n')

        if no_of_operations == no_of_operations_done:
            logging.info("All Files renamed successfully\n\n")
            self.infoMessageBox("Successful", "All Files renamed successfully")
        else:
            logging.info(f"{(no_of_operations - no_of_operations_done)} file(s) were not renamed")
            self.infoMessageBox(
                "Notice", f"{(no_of_operations - no_of_operations_done)} file(s) were not renamed\n{no_of_operations_done} were renamed successfully")

# ====================================MAIN=============================================

def main():
    app = MainUI()
    app.show()

if __name__ == "__main__":
    main()
