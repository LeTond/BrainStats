import sys
import os
import time
import asyncio

from Backend.add_to_sqlite import AddToSQL
from Backend.json_worker import Json
from Backend.log_files import Log
from Backend.parsing_aseg_stats import ParsingResults

sys.path.append('/web/Configuration')
from Configuration.key_words_and_directories_list import projects_paths, subjects_path, list_projects_paths
from Configuration.log_messages import *

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


class EventHandler(FileSystemEventHandler):
    """
    Запускаем обсервер, который будет отслеживать состояние в директории с данными субъектов исследования и
    по-необходимости добавлять обсчитанные данные в БД.
    """
    def __init__(self, folder_name):
        self.folder_name = folder_name
        self.subjects_path = subjects_path
        self.list_projects_paths = list_projects_paths
        self.lg = Log()
        self.json = Json()
        self.sql = AddToSQL()
        self.pr = ParsingResults()
        self.structure_statistic = self.pr.structure_statistic_data
        self.main_statistic = self.pr.main_statistic_data
        self.__is_active_observer = True

    @property
    def is_active_observer(self):
        return self.__is_active_observer

    @is_active_observer.setter
    def is_active_observer(self, new_status):
        if not isinstance(new_status, bool):
            raise TypeError('new_status must be BOOL')
        else:
            self.__is_active_observer = new_status

    def search_exist_projects(self) -> list:
        """
        Просматриваем и создает список с имеющимися обработанными исследованиями
        :return: Возвращает список с местонахождением файлов со статистикой (aseg.stats)
        """
        try:
            directs_list = []
            for directs, direct, files in os.walk(self.subjects_path):
                for file in files:
                    if 'aseg.stats' == file:
                        directs_list.append(directs)
        
            self.lg.event_log_file(f"{MESSAGE_SEARCH_EXIST_PROJECT}")
            return directs_list
        
        except Exception as e:
            self.lg.error_log_file(f"{e}: {MESSAGE_SEARCH_EXIST_PROJECT_ERROR}")

    def save_new_project(self, project_key: str, project_path: str):
        """
        После прочтения json отправляем данные субъекта в базу данных, после чего удаляем эти данные
        из json файла с информацией о проектах по ключю project_name
        :param project_key: название проекта (ключ в json)
        :param project_path: путь к list_projects_paths.txt с информацией об исследованиях, сохраненных в БД
        :return: None
        """
        try:
            project_name = self.json.read_subject_data()[project_key]["project"]
            pathology_name = self.json.read_subject_data()[project_key]["pathology"]
            
            project_id = self.sql.project(project_name)
            pathology_id = self.sql.pathology(pathology_name)
            subject_id = self.sql.subject(project_key, project_id, pathology_id)

            self.sql.structure_statistic(project_path, subject_id)
            self.sql.main_statistic(project_path, subject_id)
            # self.json.delete_subject_data_from_json(project_name)
            self.lg.event_log_file(f"{MESSAGE_ADD_NEW_RESULTS} {project_name}")

        except Exception as e:
            self.lg.error_log_file(f"{e}: {MESSAGE_ADD_NEW_RESULTS_ERROR}")

    def on_any_event(self, event):
        print(event.src_path)
        pass

    def on_created(self, event):
        new_project_path = self.subjects_path + self.folder_name

        if (event.src_path == f"{new_project_path}/stats/aseg.stats"):
            self.lg.event_log_file(f"{MESSAGE_ON_CREATED} {event.src_path}")

            try:
                list_projects = open(self.list_projects_paths, 'r')    # Открываем лог с сохранёнными проектами
                list_projects = list_projects.read().split('\n')
                
                self.save_new_project(self.pr.project_name(new_project_path), new_project_path)

                if new_project_path not in list_projects:
                    write_to_list = open(self.list_projects_paths, 'a')
                    write_to_list.write(new_project_path + '\n')
                   
                    self.lg.event_log_file(f"{MESSAGE_ON_CREATED_LOG_SAVED} {self.list_projects_paths}")
                    self.is_active_observer = False
                    self.lg.event_log_file(f"{MESSAGE_ON_CREATED_OBSERVER_STOPPED} {self.folder_name}")

            except ConnectionError:
                self.lg.error_log_file(f"{MESSAGE_CONNECTION_ERROR}: ON_CREATED {new_project_path}")

            except Exception as e:
                self.lg.error_log_file(f"{e}: {MESSAGE_ON_CREATED_ERROR} {new_project_path}")

    def on_deleted(self, event):
        pass

    def on_modified(self, event):
        pass

    def on_moved(self, event):
        print(event.src_path)
        pass


class RunObserver:
    def __init__(self, folder_name):
        self.subjects_path = subjects_path
        self.folder_name = folder_name
        self.lg = Log()
        self.lg.event_log_file(f"{MESSAGE_RUN_OBSERVER} {self.folder_name}")
        self.counter = 0
    
    async def __call__(self):
        try:
            event_handler = EventHandler(self.folder_name)
            observer = Observer()
            observer.schedule(event_handler, path = (self.subjects_path + self.folder_name + '/stats/'), recursive = False)
            observer.start()

            while event_handler.is_active_observer and self.counter < 1000:
                try:
                    self.counter += 1
                    await asyncio.sleep(60)
                
                except KeyboardInterrupt:
                    observer.stop()

        except Exception as e:
            self.lg.error_log_file(f"{e} {MESSAGE_RUN_OBSERVER_ERROR}")
