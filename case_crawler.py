import requests, traceback, logging
from bs4 import BeautifulSoup
from timestamp_convertor import timestamp_convertor
import urllib3
urllib3.disable_warnings()


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s:%(levelname)s:%(name)s:%(message)s')
file_handler = logging.FileHandler('tribunals.log')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

session = requests.session()

court_cases_table = []

# input_data = {
#     "search_by": "1",
#     "location": "delhi",
#     "case_type": "36",
#     "case_status": "",
#     "party_type": "",
#     "party_name": "",
#     "filing_no": "",
#     "case_number": "1",
#     "advocate_name": "",
#     "case_year": "2023"
# }

def get_cookies_data():
    starting_page = session.get("https://nclat.nic.in/display-board/cases", verify=False)
    cookies_data = session.cookies.get_dict()
    return cookies_data

def get_tribunals_court_cases_data(input_data):
    try:
        if input_data.get('search_by')=='1':
            search_by = 'case_no_wise'
        elif input_data.get('search_by')=='2':
            search_by = 'filing_no_wise'
        elif input_data.get('search_by')=='3':
            search_by = 'case_type_wise'
        elif input_data.get('search_by')=='4':
            search_by = 'party_wise'
        elif input_data.get('search_by')=='5':
            search_by = 'advocate_wise'

        starting_page_headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'en-US,en;q=0.9,hi;q=0.8',
            'Cache-Control': 'max-age=0',
            'Connection': 'keep-alive',
            'Cookie': f'_ga=GA1.3.1468851884.1678795714; _gid=GA1.3.347674307.1678795714; XSRF-TOKEN={get_cookies_data()["XSRF-TOKEN"]}; laravel_session={get_cookies_data()["laravel_session"]}',
            'Host': 'nclat.nic.in',
            'sec-ch-ua': '"Chromium";v="110", "Not A(Brand";v="24", "Google Chrome";v="110"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'same-origin',
            'Sec-Fetch-User': '?1',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36'
        }
        starting_page_response = session.get("https://nclat.nic.in/display-board/cases", headers=starting_page_headers, verify=False)
        if starting_page_response.status_code==200:
            logger.info('we have got starting page response successfully')

        soup = BeautifulSoup(starting_page_response.content, 'html.parser')
        token_value = soup.select('form#FormId>input')[0].get('value')

        court_cases_data_payload = f"_token={token_value}&search_by={search_by}&location={input_data.get('location')}&case_type={input_data.get('case_type')}&case_status={input_data.get('case_status')}&select_party={input_data.get('party_type')}&party_name={input_data.get('party_name')}&diary_no={input_data.get('filing_no')}&case_number={input_data.get('case_number')}&advocate_name={input_data.get('advocate_name')}&case_year={input_data.get('case_year')}"
        
        court_cases_data_headers = {
            'Accept': '*/*',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'en-US,en;q=0.9,hi;q=0.8',
            'Connection': 'keep-alive',
            'Content-Length': f'{len(court_cases_data_payload)}',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Cookie': f'_ga=GA1.3.1468851884.1678795714; _gid=GA1.3.347674307.1678795714; XSRF-TOKEN={get_cookies_data()["XSRF-TOKEN"]}; laravel_session={get_cookies_data()["laravel_session"]}',
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
        court_cases_data_response = session.post("https://nclat.nic.in/display-board/cases_details", headers=court_cases_data_headers, data=court_cases_data_payload, verify=False)
        if court_cases_data_response.status_code==200:
            logger.info('we have got court cases data response successfully')
        else:
            logger.info('we have not got proper court cases data response')

        cookies_value = session.cookies.get_dict()
        xsrf_token = cookies_value.get('XSRF-TOKEN')
        laravel_session = cookies_value.get('laravel_session')

        court_cases_data_list = court_cases_data_response.json().get('data')
        if court_cases_data_list == []:
            logger.info(f'No data found for {input_data}')
        for court_cases_data in court_cases_data_list:
            sr_no = court_cases_data[0]
            filing_no = court_cases_data[1]
            case_no = court_cases_data[2]
            case_title = court_cases_data[3]
            registration_date_format = court_cases_data[4]
            if registration_date_format:
                registration_date = timestamp_convertor(registration_date_format)
            else:
                registration_date = registration_date_format
            status = court_cases_data[5]
            if status == 'Pending':
                status = status
            else:
                status = court_cases_data[5].split('>')[1].split('<')[0].strip()
            data = {
                'sr_no': sr_no,
                'filing_no': filing_no,
                'case_no': case_no,
                'case_title': case_title,
                'registration_date': registration_date,
                'status': status,
                'action': 'View',
                'token': token_value,
                'xsrf_token': xsrf_token,
                'laravel_session': laravel_session
            }
            court_cases_table.append(data)

        return court_cases_table

    except Exception as e:
        logger.info(f"Error in get_tribunals_court_cases_data :- {traceback.format_exc()}")


# print(get_tribunals_court_cases_data(input_data))

