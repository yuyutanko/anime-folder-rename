import os
import sys
import pyperclip
from mass_rename_design import Ui_MainWindow
from PyQt5 import QtWidgets


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.folder_path = None
        self.genre_folder_path = None
        self.new_name = None
        self.folder_list_true = []
        self.genre_list_true = []
        self.directory_list = None
        self.genres_second = []
        self.genres_first = None
        self.anime_folder = None
        self.iterations = 0
        self.setupUi(self)
        self.setWindowTitle('Anime Folder rename')
        self.checkboxes = [
            self.checkBox_1,
            self.checkBox_2,
            self.checkBox_3,
            self.checkBox_4,
            self.checkBox_5,
            self.checkBox_6,
            self.checkBox_7,
            self.checkBox_8,
            self.checkBox_9,
            self.checkBox_10,
            self.checkBox_11,
            self.checkBox_12,
            self.checkBox_13,
            self.checkBox_14,
            self.checkBox_15,
            self.checkBox_16,
            self.checkBox_17,
            self.checkBox_18,
            self.checkBox_19,
            self.checkBox_20,
            self.checkBox_21,
            self.checkBox_22,
            self.checkBox_23,
            self.checkBox_24,
            self.checkBox_25,
            self.checkBox_26,
            self.checkBox_27,
            self.checkBox_28,
            self.checkBox_29,
            self.checkBox_30,
            self.checkBox_31,
            self.checkBox_32
        ]
        self.new_genres = [
            self.lineEdit_2,
            self.lineEdit_3,
            self.lineEdit_4,
            self.lineEdit_5,
            self.lineEdit_6,
            self.lineEdit_7,
            self.lineEdit_8,
            self.lineEdit_9,
            self.lineEdit_10,
            self.lineEdit_11,
            self.lineEdit_12,
            self.lineEdit_13,
            self.lineEdit_14,
            self.lineEdit_15,
            self.lineEdit_16,
            self.lineEdit_17
        ]
        self.new_name = None
        self.pushButton.clicked.connect(self.browse_folder)
        self.pushButton_change.clicked.connect(self.change_name)

    def browse_folder(self):
        dialog = QtWidgets.QFileDialog()
        self.folder_path = dialog.getExistingDirectory(None, "Select Folder")
        self.label.setText(self.folder_path)  # Рисуем путь до папки
        self.naming()

    def naming(self):
        self.directory_list = os.listdir(self.folder_path)  # Забиваем список директорий из папки, которую указали
        for folder in self.directory_list:  # Для каждой такой папки
            if os.path.isdir(os.path.join(self.folder_path, folder)):  # Удостоверится что это папка
                self.folder_list_true.append(folder)  # Записать в настоящий список директорий
        self.label_2.setText(self.folder_list_true[0])  # Показать первую директорию в списке
        pyperclip.copy(self.folder_list_true[0])
        # Sorted to folder_list_true
        self.genre_folder_path = (os.path.split(self.folder_path))[0]  # Записать наддиректорию с жанрами
        self.recheck_box()

    def recheck_box(self):
        self.genres_second = []
        for box in self.checkboxes:
            box.setText(' ')
        self.genres_first = os.listdir(self.genre_folder_path)  # Записать список жанров
        self.directory_list = os.listdir(self.folder_path)
        for genre in self.genres_first:
            if os.path.isdir(os.path.join(self.genre_folder_path, genre)):
                self.genres_second.append(genre)
        iteration = 0
        for genre in self.genres_second:
            if not genre[0] == '1':
                self.checkboxes[iteration].setText(genre)
                iteration += 1

    def change_name(self):
        self.new_name = self.lineEdit.text()
        if self.new_name:
            self.anime_folder = os.path.join(self.folder_path, self.new_name)
            print('Iru')
            os.rename(os.path.join(self.folder_path, self.folder_list_true[self.iterations]),
                      os.path.join(self.folder_path, self.new_name))
            self.create_additional_dirs()
            self.create_symlinks()
        else:
            self.anime_folder = os.path.join(self.folder_path, self.label_2.text())
            self.create_additional_dirs()
            self.create_symlinks()

        self.iterations += 1
        try:
            self.label_2.setText(self.folder_list_true[self.iterations])
            pyperclip.copy(self.folder_list_true[self.iterations])
        except IndexError:
            print('Out of range')
            self.label_2.setText('Out of range')
        for line in self.new_genres:
            line.clear()
        for box in self.checkboxes:
            box.setChecked(False)
        self.recheck_box()
        print('Nai')

    def create_symlinks(self):
        for box in self.checkboxes:
            if box.isChecked():
                destination = os.path.join(self.genre_folder_path, box.text())
                if self.new_name:
                    true_destination = os.path.join(destination, self.new_name)
                else:
                    true_destination = os.path.join(destination, self.label_2.text())
                source = self.anime_folder
                os.symlink(source, true_destination)

        for new_genre in self.new_genres:
            if new_genre.text():
                destination = os.path.join(self.genre_folder_path, new_genre.text())
                if self.new_name:
                    true_destination = os.path.join(destination, self.new_name)
                else:
                    true_destination = os.path.join(destination, self.label_2.text())
                source = self.anime_folder
                os.symlink(source, true_destination)

    def create_additional_dirs(self):
        for new_genre in self.new_genres:
            if new_genre.text():
                new_path = os.path.join(self.genre_folder_path, new_genre.text())
                os.mkdir(new_path)


def main():
    app = QtWidgets.QApplication(sys.argv)
    application = MainWindow()
    application.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
