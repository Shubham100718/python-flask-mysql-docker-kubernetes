import traceback
import logging
from timestamp_convertor import timestamp_convertor
import urllib3
urllib3.disable_warnings()


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s:%(levelname)s:%(name)s:%(message)s')
file_handler = logging.FileHandler('tribunals.log')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

def get_listing_details_table(session, hearing_date_format, filing_no, bench_name, token, xsrf_token, laravel_session):
    try:
        listing_details_payload = f"filing_no={filing_no}&listing_date={hearing_date_format}&_token={token}&bench_name={bench_name}"

        listing_details_headers = {
            'Accept': 'text/plain, */*; q=0.01',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'en-US,en;q=0.9,hi;q=0.8',
            'Connection': 'keep-alive',
            'Content-Length': f'{len(listing_details_payload)}',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Cookie': f'_ga=GA1.3.1468851884.1678795714; XSRF-TOKEN={xsrf_token}; laravel_session={laravel_session}',
            'Host': 'nclat.nic.in',
            'Origin': 'https://nclat.nic.in',
            'Referer': 'https://nclat.nic.in/display-board/cases',
            'sec-ch-ua': '"Google Chrome";v="111", "Not(A:Brand";v="8", "Chromium";v="111"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36',
            'X-Requested-With': 'XMLHttpRequest'
        }
        listing_details_response = session.post("https://nclat.nic.in/display-board/listing_details", headers=listing_details_headers, data=listing_details_payload, verify=False)
        
        if listing_details_response.status_code != 200:
            logger.info('we have not got proper listing details response')
        
        listing_details_data = listing_details_response.json().get('data')
        case_no = listing_details_data.get('case_type') + ' - ' + listing_details_data.get('case_year')
        diary_no = listing_details_data.get('filing_no')
        listing_date_format = listing_details_data.get('hearing_date')
        if listing_date_format:
            listing_date = timestamp_convertor(listing_date_format)
        else:
            listing_date = listing_date_format
        court_no = listing_details_data.get('court_no')
        coram = listing_details_data.get('coram')
        proceeding_summary = listing_details_data.get('proceeding_summary')
        stage_of_case = listing_details_data.get('stage_of_case')
        data = {
            'case_no': case_no,
            'diary_no': diary_no,
            'listing_date': listing_date,
            'court_no': court_no,
            'coram': coram,
            'proceeding_summary': proceeding_summary,
            'stage_of_case': stage_of_case
        }
        return data
    except:
        logger.info(f"Error in get_listing_details_table :- {traceback.format_exc()}")

