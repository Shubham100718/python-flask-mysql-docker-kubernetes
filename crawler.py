import requests, traceback, logging
from timestamp_convertor import timestamp_convertor2
from listing_details_crawler import get_listing_details_table
from orders_crawler import get_orders_pdf
import urllib3
urllib3.disable_warnings()


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s:%(levelname)s:%(name)s:%(message)s')
file_handler = logging.FileHandler('tribunals.log')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

session = requests.session()

case_details_table = []
applicant_name_table = []
respondant_name_table = []
applicant_legal_representative_table = []
respondent_legal_representative_table = []
first_hearing_details_table = []
last_hearing_details_table = []
next_hearing_details_table = []
case_history_table = []
case_history_details_table = []
order_history_table = []
ias_other_application_table = []
connected_cases_table = []

# input_data = {
#     "location": "delhi",
#     "filing_no": "9910110001532018"
# }

def get_tribunals_detail_data(input_data, token, xsrf_token, laravel_session):
    try:
        filing_no = input_data.get('filing_no')
        bench_name = input_data.get('location')

        final_page_payload = f"search_type=view_details&filing_no={filing_no}&_token={token}&bench_name={bench_name}"
        
        final_page_headers = {
            'Accept': 'text/plain, */*; q=0.01',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'en-US,en;q=0.9,hi;q=0.8',
            'Connection': 'keep-alive',
            'Content-Length': f'{len(final_page_payload)}',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Cookie': f'_ga=GA1.3.1468851884.1678795714; _gid=GA1.3.347674307.1678795714; XSRF-TOKEN={xsrf_token}; laravel_session={laravel_session}',
            'Host': 'nclat.nic.in',
            'Origin': 'https://nclat.nic.in',
            'Referer': 'https://nclat.nic.in/display-board/cases',
            'sec-ch-ua': '"Chromium";v="110", "Not A(Brand";v="24", "Google Chrome";v="110"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36',
            'X-Requested-With': 'XMLHttpRequest'
        }
        final_page_response = session.post("https://nclat.nic.in/display-board/view_details", headers=final_page_headers, data=final_page_payload, verify=False)
        if final_page_response.status_code==200:
            logger.info('we have got final page response successfully')
        else:
            logger.info('we have not got proper final page response')

        detail_data_list = final_page_response.json().get('data')

        case_details_data_list = detail_data_list.get('case_details')
        if case_details_data_list == []:
            logger.info(f'No data found for {input_data}')
            return case_details_table, applicant_name_table, respondant_name_table, applicant_legal_representative_table, respondent_legal_representative_table, first_hearing_details_table, last_hearing_details_table, next_hearing_details_table, case_history_table, case_history_details_table, order_history_table, ias_other_application_table, connected_cases_table
 
        for case_details_data in case_details_data_list:
            filing_no = case_details_data.get('filing_no')
            date_of_filing_format = case_details_data.get('date_of_filing')
            if date_of_filing_format:
                date_of_filing = timestamp_convertor2(date_of_filing_format)
            else:
                date_of_filing = date_of_filing_format
            case_no = case_details_data.get('case_type') +'/'+ case_details_data.get('case_no') +'/'+ case_details_data.get('case_year')
            registration_date_format = case_details_data.get('registration_date')
            if registration_date_format:
                registration_date = timestamp_convertor2(registration_date_format)
            else:
                registration_date = registration_date_format
            if case_details_data.get('status')=='P':
                status = 'Pending'
            elif case_details_data.get('status')=='D':
                status = 'Disposed'
            data = {
                'filing_no': filing_no,
                'date_of_filing': date_of_filing,
                'case_no': case_no,
                'registration_date': registration_date,
                'status': status,
            }
            case_details_table.append(data)
        logger.info('case_details_table save successfully')


        party_details_data_list = detail_data_list.get('party_details')
        applicant_name_data = party_details_data_list.get('applicant_name')
        applicant_data = {}
        applicant_data['applicant_name'] = [i.get('name').strip() for i in applicant_name_data]
        applicant_name_table.append(applicant_data)
        logger.info('applicant_name_table save successfully')

        respondant_name_data = party_details_data_list.get('respondant_name')
        respondant_data = {}
        respondant_data['respondant_name'] = [i.get('name').strip() for i in respondant_name_data]
        respondant_name_table.append(respondant_data)
        logger.info('respondant_name_table save successfully')


        legal_representative_data_list = detail_data_list.get('legal_representative')
        applicant_legal_representative_name_data = legal_representative_data_list.get('applicant_legal_representative_name')
        applicant_legal_representative_data = {}
        applicant_legal_representative_data['applicant_legal_representative_name'] = [i.strip() for i in applicant_legal_representative_name_data]
        applicant_legal_representative_table.append(applicant_legal_representative_data)
        logger.info('applicant_legal_representative_table save successfully')

        respondent_legal_representative_name_data = legal_representative_data_list.get('respondent_legal_representative_name')
        respondent_legal_representative_data = {}
        respondent_legal_representative_data['respondent_legal_representative_name'] = [i.strip() for i in respondent_legal_representative_name_data]
        respondent_legal_representative_table.append(respondent_legal_representative_data)
        logger.info('respondent_legal_representative_table save successfully')


        first_hearing_details_data = detail_data_list.get('first_hearing_details')
        if first_hearing_details_data!=[]:
            court_no = first_hearing_details_data.get('court_no')
            hearing_date_format = first_hearing_details_data.get('hearing_date')
            if hearing_date_format:
                hearing_date = timestamp_convertor2(hearing_date_format)
            else:
                hearing_date = hearing_date_format
            coram = first_hearing_details_data.get('coram')
            stage_of_case = first_hearing_details_data.get('stage_of_case')
            data = {
                'court_no': court_no,
                'hearing_date': hearing_date,
                'coram': coram,
                'stage_of_case': stage_of_case
            }
            first_hearing_details_table.append(data)
        logger.info('first_hearing_details_table save successfully')


        last_hearing_details_data = detail_data_list.get('last_hearing_details')
        if last_hearing_details_data!=[]:
            court_no = last_hearing_details_data.get('court_no')
            hearing_date_format = last_hearing_details_data.get('hearing_date')
            if hearing_date_format:
                hearing_date = timestamp_convertor2(hearing_date_format)
            else:
                hearing_date = hearing_date_format
            coram = last_hearing_details_data.get('coram')
            stage_of_case = last_hearing_details_data.get('stage_of_case')
            data = {
                'court_no': court_no,
                'hearing_date': hearing_date,
                'coram': coram,
                'stage_of_case': stage_of_case
            }
            last_hearing_details_table.append(data)
        logger.info('last_hearing_details_table save successfully')


        next_hearing_details_data = detail_data_list.get('next_hearing_details')
        if next_hearing_details_data!=[]:
            hearing_date_format = next_hearing_details_data.get('hearing_date')
            if hearing_date_format:
                hearing_date = timestamp_convertor2(hearing_date_format)
            else:
                hearing_date = hearing_date_format
            court_no = next_hearing_details_data.get('court_no')
            proceedings_summary = next_hearing_details_data.get('coram')
            stage_of_case = next_hearing_details_data.get('stage_of_case')
            data = {
                'hearing_date': hearing_date,
                'court_no': court_no,
                'proceedings_summary': proceedings_summary,
                'stage_of_case': stage_of_case
            }
            next_hearing_details_table.append(data)
        logger.info('next_hearing_details_table save successfully')


        case_history_data_list = detail_data_list.get('case_history')
        for count, case_history_data in enumerate(case_history_data_list, start=1):
            sr_no = count
            hearing_date_format = case_history_data.get('hearing_date')
            if hearing_date_format:
                hearing_date = timestamp_convertor2(hearing_date_format)
            else:
                hearing_date = hearing_date_format
            court_no = case_history_data.get('court_no')
            purpose = case_history_data.get('purpose')
            action = 'View'
            data = {
                'sr_no': sr_no,
                'hearing_date': hearing_date,
                'court_no': court_no,
                'purpose': purpose,
                'action': action
            }
            case_history_table.append(data)
            case_history_details_table.append(get_listing_details_table(session, hearing_date_format, filing_no, bench_name, token, xsrf_token, laravel_session))
        logger.info('case_history_table save successfully')
        logger.info('case_history_details_table save successfully')


        order_history_data_list = detail_data_list.get('order_history')
        for count, order_history_data in enumerate(order_history_data_list, start=1):
            sr_no = count
            order_date_format = order_history_data.get('order_date')
            if order_date_format:
                order_date = timestamp_convertor2(order_date_format)
            else:
                order_date = order_date_format
            order_type_symbol = order_history_data.get('order_type')
            if order_type_symbol=='D':
                order_type = 'Daily Order'
            elif order_type_symbol=='J':
                order_type = 'Final Order / Judgement'
            view = 'Download'
            orders_filename = get_orders_pdf(session, bench_name, filing_no, order_date_format, order_type_symbol, token, xsrf_token, laravel_session)
            data = {
                'sr_no': sr_no,
                'order_date': order_date,
                'order_type': order_type,
                'view': view,
                'orders_url': orders_filename
            }
            order_history_table.append(data)
        logger.info('order_history_table save successfully')


        ias_other_application_data_list = detail_data_list.get('ias_other_application')
        for count, ias_other_application_data in enumerate(ias_other_application_data_list, start=1):
            sr_no = count
            filing_no = ias_other_application_data.get('filing_no')
            case_no = ias_other_application_data.get('case_no')
            date_of_filing_format = ias_other_application_data.get('filing_date')
            if date_of_filing_format:
                date_of_filing = timestamp_convertor2(date_of_filing_format)
            else:
                date_of_filing = date_of_filing_format
            registration_date_format = ias_other_application_data.get('registration_date')
            if registration_date_format:
                registration_date = timestamp_convertor2(registration_date_format)
            else:
                registration_date = registration_date_format
            if ias_other_application_data.get('status')=='P':
                status = 'Pending'
            elif ias_other_application_data.get('status')=='D':
                status = 'Disposed'
            data = {
                'sr_no': sr_no,
                'filing_no': filing_no,
                'case_no': case_no,
                'date_of_filing': date_of_filing,
                'registration_date': registration_date,
                'status': status
            }
            ias_other_application_table.append(data)
        logger.info('ias_other_application_table save successfully')


        connected_cases_data_list = detail_data_list.get('connected_cases')
        for count, connected_cases_data in enumerate(connected_cases_data_list, start=1):
            sr_no = count
            filing_no = connected_cases_data.get('filing_no')
            case_no = connected_cases_data.get('case_no')
            date_of_filing_format = ias_other_application_data.get('filing_date')
            if date_of_filing_format:
                date_of_filing = timestamp_convertor2(date_of_filing_format)
            else:
                date_of_filing = date_of_filing_format
            registration_date_format = ias_other_application_data.get('registration_date')
            if registration_date_format:
                registration_date = timestamp_convertor2(registration_date_format)
            else:
                registration_date = registration_date_format
            if connected_cases_data.get('status')=='P':
                status = 'Pending'
            elif connected_cases_data.get('status')=='D':
                status = 'Disposed'
            data = {
                'sr_no': sr_no,
                'filing_no': filing_no,
                'case_no': case_no,
                'date_of_filing': date_of_filing,
                'registration_date': registration_date,
                'status': status
            }
            connected_cases_table.append(data)
        logger.info('connected_cases_table save successfully')

        return case_details_table, applicant_name_table, respondant_name_table, applicant_legal_representative_table, respondent_legal_representative_table, first_hearing_details_table, last_hearing_details_table, next_hearing_details_table, case_history_table, case_history_details_table, order_history_table, ias_other_application_table, connected_cases_table

    except Exception as e:
        logger.info(f"Error in get_tribunals_detail_data :- {traceback.format_exc()}")


# print(get_tribunals_detail_data(input_data, "U4txk3uhMdDVEbITXFdMuIppsTHrIuApCEmTNNb5", "eyJpdiI6Im9RMDNCL0VLTWdJMGNLSDhOd0d2SVE9PSIsInZhbHVlIjoiM2pSU3lMOXBwZ2lLNUZlSEp2NnJTQWx6M1Jyc3UyMHpoYmJ6bGFKNFdiRFNOb1JKME9ONDRUd3FxUVVqYStKRFRkTU1QVUFKa0tWclB1R0dDRzI2VDVhUzlyTGs5anFSRXRDMTZBMHpFREV5dE11QXc0YS9UUlFHK1NpRElnTmkiLCJtYWMiOiI1ZjdjNzM4ZmQ4ZWVjNTUzZGJhNTc1ZDAyNjhiYzFmZTEzMzEzODc5M2Q5MGIwNGI0NmJkMGQ4ZjZkOWRiYmMwIiwidGFnIjoiIn0%3D", "eyJpdiI6InZTY1gremZtaHJ4QUdYYVhUT3dJN3c9PSIsInZhbHVlIjoiUzJ5N1ZQOTFGbVpTa2ZSUEx5VCtpb1NLaHdEcHQ1cXRqM1ZMYW9EVWE2L3o3VzRHR1B0TTIwLzcyNk1IenRqaC9HTGdlUE1lVGgwZTk5bGtKb0huaXArek9WNjhhL0EwaGtiaTh6dkx0cTdXRWlCNm1pTFk1T3NNRENyQ2MvakgiLCJtYWMiOiIzMTM3NzFjNDMzMjEyMmMyNmM1OTk0N2MzMzg1ZWNlZWEzYjZkZmU4NDgwZTNhZjUwNjRjMDQ4OWMwMDFlZjVjIiwidGFnIjoiIn0%3D"))

