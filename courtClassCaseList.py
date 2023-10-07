import logging
import pymysql
from config import mysql
import traceback


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s:%(levelname)s:%(name)s:%(message)s')
file_handler = logging.FileHandler('tribunals.log')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

class TribunalsCaseListInsert:
    
    def __init__(self, court_type_id, _search_by, _location, _advocate_name, _party_name, _party_type, _case_type, _case_number, _case_year, _case_status, case_list_data):
        self.court_type_id = court_type_id
        self._search_by = _search_by
        self._location = _location
        self._advocate_name = _advocate_name
        self._party_name = _party_name
        self._party_type = _party_type
        self._case_type = _case_type
        self._case_number = _case_number
        self._case_year = _case_year
        self._case_status = _case_status
        self.case_list_data = case_list_data

    def createTribunalsCaseList(self):
        try:
            conn = mysql.connect()
            cursor = conn.cursor(pymysql.cursors.DictCursor)
            sqlquerytruncate = "TRUNCATE TABLE `case_list`"
            cursor.execute(sqlquerytruncate)
            conn.commit()
            sqlqueryinsert = "INSERT INTO `case_list`(`court_type_id`,`search_by`,`location`,`sr_no`,`filing_no`,`case_no`,`case_title`,`registration_date`,`status`,`action`,`advocate_name`,`party_name`,`party_type`,`case_type`,`case_number`,`case_year`,`case_status`,`token`,`xsrf_token`,`laravel_session`) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            for i in self.case_list_data:
                bindData = (
                    self.court_type_id,
                    self._search_by,
                    self._location,
                    i.get('sr_no', None),
                    i.get('filing_no', None),
                    i.get('case_no', None),
                    i.get('case_title', None),
                    i.get('registration_date', None),
                    i.get('status', None),
                    i.get('action', None),
                    self._advocate_name,
                    self._party_name,
                    self._party_type,
                    self._case_type,
                    self._case_number,
                    self._case_year,
                    self._case_status,
                    i.get('token', None),
                    i.get('xsrf_token', None),
                    i.get('laravel_session', None)
                )
                cursor.execute(sqlqueryinsert, bindData)
            conn.commit()
            self.case_list_data.clear()
        except Exception as err:
            logger.info(f"Error in SQL createTribunalsCaseList :- {traceback.format_exc()}")
        finally:
            cursor.close()
            conn.close()
            return logger.info('Insert Tribunals Case List successfully')


