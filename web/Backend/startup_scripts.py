import os, sys
import time
import subprocess
import asyncio

from threading import Thread
from typing import AnyStr

from Backend.observer import RunObserver
from Backend.log_files import Log

sys.path.append('/web/Configuration')
from Configuration.key_words_and_directories_list import preprocess_script_path, view_script_path, subjects_path
from Configuration.log_messages import *


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
    def start_up_freeview(cmd: AnyStr) -> None:
        """
        Вызов скрипта для запуска встроенного во freesurfer просмотровщика
        :param cmd: имя программы (freeview) для запуска
        :return: None
        """
        command_list = [f'{view_script_path} {cmd}']
        subprocess.Popen(command_list, shell = True, executable = '/bin/bash', cwd = '/')

    # @staticmethod
    # def start_up_preprocessing(command: AnyStr, folder_name: str) -> None:
    #     """
    #     Вызов скрипта для запуска процесса обсчета данных МР-морфометрии
    #     :param command: параметры для запуска программы
    #     :return: None
    #     """
    #     lg = Log()
    #     command_list = [f'{preprocess_script_path} {command}']

    #     # await asyncio.sleep(1)

    #     lg.event_log_file(f"{MESSAGE_FSR_STARTUP} {folder_name} ")
    #     lg.event_log_file(command_list)

    #     try:
    #         process = subprocess.Popen(command_list, shell = True, executable = '/bin/bash', cwd = '/')
            
    #         while process.poll() is None:
    #             lg.event_log_file(f"SLEEEP FSR RUN {folder_name}")    
    #             time.sleep(15)

    #     except KeyboardInterrupt:
    #         print("Процесс был прерван пользователем.")
        
    #     except Exception as e:
    #         lg.error_log_file(f"{e}: {MESSAGE_RUN_START_FREESURFER_PROBLEM}: {folder_name}")
        
    #     finally:
    #         # Завершение процесса
    #         process.terminate()
    #         process.wait()
    #         lg.event_log_file(f"{MESSAGE_STOP_FREESURFER}: {folder_name}")    

        # subprocess.Popen(command_list, shell = True, executable = '/bin/bash', cwd = '/')
        # await asyncio.sleep(1)

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
