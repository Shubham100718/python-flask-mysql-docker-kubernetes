import requests
import traceback
import logging
from threading import Thread
from timestamp_convertor import timestamp_convertor
from listing_details_crawler import get_listing_details_table
from orders_crawler import get_orders_pdf
import urllib3
urllib3.disable_warnings()


session = requests.Session()
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s:%(levelname)s:%(name)s:%(message)s')
file_handler = logging.FileHandler('tribunals.log')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

# input_data = {
#     "location": "delhi",
#     "filing_no": "9910110083542022"
# }

def get_tribunals_soup_data(input_data, token, xsrf_token, laravel_session):
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
        final_page_response = session.post("https://nclat.nic.in/display-board/view_details",
                                        headers=final_page_headers, data=final_page_payload, verify=False)
        
        if final_page_response.status_code != 200:
            logger.info('we have not got proper final page response')

        detail_data_list = final_page_response.json().get('data')

        if detail_data_list.get('case_details') != []:

            return detail_data_list, filing_no, bench_name
        
        else:
            return []
    except:
        logger.info(f"Error in get_tribunals_soup_data :- {traceback.format_exc()}")


def get_tribunals_case_details_data(detail_data_list):
    try:
        case_details_table = []
        case_details_table.clear()
        case_details_data_list = detail_data_list.get('case_details')
        for case_details_data in case_details_data_list:
            filing_no = case_details_data.get('filing_no')
            date_of_filing_format = case_details_data.get('date_of_filing')
            if date_of_filing_format:
                date_of_filing = timestamp_convertor(date_of_filing_format)
            else:
                date_of_filing = ''
            case_no = case_details_data.get('case_type') +'/'+ case_details_data.get('case_no') +'/'+ case_details_data.get('case_year')
            registration_date_format = case_details_data.get('registration_date')
            if registration_date_format:
                registration_date = timestamp_convertor(registration_date_format)
            else:
                registration_date = ''
            if case_details_data.get('status')=='P':
                status = 'Open'
            elif case_details_data.get('status')=='D':
                status = 'Close'
            data = {
                'filing_no': filing_no,
                'date_of_filing': date_of_filing,
                'case_no': case_no,
                'registration_date': registration_date,
                'status': status,
            }
            case_details_table.append(data)
        # print(case_details_table)
        return case_details_table
    except:
        logger.info(f"Error in get_tribunals_case_details_data :- {traceback.format_exc()}")


def get_tribunals_party_details_data(detail_data_list):
    try:
        applicant_name_table = []
        respondant_name_table = []
        applicant_name_table.clear()
        respondant_name_table.clear()
        party_details_data_list = detail_data_list.get('party_details')
        applicant_name_data = party_details_data_list.get('applicant_name')
        applicant_data = {}
        applicant_data['applicant_name'] = [i.get('name').strip() for i in applicant_name_data]
        applicant_name_table.append(applicant_data)
        respondant_name_data = party_details_data_list.get('respondant_name')
        respondant_data = {}
        respondant_data['respondant_name'] = [i.get('name').strip() for i in respondant_name_data]
        respondant_name_table.append(respondant_data)
        # print(applicant_name_table)
        # print(respondant_name_table)
        return applicant_name_table, respondant_name_table
    except:
        logger.info(f"Error in get_tribunals_party_details_data :- {traceback.format_exc()}")


def get_tribunals_legal_representative_data(detail_data_list):
    try:
        applicant_legal_representative_table = []
        respondent_legal_representative_table = []
        applicant_legal_representative_table.clear()
        respondent_legal_representative_table.clear()
        legal_representative_data_list = detail_data_list.get('legal_representative')
        applicant_legal_representative_name_data = legal_representative_data_list.get('applicant_legal_representative_name')
        applicant_legal_representative_data = {}
        applicant_legal_representative_data['applicant_legal_representative_name'] = [i.strip() for i in applicant_legal_representative_name_data]
        applicant_legal_representative_table.append(applicant_legal_representative_data)
        respondent_legal_representative_name_data = legal_representative_data_list.get('respondent_legal_representative_name')
        respondent_legal_representative_data = {}
        respondent_legal_representative_data['respondent_legal_representative_name'] = [i.strip() for i in respondent_legal_representative_name_data]
        respondent_legal_representative_table.append(respondent_legal_representative_data)
        # print(applicant_legal_representative_table)
        # print(respondent_legal_representative_table)
        return applicant_legal_representative_table, respondent_legal_representative_table
    except:
        logger.info(f"Error in get_tribunals_legal_representative_data :- {traceback.format_exc()}")


def get_tribunals_first_hearing_details_data(detail_data_list):
    try:
        first_hearing_details_table = []
        first_hearing_details_table.clear()
        first_hearing_details_data = detail_data_list.get('first_hearing_details')
        if first_hearing_details_data!=[]:
            court_no = first_hearing_details_data.get('court_no')
            hearing_date_format = first_hearing_details_data.get('hearing_date')
            if hearing_date_format:
                hearing_date = timestamp_convertor(hearing_date_format)
            else:
                hearing_date = ''
            coram = first_hearing_details_data.get('coram')
            stage_of_case = first_hearing_details_data.get('stage_of_case')
            data = {
                'court_no': court_no,
                'hearing_date': hearing_date,
                'coram': coram,
                'stage_of_case': stage_of_case
            }
            first_hearing_details_table.append(data)
        # print(first_hearing_details_table)
        return first_hearing_details_table
    except:
        logger.info(f"Error in get_tribunals_first_hearing_details_data :- {traceback.format_exc()}")


def get_tribunals_last_hearing_details_data(detail_data_list):
    try:
        last_hearing_details_table = []
        last_hearing_details_table.clear()
        last_hearing_details_data = detail_data_list.get('last_hearing_details')
        if last_hearing_details_data!=[]:
            court_no = last_hearing_details_data.get('court_no')
            hearing_date_format = last_hearing_details_data.get('hearing_date')
            if hearing_date_format:
                hearing_date = timestamp_convertor(hearing_date_format)
            else:
                hearing_date = ''
            coram = last_hearing_details_data.get('coram')
            stage_of_case = last_hearing_details_data.get('stage_of_case')
            data = {
                'court_no': court_no,
                'hearing_date': hearing_date,
                'coram': coram,
                'stage_of_case': stage_of_case
            }
            last_hearing_details_table.append(data)
        # print(last_hearing_details_table)
        return last_hearing_details_table
    except:
        logger.info(f"Error in get_tribunals_last_hearing_details_data :- {traceback.format_exc()}")


def get_tribunals_next_hearing_details_data(detail_data_list):
    try:
        next_hearing_details_table = []
        next_hearing_details_table.clear()
        next_hearing_details_data = detail_data_list.get('next_hearing_details')
        if next_hearing_details_data!=[]:
            hearing_date_format = next_hearing_details_data.get('hearing_date')
            if hearing_date_format:
                hearing_date = timestamp_convertor(hearing_date_format)
            else:
                hearing_date = ''
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
        # print(next_hearing_details_table)
        return next_hearing_details_table
    except:
        logger.info(f"Error in get_tribunals_next_hearing_details_data :- {traceback.format_exc()}")


def get_tribunals_case_history_data(detail_data_list, filing_no, bench_name, token, xsrf_token, laravel_session):
    try:
        case_history_table = []
        case_history_details_table = []
        case_history_table.clear()
        case_history_details_table.clear()
        case_history_data_list = detail_data_list.get('case_history')
        for count, case_history_data in enumerate(case_history_data_list, start=1):
            sr_no = count
            hearing_date_format = case_history_data.get('hearing_date')
            if hearing_date_format:
                hearing_date = timestamp_convertor(hearing_date_format)
            else:
                hearing_date = ''
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
        # print(case_history_table)
        # print(case_history_details_table)
        return case_history_table, case_history_details_table
    except:
        logger.info(f"Error in get_tribunals_case_history_data :- {traceback.format_exc()}")


def get_tribunals_order_history_data(detail_data_list, filing_no, bench_name, token, xsrf_token, laravel_session):
    try:
        order_history_table = []
        order_history_table.clear()
        order_history_data_list = detail_data_list.get('order_history')
        for count, order_history_data in enumerate(order_history_data_list, start=1):
            sr_no = count
            order_date_format = order_history_data.get('order_date')
            if order_date_format:
                order_date = timestamp_convertor(order_date_format)
            else:
                order_date = ''
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
        # print(order_history_table)
        return order_history_table
    except:
        logger.info(f"Error in get_tribunals_order_history_data :- {traceback.format_exc()}")


def get_tribunals_ias_other_application_data(detail_data_list):
    try:
        ias_other_application_table = []
        ias_other_application_table.clear()
        ias_other_application_data_list = detail_data_list.get('ias_other_application')
        for count, ias_other_application_data in enumerate(ias_other_application_data_list, start=1):
            sr_no = count
            filing_no = ias_other_application_data.get('filing_no')
            case_no = ias_other_application_data.get('case_no')
            date_of_filing_format = ias_other_application_data.get('filing_date')
            if date_of_filing_format:
                date_of_filing = timestamp_convertor(date_of_filing_format)
            else:
                date_of_filing = ''
            registration_date_format = ias_other_application_data.get('registration_date')
            if registration_date_format:
                registration_date = timestamp_convertor(registration_date_format)
            else:
                registration_date = ''
            if ias_other_application_data.get('status')=='P':
                status = 'Open'
            elif ias_other_application_data.get('status')=='D':
                status = 'Close'
            data = {
                'sr_no': sr_no,
                'filing_no': filing_no,
                'case_no': case_no,
                'date_of_filing': date_of_filing,
                'registration_date': registration_date,
                'status': status
            }
            ias_other_application_table.append(data)
        # print(ias_other_application_table)
        return ias_other_application_table
    except:
        logger.info(f"Error in get_tribunals_ias_other_application_data :- {traceback.format_exc()}")


def get_tribunals_connected_cases_data(detail_data_list):
    try:
        connected_cases_table = []
        connected_cases_table.clear()
        connected_cases_data_list = detail_data_list.get('connected_cases')
        for count, connected_cases_data in enumerate(connected_cases_data_list, start=1):
            sr_no = count
            filing_no = connected_cases_data.get('filing_no')
            case_no = connected_cases_data.get('case_no')
            date_of_filing_format = connected_cases_data.get('filing_date')
            if date_of_filing_format:
                date_of_filing = timestamp_convertor(date_of_filing_format)
            else:
                date_of_filing = ''
            registration_date_format = connected_cases_data.get('registration_date')
            if registration_date_format:
                registration_date = timestamp_convertor(registration_date_format)
            else:
                registration_date = ''
            if connected_cases_data.get('status')=='P':
                status = 'Open'
            elif connected_cases_data.get('status')=='D':
                status = 'Close'
            data = {
                'sr_no': sr_no,
                'filing_no': filing_no,
                'case_no': case_no,
                'date_of_filing': date_of_filing,
                'registration_date': registration_date,
                'status': status
            }
            connected_cases_table.append(data)
        # print(connected_cases_table)
        return connected_cases_table
    except:
        logger.info(f"Error in get_tribunals_connected_cases_data :- {traceback.format_exc()}")


# s1 = time.time()
def get_tribunals_detail_data(input_data, token, xsrf_token, laravel_session):
    try:
        detail_data_list, filing_no, bench_name = get_tribunals_soup_data(input_data, token, xsrf_token, laravel_session)
        if detail_data_list == []:
            return []

        class ThreadWithReturnValue(Thread):
            def __init__(self, group=None, target=None, name=None,
                        args=(), kwargs={}, Verbose=None):
                Thread.__init__(self, group, target, name, args, kwargs)
                self._return = None
            def run(self):
                if self._target is not None:
                    self._return = self._target(*self._args,
                                                        **self._kwargs)
            def join(self, *args):
                Thread.join(self, *args)
                return self._return

        thread1 = ThreadWithReturnValue(target=get_tribunals_case_details_data, args=[detail_data_list])
        thread2 = ThreadWithReturnValue(target=get_tribunals_party_details_data, args=[detail_data_list])
        thread3 = ThreadWithReturnValue(target=get_tribunals_legal_representative_data, args=[detail_data_list])
        thread4 = ThreadWithReturnValue(target=get_tribunals_first_hearing_details_data, args=[detail_data_list])
        thread5 = ThreadWithReturnValue(target=get_tribunals_last_hearing_details_data, args=[detail_data_list])
        thread6 = ThreadWithReturnValue(target=get_tribunals_next_hearing_details_data, args=[detail_data_list])
        thread7 = ThreadWithReturnValue(target=get_tribunals_case_history_data, args=[detail_data_list,filing_no,bench_name,token,xsrf_token,laravel_session])
        thread8 = ThreadWithReturnValue(target=get_tribunals_order_history_data, args=[detail_data_list,filing_no,bench_name,token,xsrf_token,laravel_session])
        thread9 = ThreadWithReturnValue(target=get_tribunals_ias_other_application_data, args=[detail_data_list])
        thread10 = ThreadWithReturnValue(target=get_tribunals_connected_cases_data, args=[detail_data_list])
        thread7.start()
        thread8.start()
        thread2.start()
        thread3.start()
        thread1.start()
        thread4.start()
        thread5.start()
        thread6.start()
        thread9.start()
        thread10.start()
        thread1.join()
        thread2.join()
        thread3.join()
        thread4.join()
        thread5.join()
        thread6.join()
        thread7.join()
        thread8.join()
        thread9.join()
        thread10.join()

        return [thread1.join(),thread2.join(),thread3.join(),thread4.join(),thread5.join(),thread6.join(),thread7.join(),thread8.join(),thread9.join(),thread10.join()]

    except:
        logger.info(f"Error in get_tribunals_detail_data :- {traceback.format_exc()}")
    

# print(get_tribunals_detail_data(input_data, "IkDTXEPwfnt0WCXh9F2ALvQJTntvb8sJJEopKZc6", "eyJpdiI6IjgvbU1FYjhybkZPRGNFVHZTeXZQOUE9PSIsInZhbHVlIjoiQnArTEZRMFRhb1NXb084WWgzRUcrbmNSaUdLRXBPcGRnNEQveTk5ak43UXpTTmNUSzE3SEJxNGQyNkNUc3RqaEtsaG92RnRKQ1VTL0VKYnJpR0JpYWxqZW45T1YxdXdiM1FoWnNuVDkzMm04dDVUQUhPeTlkemtJaHhvVDlIVXYiLCJtYWMiOiI0MWZjN2M0NzM0Y2UyNWIwZmUxNzBmYWVjMmIyNTQyOWM4ZWIzYWY5ZjlmZWJmYjkzMGEwMTQ3YWY2ZDM2ZWNjIiwidGFnIjoiIn0%3D", "eyJpdiI6IklVZlc0Zjd5ckZkZWp5U0oyTzJ4MFE9PSIsInZhbHVlIjoiOWRrWkgyUDcwaUxhQ0VNNGZPemEvcVgxTFBCS2QvSGY1bUwrT3RFc1NBc285S2ZBT2dqL2M0SXczaExQMVFhQkxLb1RWeU8vcS9ScElvaDdOL2pyNDF0azlCSkZkVm52Y1V5WHMwdUpDQVVxa3lBT3hQdVl0YkZyaVFFQWYrMWsiLCJtYWMiOiIwNzZjZTY5NzRkMGFlMDc4MDg1NWVjNGM1MDExOGJlMjNjNTAyNzZiYTczMTY2ZGViY2VhZjUwOTIyYmQzNzY3IiwidGFnIjoiIn0%3D"))
# print(time.time()-s1)

