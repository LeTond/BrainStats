import os, sys
import subprocess
import asyncio


# from Backend.observer import RunObserver
from Backend.log_files import Log

sys.path.append('/web/Configuration')
from Configuration.key_words_and_directories_list import preprocess_script_path, view_script_path, subjects_path
from Configuration.log_messages import *

# from watchdog.observers import Observer
from typing import AnyStr


class DataSearcher:
    @staticmethod
    def search_files() -> list:
        """
        Поиск готовых к обработке файлов с расширением NifTy
        :return: Список файлов
        """
        subjects_list = []
        for file in os.listdir('/Applications/freesurfer/subjects'):
            if '.nii' in file:
                subjects_list.append(file.strip('.nii'))
        return subjects_list

    @staticmethod
    def start_up_parameter() -> list:
        """
        Создаем список со сценариями обработки данных
        :return: список с параметрами
        """
        start_up_parameter = [
            "-all",
            "-hemi lh",
            "-hemi rh",
            "-autorecon1",
            "-autorecon2",
            "-autorecon3",
        ]
        return start_up_parameter

    @staticmethod
    def sex_list() -> list:
        """
        Создание списка для выбора пола субъекта
        :return: список полов
        """
        sex_list_ = [
            "Male",
            "Female",
            "Other",
        ]
        return sex_list_


class FreeScripts:
    @staticmethod
    async def start_up_freeview(cmd: AnyStr) -> None:
        """
        Вызов скрипта для запуска встроенного во freesurfer просмотровщика
        :param cmd: имя программы (freeview) для запуска
        :return: None
        """
        command_list = [f'{view_script_path} {cmd}']
        subprocess.Popen(command_list, shell = True, executable = '/bin/bash', cwd = '/')

    @staticmethod
    async def start_up_preprocessing(command: AnyStr, folder_name: str) -> None:
        """
        Вызов скрипта для запуска процесса обсчета данных МР-морфометрии
        :param command: параметры для запуска программы
        :return: None
        """
        lg = Log()
        command_list = [f'{preprocess_script_path} {command}']
        
        await asyncio.sleep(1)
        
        lg.event_log_file(f"{MESSAGE_FSR_STARTUP} {folder_name} ")
        lg.event_log_file(command_list)

        subprocess.Popen(command_list, shell = True, executable = '/bin/bash', cwd = '/')
        await asyncio.sleep(1)
        
