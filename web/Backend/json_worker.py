import sys
import json

sys.path.append('/web/Configuration')

from Configuration.key_words_and_directories_list import add_project_log


class Json:
    def __init__(self):
        self.add_project_log = add_project_log

    def read_json(self) -> dict:
        """
        Чтение данных из json
        :return:
        """
        with open(self.add_project_log) as file:
            return json.load(file)

    def write_json(self, value: dict):
        """
        Запись данных в json
        :param value: словарь с данными для записи
        :return: None
        """
        with open(self.add_project_log, 'w') as file:
            json.dump(value, file)

    def read_subject_data(self) -> dict:
        """
        Чтение jsоn файла с информацией о субъекте
        :return:
        """
        diction = self.read_json()
        return diction

    def delete_subject_data(self, project_name: str):
        """
        Удаление из json данных о субъекте, записанных в БД
        :param project_name: название проекта
        """
        diction = self.read_json()
        for project in diction:
            if project == project_name:
                diction.pop(project_name)
                self.write_json(diction)
                break
