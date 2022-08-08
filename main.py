import sys

import pyperclip
from PyQt5 import QtWidgets, QtCore

from mass_rename_design import Ui_MainWindow
from file_ops import FileOperations


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        # Startup
        self.setupUi(self)
        self.setWindowTitle('Anime Folder Rename')
        for cb in self.checkboxes():
            cb.hide()
        # Vars
        self.file_ops = None
        self.ch_bxs = list()
        # Buttons connects
        self.btn_main_dir_path_browse.clicked.connect(self.browse)
        self.btn_main_dir_scan.clicked.connect(self.scan)
        self.btn_process.clicked.connect(self.write_changes)
        # List connects
        self.listWidget.clicked.connect(self.anime_title_info)
        self.listWidget.currentRowChanged.connect(self.anime_title_info)
        self.listWidget.clear()

    def checkboxes(self):
        return self.ch_bxs

    def browse(self):
        """
        При нажатии на кнопку browse, появляется диалоговое окно с выбором директории.
        Создается объект для операций с файлами в ОС.
        В поле ввода для пути появляется выбранная директория.
        """
        dialog = QtWidgets.QFileDialog()
        input_path = dialog.getExistingDirectory(None, "Select Folder")
        self.file_ops = FileOperations(input_path=input_path)
        self.led_input_path.setText(self.file_ops.input_path)

    def scan(self) -> None:
        """
        При нажатии на кнопку Scan выполняется метод в классе FileOperations,
        который записывает список директорий, что находятся в основной.
        Выполняется метод, который выводит список тайтлов в виджет списка.
        Выполняется метод, который раскрывает чекбоксы в соответствии найденным жанрам.
        """
        self.file_ops.scan_main_folder()
        self.show_folder_content()
        self.show_genres()

    def show_folder_content(self):
        """Выводит список тайтлов в виджет списка."""
        self.listWidget.clear()
        self.listWidget.addItems(self.file_ops.input_path_folders)

    def show_genres(self):
        """Раскрывает чекбоксы в соответствии найденным жанрам"""
        for index, genre in enumerate(self.file_ops.get_genres()):
            self.checkboxes()[index].show()
            self.checkboxes()[index].setText(genre)
            print((self.checkboxes()[index].pos().__pos__()))

    def anime_title_info(self):
        """
        При нажатии на строку в списке, подтянется информация.
        Проверяет наличие симлинков в директориях жанров, если они есть, то проставляет чекбоксы соответственно.
        """
        row = self.listWidget.currentRow()
        current_title = self.file_ops.input_path_folders[row]
        self.label_current_name.setText(current_title)
        pyperclip.copy(current_title)
        genres = self.file_ops.prepare_title_info(current_title)
        self.clear_boxes()
        for cb in self.checkboxes():
            for genre in genres:
                if cb.text() == genre:
                    cb.setChecked(True)

    def clear_boxes(self):
        """Нужен для снятия всех галочек, при переходе на другой тайтл."""
        for cb in self.checkboxes():
            cb.setChecked(False)

    def write_changes(self):
        """
        При нажатии на кнопку process введённые данные будут обработаны.
        Изменится название папки, если новое. Создадутся симлинки по жанрам, если отмечены.
        Создадутся директории для новых жанров и туда сразу же запишутся симлинки.
        По окончании, выделение списка переключится на следующую строку.
        """
        row = self.listWidget.currentRow()
        current_title_name = self.file_ops.input_path_folders[row]
        new_title_name = self.led_new_name.text()
        new_genres = self.led_new_genres.text()

        if new_title_name:
            self.file_ops.change_name(current_title_name, new_title_name)
            current_title_name = new_title_name

        for cb in self.checkboxes():
            if cb.isChecked():
                genre_name = cb.text()
                self.file_ops.create_symlinks(genre_name, current_title_name)

        if new_genres:
            new_genres_list = new_genres.split(',')
            self.file_ops.create_new_genres_dir(new_genres_list, current_title_name)

        self.scan()
        self.led_new_genres.clear()
        self.led_new_name.clear()
        self.listWidget.setCurrentRow(row + 1)


class Alert(QtWidgets.QDialog):
    def __init__(self, title='Default title', message='Default Alert'):
        """Show dialog message."""
        super().__init__()
        q_button = QtWidgets.QDialogButtonBox.Ok
        # Settings
        self.setWindowFlag(QtCore.Qt.WindowCloseButtonHint, False)
        self.setWindowTitle(title)
        # Layout
        self.buttonBox = QtWidgets.QDialogButtonBox(q_button)
        self.layout = QtWidgets.QHBoxLayout()
        self.layout.addWidget(QtWidgets.QLabel(message))
        self.layout.addWidget(self.buttonBox)
        self.setLayout(self.layout)
        # OK button connect
        self.buttonBox.accepted.connect(self.accept)

    def accept(self) -> None:
        self.close()


def main():
    app = QtWidgets.QApplication(sys.argv)
    application = MainWindow()
    application.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
