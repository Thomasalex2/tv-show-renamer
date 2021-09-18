# TV Show Renamer Program
# Author: Thomas Alex
# License: For personal use only

import os
import requests
import bs4
import re
import csv
import sys
import logging
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
        self.MainWindow = QtWidgets.QMainWindow()
        self.ui = Ui_MainWindow()
        self.MainWindow.setWindowIcon(QtGui.QIcon('logo.png'))
        self.setupUi(self.MainWindow)

        self.browse_btn.clicked.connect(self.SelectDirectory)
        self.renameShows_btn.clicked.connect(self.executeRenamer)
        self.Show_comboBox.addItems(self.retrieveShowList())


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
        self.folderPath = QtWidgets.QFileDialog.getExistingDirectory(None, 'Select Directory', "Downloads")
        logging.info("Selected folder path: " + str(self.folderPath))
        self.directory_textedit.setPlainText(self.folderPath)


    def executeRenamer(self):
        
        if self.episode_text.toPlainText() == "" and self.directory_textedit.toPlainText() == "":
            self.alertMessageBox("No data given", "Please fill in the data before proceeding")
            return
        
        if self.episode_text.toPlainText().isnumeric() == False:
            self.alertMessageBox("Invalid Entry", "Episode number entered was invalid")
            return
        
        if self.directory_textedit.toPlainText() == "":
            self.alertMessageBox("Invalid Entry", "Directory is not entered")
            return
        elif os.path.exists(self.directory_textedit.toPlainText()) == False:
            self.alertMessageBox("Invalid Entry", "Directory does not Exist")
            return
        
        self.required_verification = self.confirmation_checkBox.isChecked()
        logging.info("Confirmation Required: " + str(self.required_verification))

        logging.info("Entered Renamer Function")
        if self.Internet_rdobtn.isChecked():
            self.RetrievefromInternet()
            logging.info("Selected Retrieve from Internet")
        elif self.reformat_rdobtn.isChecked():
            self.ReformatNames()
            logging.info("Entered Reformat Names")
        elif self.reformat2_rdobtn.isChecked():
            self.ReformatNames2()
            logging.info("Entered Reformat Names 2")

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

        logging.info("Chosen Directory: " + str(self.directory_textedit.toPlainText()))
        logging.info("Total Episodes: " + str(self.episode_text.toPlainText()))
        logging.info("Selected Show: " + str(self.Show_comboBox.currentText()))
        logging.info("Fetching Link: " + str(self.ShowDB[self.Show_comboBox.currentText()][0]))

        dest_directory = self.directory_textedit.toPlainText()
        name_of_series = self.Show_comboBox.currentText()
        download_page = self.ShowDB[self.Show_comboBox.currentText()][0]
        total_episodes = int(self.episode_text.toPlainText())

        new_names_list_wiki = []
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
            episode_no = episode.find('th', attrs={'scope': 'row'}).getText()
            episode_name = episode.find('td', attrs={'class': 'summary'}).getText()
            formatted_name = episode_no + '. ' + episode_name[1:-1]
            new_names_list_wiki.append(formatted_name)

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

            for match in new_names_list_wiki:

                dot_index = match.find('.')

                subtract_episodes = total_episodes
                try:
                    val = int(match[:dot_index])
                except ValueError as e:
                    try:
                        val = match[:dot_index]
                        print("Hello2: " + val.split("–")[0])
                        val = int(match[:dot_index].split("–")[0]) # Need to implement fix for the consecutive parts of the episodes
                    except ValueError as e:
                        logging.info(e)
                        logging.info("Combined Episode name Detected. Please manually check")
                        logging.info("Retrieved value: ")
                        logging.info(match)
                        logging.info("Old episode number: " + str(identifier))
                        continue

                if int(identifier) == (val - subtract_episodes):
                    epi_name = match.split(' ', 1)[1]
                    epi_name_mod = ""

                    for ch in epi_name:
                        if ch in '<>:"\/|?*':
                            epi_name_mod = epi_name_mod + ""
                        else:
                            epi_name_mod = epi_name_mod + ch

                    file_format = old_name.split('.')[-1]

                    new_name = name_of_series + \
                        f' - S{season}E{identifier} - {epi_name_mod}.{file_format}'
                    logging.info(f'{old_name}\n--> {new_name}')

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
            logging.info(str(no_of_operations - no_of_operations_done) + "file(s) were not renamed")
            self.alertMessageBox("Notice", str(no_of_operations - no_of_operations_done) + " file(s) were not renamed")


    def ReformatNames2(self):

        dest_directory = self.directory_textedit.toPlainText()
        old_names_list = os.listdir(dest_directory)
        no_of_operations = len(old_names_list)
        no_of_operations_done = 0
        pattern = re.compile(r'\b(\d{1,2})\w(\d\d)\b')

        for old_name in old_names_list:

            extract = pattern.search(old_name)

            if extract == None:
                logging.info("Filenames are not in the expected format\n")
                return

            season = str('%02d' % int(extract.group(1)))
            epi_no = str('%02d' % int(extract.group(2)))

            epi_name = old_name.split('-')[-1]

            new_name = f"{name_of_series} - S{season}E{epi_no} - {epi_name}"

            logging.info(f"{old_name} --> {new_name}")

            if self.required_verification == 'Y':
                verification = input('Y/N: ')
            else:
                verification = 'Y'

            if verification.upper() == 'Y':
                old_path = os.path.join(dest_directory, old_name)
                new_path = os.path.join(dest_directory, new_name)
                os.rename(old_path, new_path)
                no_of_operations_done += 1
                logging.info()

        if no_of_operations == no_of_operations_done:
            logging.info("All Files renamed successfully")
        else:
            logging.info(str(no_of_operations - no_of_operations_done) + " file(s) were not renamed")


# ==============================FOR XX.EPISODE_NAME FORMAT========================================

    def ReformatNames(self):

        dest_directory = self.directory_textedit.toPlainText()
        season = eval(input("Season: "))
        old_names_list = os.listdir(dest_directory)
        no_of_operations = len(old_names_list)
        no_of_operations_done = 0

        for old_name in old_names_list:

            try:
                ep_no = int(old_name.split('.', 1)[0])
            except ValueError:
                continue

            epi_name = old_name.split(' ', 1)[1]

            try:
                subtract_episodes = episode_per_season * (season - 1)
            except NameError:
                subtract_episodes = total_episodes

            if ep_no - subtract_episodes < 0:
                logging.info("\nEpisode Number changing to Negative")
                logging.info("Please Check ReformatNames Conditions")
                return

            new_name = name_of_series + ' - ' + 'S' + \
                str('%02d' % season) + 'E' + str('%02d' %
                                                (ep_no - subtract_episodes)) + ' - ' + epi_name

            logging.info(f'{old_name} --> {new_name}')

            if self.required_verification == 'Y':
                verification = input('Y/N: ')
            else:
                verification = 'Y'

            if verification.upper() == 'Y':
                old_path = os.path.join(dest_directory, old_name)
                new_path = os.path.join(dest_directory, new_name)
                os.rename(old_path, new_path)
                no_of_operations_done += 1
                logging.info()

        if no_of_operations == no_of_operations_done:
            logging.info("All Files renamed successfully")
        else:
            logging.info(str(no_of_operations - no_of_operations_done) + " files were not renamed")


# ====================================MAIN=============================================

def main():
    app = MainUI()
    app.show()

main()

if __name__ == "__main__":
    main()
