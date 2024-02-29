import logging
import pymysql
import traceback
from config import mysql


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s:%(levelname)s:%(name)s:%(message)s')
file_handler = logging.FileHandler('tribunals.log')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

class TribunalsCaseListInsert:
    
    def __init__(self, court_type_id, _search_by, _location, _case_type, _case_status, _party_type, _party_name, _filing_no, _case_number, _advocate_name, _case_year, case_list_data):
        self.court_type_id = court_type_id
        self._search_by = _search_by
        self._location = _location
        self._case_type = _case_type
        self._case_status = _case_status
        self._party_type = _party_type
        self._party_name = _party_name
        self._filing_no = _filing_no
        self._case_number = _case_number
        self._advocate_name = _advocate_name
        self._case_year = _case_year
        self.case_list_data = case_list_data

    def createTribunalsCaseList(self):
        try:
            conn = mysql.connect()
            cursor = conn.cursor(pymysql.cursors.DictCursor)
            sqlqueryinsert = "INSERT INTO `case_list`(`court_type_id`,`search_by`,`location`,`sr_no`,`filing_no`,`case_no`,`case_title`,`registration_date`,`status`,`action`,`advocate_name`,`party_name`,`party_type`,`case_type`,`case_number`,`case_year`,`case_status`) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
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
                    self._case_status
                )
                cursor.execute(sqlqueryinsert, bindData)
            conn.commit()
            if self._search_by == '1':
                sqlselectquery = f"SELECT * FROM `case_list` where `search_by`='{self._search_by}' and `location`='{self._location}' and `case_type`='{self._case_type}' and `case_number`='{self._case_number}' and `case_year`='{self._case_year}'"
            elif self._search_by == '2':
                sqlselectquery = f"SELECT * FROM `case_list` where `search_by`='{self._search_by}' and `location`='{self._location}' and `filing_no`='{self._filing_no}'"
            elif self._search_by == '3':
                sqlselectquery = f"SELECT * FROM `case_list` where `search_by`='{self._search_by}' and `location`='{self._location}' and `case_type`='{self._case_type}' and `case_status`='{self._case_status}' and `case_year`='{self._case_year}'"
            elif self._search_by == '4':
                sqlselectquery = f"SELECT * FROM `case_list` where `search_by`='{self._search_by}' and `location`='{self._location}' and `party_type`='{self._party_type}' and `party_name`='{self._party_name}' and `case_year`='{self._case_year}'"
            elif self._search_by == '5':
                sqlselectquery = f"SELECT * FROM `case_list` where `search_by`='{self._search_by}' and `location`='{self._location}' and `advocate_name`='{self._advocate_name}' and `case_year`='{self._case_year}'"
            cursor.execute(sqlselectquery)
            case_list_table_data = cursor.fetchall()
            conn.commit()
        except:
            logger.info(f"Error in SQL createTribunalsCaseList :- {traceback.format_exc()}")
        finally:
            cursor.close()
            conn.close()
            return case_list_table_data

