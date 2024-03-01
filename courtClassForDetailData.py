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

class TribunalsInsert:
    
    def __init__(self, court_type_id, _status, _location, tribunals_data):
        self.court_type_id = court_type_id
        self._status = _status
        self._location = _location
        self.tribunals_data = tribunals_data
        self.tribunals_case_details = tribunals_data[0]
        self.tribunals_applicant_name_details = tribunals_data[1][0]
        self.tribunals_respondant_name_details = tribunals_data[1][1]
        self.tribunals_applicant_legal_representative = tribunals_data[2][0]
        self.tribunals_respondent_legal_representative = tribunals_data[2][1]
        self.tribunals_first_hearing_details = tribunals_data[3]
        self.tribunals_last_hearing_details = tribunals_data[4]
        self.tribunals_next_hearing_details = tribunals_data[5]
        self.tribunals_case_history = tribunals_data[6][0]
        self.tribunals_case_history_details = tribunals_data[6][1]
        self.tribunals_order_history = tribunals_data[7]
        self.tribunals_ias_other_application = tribunals_data[8]
        self.tribunals_connected_cases = tribunals_data[9]
        
    def createCaseDetails(self):
        try:
            conn = mysql.connect()
            cursor = conn.cursor(pymysql.cursors.DictCursor)
            sqlqueryinsert = "INSERT INTO `case_details`(`court_type_id`,`filing_no`,`date_of_filing`,`case_no`,`registration_date`,`status`,`location`,`case_status`) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"
            for i in self.tribunals_case_details:
                bindData = (
                    self.court_type_id,
                    i.get('filing_no', None),
                    i.get('date_of_filing', None),
                    i.get('case_no', None),
                    i.get('registration_date', None),
                    i.get('status', None),
                    self._location,
                    self._status
                )
                cursor.execute(sqlqueryinsert, bindData)
            conn.commit()
            getlastid = cursor.lastrowid
            sqlselectquery = f"SELECT * FROM `case_details` where `id`={getlastid}"
            cursor.execute(sqlselectquery)
            case_details_table_data = cursor.fetchall()
            conn.commit()
        except:
            logger.info(f"Error in SQL createCaseDetails:- {traceback.format_exc()}")
        finally:
            cursor.close()
            conn.close()
            self.createApplicantNameDetails(getlastid)
            return getlastid, case_details_table_data

    def createApplicantNameDetails(self, getlastid):
        try:
            conn = mysql.connect()
            cursor = conn.cursor(pymysql.cursors.DictCursor)
            sqlqueryinsert = "INSERT INTO `applicant_name`(`court_case_id`,`applicant_name`) VALUES (%s,%s)"
            if self.tribunals_applicant_name_details[0].get('applicant_name')!=[]:
                for applicant_name in self.tribunals_applicant_name_details[0].get('applicant_name'):
                    bindData = (
                        getlastid,
                        applicant_name,
                    )
                    cursor.execute(sqlqueryinsert, bindData)
                conn.commit()
        except:
            logger.info(f"Error in SQL createApplicantNameDetails :- {traceback.format_exc()}")
        finally:
            cursor.close()
            conn.close()
            return self.createRespondantNameDetails(getlastid)
        
    def createRespondantNameDetails(self, getlastid):
        try:
            conn = mysql.connect()
            cursor = conn.cursor(pymysql.cursors.DictCursor)
            sqlqueryinsert = "INSERT INTO `respondant_name`(`court_case_id`,`respondant_name`) VALUES (%s,%s)"
            if self.tribunals_respondant_name_details[0].get('respondant_name')!=[]:
                for respondant_name in self.tribunals_respondant_name_details[0].get('respondant_name'):
                    bindData = (
                        getlastid,
                        respondant_name,
                    )
                    cursor.execute(sqlqueryinsert, bindData)
                conn.commit()
        except:
            logger.info(f"Error in SQL createRespondantNameDetails :- {traceback.format_exc()}")
        finally:
            cursor.close()
            conn.close()
            return self.createApplicantLegalRepresentative(getlastid)

    def createApplicantLegalRepresentative(self, getlastid):
        try:
            conn = mysql.connect()
            cursor = conn.cursor(pymysql.cursors.DictCursor)
            sqlqueryinsert = "INSERT INTO `applicant_legal_representative`(`court_case_id`,`applicant_legal_representative_name`) VALUES (%s,%s)"
            if self.tribunals_applicant_legal_representative[0].get('applicant_legal_representative_name')!=[]:
                for applicant_legal_representative_name in self.tribunals_applicant_legal_representative[0].get('applicant_legal_representative_name'):
                    bindData = (
                        getlastid,
                        applicant_legal_representative_name
                    )
                    cursor.execute(sqlqueryinsert, bindData)
                conn.commit()
        except:
            logger.info(f"Error in SQL createApplicantLegalRepresentative :- {traceback.format_exc()}")
        finally:
            cursor.close()
            conn.close()
            return self.createRespondentLegalRepresentative(getlastid)

    def createRespondentLegalRepresentative(self, getlastid):
        try:
            conn = mysql.connect()
            cursor = conn.cursor(pymysql.cursors.DictCursor)
            sqlqueryinsert = "INSERT INTO `respondent_legal_representative`(`court_case_id`,`respondent_legal_representative_name`) VALUES (%s,%s)"
            if self.tribunals_respondent_legal_representative[0].get('respondent_legal_representative_name')!=[]:
                for respondent_legal_representative_name in self.tribunals_respondent_legal_representative[0].get('respondent_legal_representative_name'):
                    bindData = (
                        getlastid,
                        respondent_legal_representative_name
                    )
                    cursor.execute(sqlqueryinsert, bindData)
                conn.commit()
        except:
            logger.info(f"Error in SQL createRespondentLegalRepresentative :- {traceback.format_exc()}")
        finally:
            cursor.close()
            conn.close()
            return self.createFirstHearingDetails(getlastid)

    def createFirstHearingDetails(self, getlastid):
        try:
            conn = mysql.connect()
            cursor = conn.cursor(pymysql.cursors.DictCursor)
            sqlqueryinsert = "INSERT INTO `first_hearing_details`(`court_case_id`,`court_no`,`hearing_date`,`coram`,`stage_of_case`) VALUES (%s,%s,%s,%s,%s)"
            for i in self.tribunals_first_hearing_details:
                bindData = (
                    getlastid,
                    i.get('court_no', None),
                    i.get('hearing_date', None),
                    i.get('coram', None),
                    i.get('stage_of_case', None)
                )
                cursor.execute(sqlqueryinsert, bindData)
            conn.commit()
        except:
            logger.info(f"Error in SQL createFirstHearingDetails :- {traceback.format_exc()}")
        finally:
            cursor.close()
            conn.close()
            return self.createLastHearingDetails(getlastid)

    def createLastHearingDetails(self, getlastid):
        try:
            conn = mysql.connect()
            cursor = conn.cursor(pymysql.cursors.DictCursor)
            sqlqueryinsert = "INSERT INTO `last_hearing_details`(`court_case_id`,`court_no`,`hearing_date`,`coram`,`stage_of_case`) VALUES (%s,%s,%s,%s,%s)"
            for i in self.tribunals_last_hearing_details:
                bindData = (
                    getlastid,
                    i.get('court_no', None),
                    i.get('hearing_date', None),
                    i.get('coram', None),
                    i.get('stage_of_case', None)
                )
                cursor.execute(sqlqueryinsert, bindData)
            conn.commit()
        except:
            logger.info(f"Error in SQL createLastHearingDetails :- {traceback.format_exc()}")
        finally:
            cursor.close()
            conn.close()
            return self.createNextHearingDetails(getlastid)

    def createNextHearingDetails(self, getlastid):
        try:
            conn = mysql.connect()
            cursor = conn.cursor(pymysql.cursors.DictCursor)
            sqlqueryinsert = "INSERT INTO `next_hearing_details`(`court_case_id`,`hearing_date`,`court_no`,`proceedings_summary`,`stage_of_case`) VALUES (%s,%s,%s,%s,%s)"
            for i in self.tribunals_next_hearing_details:
                bindData = (
                    getlastid,
                    i.get('hearing_date', None),
                    i.get('court_no', None),
                    i.get('proceedings_summary', None),
                    i.get('stage_of_case', None)
                )
                cursor.execute(sqlqueryinsert, bindData)
            conn.commit()
        except:
            logger.info(f"Error in SQL createNextHearingDetails :- {traceback.format_exc()}")
        finally:
            cursor.close()
            conn.close()
            return self.createCaseHistory(getlastid)
        
    def createCaseHistory(self, getlastid):
        try:
            conn = mysql.connect()
            cursor = conn.cursor(pymysql.cursors.DictCursor)
            sqlqueryinsert = "INSERT INTO `case_history`(`court_case_id`,`sr_no`,`hearing_date`,`court_no`,`purpose`,`action`) VALUES (%s,%s,%s,%s,%s,%s)"
            for i in self.tribunals_case_history:
                bindData = (
                    getlastid,
                    i.get('sr_no', None),
                    i.get('hearing_date', None),
                    i.get('court_no', None),
                    i.get('purpose', None),
                    i.get('action', None)
                )
                cursor.execute(sqlqueryinsert, bindData)
            conn.commit()
        except:
            logger.info(f"Error in SQL createCaseHistory :- {traceback.format_exc()}")
        finally:
            cursor.close()
            conn.close()
            return self.createCaseHistoryDetails(getlastid)

    def createCaseHistoryDetails(self, getlastid):
        try:
            conn = mysql.connect()
            cursor = conn.cursor(pymysql.cursors.DictCursor)
            sqlselectquery = f"SELECT `id` FROM `case_history` where `court_case_id`={getlastid}"
            cursor.execute(sqlselectquery)
            case_history_ids_list = cursor.fetchall()
            sqlqueryinsert = "INSERT INTO `case_history_details`(`court_case_id`,`case_history_id`,`case_no`,`diary_no`,`listing_date`,`court_no`,`coram`,`proceeding_summary`,`stage_of_case`) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            for i in self.tribunals_case_history_details:
                bindData = (
                    getlastid,
                    case_history_ids_list[0].get('id'),
                    i.get('case_no', None),
                    i.get('diary_no', None),
                    i.get('listing_date', None),
                    i.get('court_no', None),
                    i.get('coram', None),
                    i.get('proceeding_summary', None),
                    i.get('stage_of_case', None)
                )
                cursor.execute(sqlqueryinsert, bindData)
                case_history_ids_list.pop(0)
            conn.commit()
        except:
            logger.info(f"Error in SQL createCaseHistoryDetails :- {traceback.format_exc()}")
        finally:
            cursor.close()
            conn.close()
            return self.createOrderHistory(getlastid)

    def createOrderHistory(self, getlastid):
        try:
            conn = mysql.connect()
            cursor = conn.cursor(pymysql.cursors.DictCursor)
            sqlqueryinsert = "INSERT INTO `order_history`(`court_case_id`,`sr_no`,`order_date`,`order_type`,`view`,`orders_url`) VALUES (%s,%s,%s,%s,%s,%s)"
            for i in self.tribunals_order_history:
                bindData = (
                    getlastid,
                    i.get('sr_no', None),
                    i.get('order_date', None),
                    i.get('order_type', None),
                    i.get('view', None),
                    i.get('orders_url', None)
                )
                cursor.execute(sqlqueryinsert, bindData)
            conn.commit()
        except:
            logger.info(f"Error in SQL createOrderHistory :- {traceback.format_exc()}")
        finally:
            cursor.close()
            conn.close()
            return self.createIAsOtherApplication(getlastid)

    def createIAsOtherApplication(self, getlastid):
        try:
            conn = mysql.connect()
            cursor = conn.cursor(pymysql.cursors.DictCursor)
            sqlqueryinsert = "INSERT INTO `ias_other_application`(`court_case_id`,`sr_no`,`filing_no`,`case_no`,`date_of_filing`,`registration_date`,`status`) VALUES (%s,%s,%s,%s,%s,%s,%s)"
            for i in self.tribunals_ias_other_application:
                bindData = (
                    getlastid,
                    i.get('sr_no', None),
                    i.get('filing_no', None),
                    i.get('case_no', None),
                    i.get('date_of_filing', None),
                    i.get('registration_date', None),
                    i.get('status', None)
                )
                cursor.execute(sqlqueryinsert, bindData)
            conn.commit()
        except:
            logger.info(f"Error in SQL createIAsOtherApplication :- {traceback.format_exc()}")
        finally:
            cursor.close()
            conn.close()
            return self.createConnectedCases(getlastid)

    def createConnectedCases(self, getlastid):
        try:
            conn = mysql.connect()
            cursor = conn.cursor(pymysql.cursors.DictCursor)
            sqlqueryinsert = "INSERT INTO `connected_cases`(`court_case_id`,`sr_no`,`filing_no`,`case_no`,`date_of_filing`,`registration_date`,`status`) VALUES (%s,%s,%s,%s,%s,%s,%s)"
            for i in self.tribunals_connected_cases:
                bindData = (
                    getlastid,
                    i.get('sr_no', None),
                    i.get('filing_no', None),
                    i.get('case_no', None),
                    i.get('date_of_filing', None),
                    i.get('registration_date', None),
                    i.get('status', None)
                )
                cursor.execute(sqlqueryinsert, bindData)
            conn.commit()
        except:
            logger.info(f"Error in SQL createConnectedCases :- {traceback.format_exc()}")
        finally:
            cursor.close()
            conn.close()
            return True

