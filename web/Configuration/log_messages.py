#######################################################################################
## 		EVENT MESSAGES
#######################################################################################
##startup_scripts.py
MESSAGE_FSR_STARTUP = 'START FreeScripts.START_UP_PREPROCESSING METHOD for study'

##views.py
MESSAGE_WRITE_JSON_SUBJECT = 'Write to log_subject_data_json new ran Subject'

##observer.py
MESSAGE_SEARCH_EXIST_PROJECT = 'Was Found new aseg.stats by EventHandler.search_existing_projects'
MESSAGE_ADD_NEW_RESULTS = 'Added aseg.stats result data to Sqlite. Study:'
MESSAGE_ON_CREATED_FOUND = 'ON_CREATED found a new aseg.stats'
MESSAGE_ON_CREATED_LOG_SAVED = 'Log info was saved:'
MESSAGE_ON_CREATED_OBSERVER_STOPPED = 'Observer was STOPPED for Subject: '
MESSAGE_RUN_OBSERVER = 'START RunObserver for Subject:'

#######################################################################################
## 		ERROR MESSAGES
#######################################################################################
##json_worker.py
MESSAGE_READ_JSON_PROBLEM = 'READ JSON PROBLEM'
MESSAGE_WRITE_JSON_PROBLEM = 'WRITE JSON PROBLEM'

##add_to_sqlite.py
MESSAGE_SQL_PROJECT_PROBLEM = 'Problem with AddToSQL.PROJECT method'
MESSAGE_SQL_SUBJECT_PROBLEM = 'Problem with AddToSQL.SUBJECT method'
MESSAGE_SQL_STRUCTURE_STATISTIC_PROBLEM = 'Problem with AddToSQL.STRUCTURE_STATISTIC method'
MESSAGE_SQL_MAIN_STATISTIC_PROBLEM = 'Problem with AddToSQL.MAIN_STATISTIC method'
MESSAGE_SQL_PATHOLOGY_PROBLEM = 'Problem with AddToSQL.PATHOLOGY method'
MESSAGE_SQL_RSS_PROBLEM = 'Problem with AddToSQL.RELATIONS_SUBJECT_STATISTIC method'
MESSAGE_SQL_RSMS_PROBLEM = 'Problem with AddToSQL.RELATIONS_SUBJECT_MAIN_STATISTIC method'

##views.py
MESSAGE_VIEW_CREATE_PROJECT_GET = 'Problem with CreateProjectView.GET method'
MESSAGE_VIEW_CREATE_PROJECT_POST = 'Problem with CreateProjectView.POST method'
MESSAGE_PROJECTVIEW_GET_PROBLEM = 'Problem in ProjectsView.get'
MESSAGE_SUBJECTVIEW_GET_PROBLEM = 'Problem in SubjectsView.get'
MESSAGE_STATISTICVIEW_GET_PROBLEM = 'Problem in StatisticView.get'
MESSAGE_CONNECTION_ERROR = 'Connection Error'
MESSAGE_PROJECT_DONT_EXIST = 'Projects Does Not Exist'
MESSAGE_SUBJECT_DONT_EXIST = 'Subject Does Not Exist'

##parsing_aseg_stats.py
MESSAGE_ASEG_STATS_ERROR = 'Read ASEG_SATS Problem'
MESSAGE_ASEG_STATS_PROJECT_NAME_ERROR = 'Read ASEG_SATS Problem with SUBJECTNAME sentence'
MESSAGE_ASEG_STATS_INDEX_ERROR = 'Error while diction create. IndexError: sentence number incorrect'
MESSAGE_ASEG_STATS_MAIN_ERROR = 'Error while diction create. MAIN_STATISTIC_DATA PROBLEM'
MESSAGE_ASEG_STATS_STRUCTURE_ERROR = 'IndexError: Error while diction create. STATISTIC DATA PROBLEM'

##observer.py
MESSAGE_SEARCH_EXIST_PROJECT_ERROR = 'Problem with EventHandler.search_existing_projects'
MESSAGE_ADD_NEW_RESULTS_ERROR =  'Problem with EventHandler.save_new_project'
MESSAGE_ON_CREATED_ERROR = 'Exception Error while ON_CREATED'
MESSAGE_RUN_OBSERVER_ERROR = 'Exception Error while __CALL__ RunObserver'

#######################################################################################
## 		WARNING MESSAGES
#######################################################################################
##views.py
MESSAGE_PROJECT_DELETE_WARNING = 'You may be trying to delete a project that has studies in it. Before deleting a project, make sure all studies in it are deleted'

