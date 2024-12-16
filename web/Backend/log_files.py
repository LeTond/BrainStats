import sys
import datetime

sys.path.append('/web/Configuration')

from Configuration.key_words_and_directories_list import error_log_path

from Backend.json_worker import Json


class Log:
    def __init__(self):
        self.js = Json()
        self.error_log_path = error_log_path

    def write_subject_data_to_json(self, project_key: str, diction: dict):
        """
        Запись названия проекта и данных субъекта в json
        :param project_key: название проекта
        :param diction: словарь с данными субъекта исследования
        :return: None
        """
        dict_to_json = self.js.read_json()
        dict_to_json[project_key] = diction
        self.js.write_json(dict_to_json)

    def error_log_file(self, message: str):
        """
        Запись ошибок в log
        :param message: сообщение об ошибке
        :return: None
        """
        file = open(self.error_log_path, 'a')
        file.write(f"{datetime.datetime.now()}: {message} \n")
        file.close()
