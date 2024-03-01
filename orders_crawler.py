import os
import traceback
import logging
import time
import urllib3
from dotenv import load_dotenv
urllib3.disable_warnings()
load_dotenv()


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s:%(levelname)s:%(name)s:%(message)s')
file_handler = logging.FileHandler('tribunals.log')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

def get_orders_pdf(session, bench_name, filing_no, order_date_format, order_type_symbol, token, xsrf_token, laravel_session):
    try:
        orders_payload = f"search_type=view_order&_token={token}&bench_name={bench_name}&filing_no={filing_no}&order_date={order_date_format}&order_type={order_type_symbol}"

        orders_headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'en-US,en;q=0.9,hi;q=0.8',
            'Cache-Control': 'max-age=0',
            'Connection': 'keep-alive',
            'Content-Length': f'{len(orders_payload)}',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Cookie': f'_ga=GA1.3.1468851884.1678795714; _gid=GA1.3.724448926.1679033392; XSRF-TOKEN={xsrf_token}; laravel_session={laravel_session}',
            'Host': 'nclat.nic.in',
            'Origin': 'https://nclat.nic.in',
            'Referer': 'https://nclat.nic.in/display-board/cases',
            'sec-ch-ua': '"Google Chrome";v="111", "Not(A:Brand";v="8", "Chromium";v="111"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'same-origin',
            'Sec-Fetch-User': '?1',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36'
        }
        orders_response = session.post("https://nclat.nic.in/display-board/view_order", headers=orders_headers, data=orders_payload, verify=False)
        
        if orders_response.status_code != 200:
            logger.info('we have not got proper orders response')

        microsecond = round(time.time() * 1000)
        orders_filename = str(microsecond)+'-'+order_date_format+'.pdf'
        with open(os.getenv('orders_path')+orders_filename, 'wb') as f:
            f.write(orders_response.content)

        return orders_filename

    except:
        logger.info(f"Error in get_orders_pdf :- {traceback.format_exc()}")

