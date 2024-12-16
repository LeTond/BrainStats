import sys
import json

sys.path.append('/web/Configuration')

from Configuration.key_words_and_directories_list import json_project_names_path


class Json:
    def __init__(self):
        self.json_project_names_path = json_project_names_path

    def read_json(self) -> dict:
        """
        Чтение данных из json
        :return:
        """
        try:
            with open(self.json_project_names_path) as file:
                return json.load(file)
        except Exception as e:
            # self.lg.error_log_file(f"{e}: Отсутствует файл ./Logs/created_project_names.json")

            with open(self.json_project_names_path, 'w', encoding='utf-8') as f:
                json.dump({}, f)


    def write_json(self, value: dict):
        """
        Запись данных в json
        :param value: словарь с данными для записи
        :return: None
        """
        with open(self.json_project_names_path, 'w') as file:
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
