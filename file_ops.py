import os


class FileOperations:
    def __init__(self, input_path):
        self.input_path = input_path

        self.input_path_folders = []
        self.genre_path = None
        self.genre_list = []
        self.genre_list_with_path = []

    def scan_main_folder(self):
        """Записывает список директорий в переменную self.input_path_folders"""
        self.input_path_folders = self._get_folders_from_path(path=self.input_path, skip_one_prefix=False)

    def get_genres(self, genre_source='parent_folder') -> list:
        """
        Подготавливает список жанров.
        По умолчанию формируется из списка директорий, которые находятся на уровень выше основного пути.
        Записывает список в переменную self.genre_list, её же и возвращает.
        :param genre_source Директория с папками(названиями жанров), по умолчанию на уровень выше основной.
        """
        if genre_source == 'parent_folder':
            self.genre_path = self._get_parent_directory(self.input_path)
        self.genre_list = self._get_folders_from_path(path=self.genre_path)
        self.generate_genre_paths()
        return self.genre_list

    def prepare_title_info(self, current_title) -> list:
        """
        Возвращает список жанров определённого тайтла, проверяя наличие симлинки в директориях жанров.
        :param current_title: Тайтл
        :return:
        """
        title_genre_list = []
        for genre_path in self.genre_list_with_path:
            listdir = os.listdir(genre_path)
            if current_title in listdir:
                genre = os.path.split(genre_path)[-1]
                title_genre_list.append(genre)
        return title_genre_list

    def generate_genre_paths(self):
        """
        Генерирует пути до директорий жанров.
        Забивает в список self.genre_list_with_path пути до директорий нужных жанров.
        """
        for genre in self.genre_list:
            path = os.path.join(self.genre_path, genre)
            self.genre_list_with_path.append(path)

    def create_symlinks(self, genre_name, current_title):
        """
        Создает симлинк, принимает название жанра и название тайтла, если он есть, то действие пропускается.
        :param genre_name Название жанра.
        :param current_title Название тайтла.
        """
        current_title_path = os.path.join(self.input_path, current_title)
        genre_folder_path = os.path.join(self.genre_path, genre_name)
        new_symlink_path = os.path.join(genre_folder_path, current_title)
        try:
            os.symlink(current_title_path, new_symlink_path)
        except FileExistsError:
            pass

    def change_name(self, current_title, new_name):
        """
        Переименовывает директорию(тайтл).
        :param current_title: Тайтл
        :param new_name: Новое название
        """
        old_path = os.path.join(self.input_path, current_title)
        new_path = os.path.join(self.input_path, new_name)
        os.rename(old_path, new_path)

    def create_new_genres_dir(self, new_genres, current_title):
        """
        Создает дополнительные директории с жанрами и создает симлинки с тайтлом в директориях нового жанра.
        :param new_genres: Список с новыми жанрами.
        :param current_title: Тайтл
        """
        for new_genre in new_genres:
            new_genre_path = os.path.join(self.genre_path, new_genre.lstrip())
            os.mkdir(new_genre_path)
            print(new_genre.lstrip())
            self.create_symlinks(genre_name=new_genre.lstrip(), current_title=current_title)

    @staticmethod
    def _get_parent_directory(path) -> os.path:
        """
        Только для этого класса, возвращает путь до родительской директории.
        :param path: путь.
        :return:
        """
        return (os.path.split(path))[0]

    @staticmethod
    def _get_folders_from_path(path, skip_one_prefix=True) -> list:
        """
        Отфильтровывает папки из списка всех элементов в директории.
        :param path: путь.
        :param skip_one_prefix: Если True, то папки, которые начинаются с единицы, не будут учтены в списке.
        """
        listdir = os.listdir(path)
        folders_list = []
        for folder in listdir:
            if os.path.isdir(os.path.join(path, folder)):
                if skip_one_prefix:
                    if not folder.startswith('1'):
                        folders_list.append(folder)
                else:
                    folders_list.append(folder)

        folders_list.sort()
        return folders_list

