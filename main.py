import logging, pymysql, traceback
from app import app
from config import mysql
from flask import jsonify
from flask import request
from case_crawler import get_tribunals_court_cases_data
from crawler import get_tribunals_detail_data
from courtClassCaseList import TribunalsCaseListInsert
from courtClassForDetailData import TribunalsInsert


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s:%(levelname)s:%(name)s:%(message)s')
file_handler = logging.FileHandler('tribunals.log')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)


@app.route('/tribunals/caselist', methods=['POST'])
def tribunals_caselist():
    try:
        _json = request.json
        _search_by = _json['search_by']
        _location = _json['location']
        _case_type = _json.get('case_type', None)
        _case_status = _json.get('case_status', None)
        _party_type = _json.get('party_type', None)
        _party_name = _json.get('party_name', None)
        _filing_no = _json.get('filing_no', None)
        _case_number = _json.get('case_number', None)
        _advocate_name = _json.get('advocate_name', None)
        _case_year = _json['case_year']

        input_data = {
            'search_by': _search_by,
            'location': _location,
            'case_type': _case_type,
            'case_status': _case_status,
            'party_type': _party_type,
            'party_name': _party_name,
            'filing_no': _filing_no,
            'case_number': _case_number,
            'advocate_name': _advocate_name,
            'case_year': _case_year
        }
        case_list_data = get_tribunals_court_cases_data(input_data)
        if case_list_data != []:
            logger.info('we have got case_list_data successfully')
            
        court_type_id = 8
        if case_list_data != []:
            if request.method == 'POST':
                TribunalsCaseListInsert(court_type_id, _search_by, _location, _advocate_name, _party_name, _party_type, _case_type, _case_number, _case_year, _case_status, case_list_data).createTribunalsCaseList()

                respone = jsonify({'meaasge': 'Fetched NCLAT Tribunals Case List succesfully!'})
                respone.status_code = 200
                return respone
            else:
                return showMessage()
        else:
            return dataNotFound()

    except:
        logger.info(f"Error in tribunals_caselist :- {traceback.format_exc()}")


@app.route('/tribunals/detaildata', methods=['POST'])
def create_employee():
    try:
        _json = request.json
        _location = _json['location']
        _filing_no = _json['filing_no']
        _status = 1
        court_type_id = 8

        input_data = {
            'location': _location,
            'filing_no': _filing_no
        }

        if request.method == 'POST':
            conn = mysql.connect()
            cursor = conn.cursor(pymysql.cursors.DictCursor)
            sqlqueryselect = f"SELECT `token`,`xsrf_token`,`laravel_session` FROM `case_list` where `location`='{_location}' and `filing_no`={_filing_no}"
            cursor.execute(sqlqueryselect)
            security_tokens = cursor.fetchone()
            _token = security_tokens.get('token')
            _xsrf_token = security_tokens.get('xsrf_token')
            _laravel_session = security_tokens.get('laravel_session')
            conn.commit()
            tribunals_data = get_tribunals_detail_data(input_data, _token, _xsrf_token, _laravel_session)
            if tribunals_data != None:
                getlastid = TribunalsInsert(court_type_id, _status, _location, _token, _xsrf_token, _laravel_session, tribunals_data).createCaseDetails()
            else:
                return dataNotFound()

            respone = jsonify(
                {'case_id': getlastid, 'meaasge': 'Fetched NCLAT Tribunals data succesfully!'})

            return respone
        else:
            return showMessage()

    except:
        logger.info(f"Error in create_employee :- {traceback.format_exc()}")


@app.errorhandler(404)
def showMessage(error=None):
    message = {
        'status': 404,
        'message': 'Record not found: ' + request.url,
    }
    respone = jsonify(message)
    respone.status_code = 404
    return respone


@app.errorhandler(500)
def dataNotFound(error=None):
    message = {
        'status': 'Oops, data not found!'
    }
    respone = jsonify(message)
    respone.status_code = 500
    return respone


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=9007, debug=True)

