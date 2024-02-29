import logging
import traceback
from app import app
from flask import jsonify, request
from case_crawler import get_tribunals_court_cases_data, get_tribunals_token_values
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
        _case_year = _json.get('case_year', None)

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
            
        court_type_id = 8
        if case_list_data != []:
            if case_list_data != None:
                if case_list_data[0].get('message') != 'Server error, Please try after some time!':
                    if request.method == 'POST':
                        case_list_table_data = TribunalsCaseListInsert(court_type_id, _search_by, _location, _case_type, _case_status, _party_type, _party_name, _filing_no, _case_number, _advocate_name, _case_year, case_list_data).createTribunalsCaseList()
                        response = jsonify({
                            'status': 200,
                            'message': 'Fetched NCLAT Tribunals Case List succesfully!',
                            'partyName': case_list_table_data
                        })
                        return response
                    else:
                        return showMessage()
                else:
                    return serverError()
            else:
                return serverError()
        else:
            return dataNotFound()
    except:
        logger.info(traceback.format_exc())


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
            security_tokens = get_tribunals_token_values(input_data)
            if security_tokens != None:
                _token = security_tokens[0]
                _xsrf_token = security_tokens[1]
                _laravel_session = security_tokens[2]
                tribunals_data = get_tribunals_detail_data(input_data, _token, _xsrf_token, _laravel_session)
                if tribunals_data != None:
                    if tribunals_data != []:
                        getlastid, case_details_table_data = TribunalsInsert(court_type_id, _status, _location, tribunals_data).createCaseDetails()
                        response = jsonify({
                            'status': 200,
                            'case_id': getlastid,
                            'message': 'Fetched NCLAT Tribunals data succesfully!',
                            'partyName': case_details_table_data
                        })
                        return response
                    else:
                        return dataNotFound()
                else:
                    return serverError()
            else:
                return serverError()
        else:
            return showMessage()
    except:
        logger.info(traceback.format_exc())


def showMessage():
    message = {
        'status': 400,
        'message': 'Invalid request!'
    }
    response = jsonify(message)
    return response

def dataNotFound():
    message = {
        'status': 404,
        'message': 'Oops, data not found!'
    }
    response = jsonify(message)
    return response

def serverError():
    message = {
        'status': 500,
        'message': 'Server error, Please try after some time!'
    }
    response = jsonify(message)
    return response


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=9000, debug=True)

