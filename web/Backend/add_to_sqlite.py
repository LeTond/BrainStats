import sys

from Backend.json_worker import Json
from Backend.parsing_aseg_stats import ParsingResults

sys.path.append('/web/fsweb')

from fsweb.models import Projects, Subjects, StructureStatistic, MainStatistic, Pathology
from django.db import transaction


class AddToSQL:
    def __init__(self):
        self.json = Json()
        self.pres = ParsingResults()

    @staticmethod
    def project(project_name: str) -> int:
        """
        Если проект отсутсвует в БД, то сохраняем его и возвращаем информацию об id,
        иначе возвращаем ключ существующего проекта
        :param project_name: Название проекта
        :return: Ключ для свзывания субъекта с проектом
        """
        try:
            project = Projects.objects.get(name=project_name)
        except Exception as e:
            self.lg.error_log_file(f"{e}: Проблема в AddToSQL.project")
            print("Проблема в AddToSQL.project")

            Projects.objects.create(name=project_name)
            project = Projects.objects.get(name=project_name)

        return project

    def subject(self, project_key: str, project_id: int, pathology_id: int) -> int:
        """
        Добавление данных субъекта в БД
        :param project_key: ключ проекта (название проекта + имя субъекта + дата создания проекта)
        :param project_id: id проекта
        :param pathology_id: id патологии
        :return: None
        """
        try:
            diction = self.json.read_subject_data()[project_key]
            try:
                pk = Subjects.objects.last().id
            except AttributeError:
                pk = 0
            with transaction.atomic():
                pk += 1
                Subjects.objects.create(
                    id=pk, name=diction["subject"], sex=diction["sex"], date_of_birth=diction["date_of_birth"],
                    date_of_study=diction["date_of_study"], project=project_id, pathology=pathology_id
                )
            return pk

        except Exception as e:
            self.lg.error_log_file(f"{e}: Проблема в AddToSQL.subject")
            print("Проблема в AddToSQL.subject")

    def structure_statistic(self, project_path: str, subject_id: int):
        """
        Добавление статистики в БД
        :param project_path: путь к файлу со статистикой
        :param subject_id: id связываемого субъекта
        :return: None
        """
        try:
            statistics = self.pres.structure_statistic_data(project_path)
            id_list = []
            try:
                pk = StructureStatistic.objects.last().id
            except AttributeError:
                pk = 0
            with transaction.atomic():
                for stats in statistics:
                    pk += 1
                    id_list.append(pk)
                    StructureStatistic.objects.create(
                        id=pk, name=stats[0], NVoxels=stats[1], Volume_mm3=stats[2], normMean=stats[3],
                        normStdDev=stats[4], normMin=stats[5], normMax=stats[6], normRange=stats[7]
                    ).save()
            self.relations_subject_statistic(subject_id, id_list)

        except Exception as e:
            self.lg.error_log_file(f"{e}: Проблема в AddToSQL.structure_statistic")
            print("Проблема в AddToSQL.structure_statistic")

    def main_statistic(self, project_path: str, subject_id: int):
        """
        Добавление статистики в БД
        :param project_path: путь к файлу со статистикой
        :param subject_id: id субъекта
        :return: None
        """
        try:
            statistics = self.pres.main_statistic_data(project_path)
            try:
                pk = MainStatistic.objects.last().id
            except AttributeError:
                pk = 0
            with transaction.atomic():
                pk += 1
                MainStatistic(
                    id=pk, BrainSegVol=statistics[0], VentricleChoroidVol=statistics[1], lhCortexVol=statistics[2],
                    rhCortexVol=statistics[3], CortexVol=statistics[4], lhCerebralWhiteMatterVol=statistics[5],
                    rhCerebralWhiteMatterVol=statistics[6], CerebralWhiteMatterVol=statistics[7],
                    SubCortGrayVol=statistics[8], TotalGrayVol=statistics[9], SupraTentorialVol=statistics[10],
                    eTIV=statistics[11]
                ).save()
            self.relations_subject_main_statistic(subject_id, pk)

        except Exception as e:
            self.lg.error_log_file(f"{e}: Проблема в AddToSQL.main_statistic")
            print("Проблема в AddToSQL.main_statistic")


    @staticmethod
    def pathology(pathology_name: str):
        """
        Добавление патологии в БД
        :param pathology_name: ключ проекта в json файле
        :return: None
        """
        try:
            pathology = Pathology.objects.get(name=pathology_name)
        except Exception as e:
            self.lg.error_log_file(f"{e}: Проблема в AddToSQL.pathology")
            print("Проблема в AddToSQL.pathology")
            Pathology.objects.create(name=pathology_name)
            pathology = Pathology.objects.get(name=pathology_name)

        return pathology

    @staticmethod
    def relations_subject_statistic(subject_id: int, id_list: list):
        """
        Добавление связи субъекта и статистических данных из таблицы structure_statistic
        :param subject_id: id субъекта
        :param id_list: список с id статистических данных из исследования для субъекта,
        :return: None
        """
        try:
            subject = Subjects.objects.get(id=subject_id)
            with transaction.atomic():
                for stat_id in id_list:
                    subject.statistic.add(StructureStatistic.objects.get(id=stat_id).id)
        
        except Exception as e:
            self.lg.error_log_file(f"{e}: Проблема в AddToSQL.relations_subject_statistic")
            print("Проблема в AddToSQL.relations_subject_statistic")

    @staticmethod
    def relations_subject_main_statistic(subject_id: int, stat_id: int):
        """
        Добавление связи субъекта и статистических данных из таблицы main_statistic
        :param subject_id: id связываемого субъекта
        :param stat_id: id связываемой статистики
        :return: None
        """
        try:
            subject = Subjects.objects.get(id=subject_id)
            with transaction.atomic():
                subject.main_statistic.add(MainStatistic.objects.get(id=stat_id).id)

        except Exception as e:
            self.lg.error_log_file(f"{e}: Проблема в AddToSQL.relations_subject_main_statistic")
            print("Проблема в AddToSQL.relations_subject_main_statistic")


