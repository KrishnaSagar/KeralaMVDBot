# Kerala MVD Bot by Krishna Sagar
# For Educational Purposes Only

import requests
from bs4 import BeautifulSoup
from user_agent import generate_user_agent
from PIL import Image
import pytesseract
from captcha_solver import CaptchaSolver
import logging
from PIL import ImageFilter

from pprint import pprint


import numpy
import cv2


logging.basicConfig()
logging.basicConfig(level=logging.DEBUG)

proxies = {
  "http": None,
  "https": None,
}



def get_keralamvd_page(reg_no):
    FIRST_ENDPOINT = 'https://smartweb.keralamvd.gov.in/kmvdnew/services/registration/regnw.php'
    FORM_ENDPOINT = 'https://smartweb.keralamvd.gov.in/kmvdnew/services/registration/registrationnew.php'
    CAPTCHA_ENDPOINT = 'https://smartweb.keralamvd.gov.in/kmvdnew/captcha/captcha.php'

    headers = {
        'Referer': 'https://mvd.kerala.gov.in/',
        'Host': 'smartweb.keralamvd.gov.in',
        'User-Agent': generate_user_agent(),
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate, br'
    }

    req = requests.get(FIRST_ENDPOINT, headers=headers, proxies=proxies)
    soup = BeautifulSoup(req.content.decode('utf-8'), 'html.parser')
    r_token = soup.find('input', {'name': 'r_token'})['value']

    cookies = {
        'PHPSESSID': req.cookies.get('PHPSESSID')
    }

    headers['Referer'] = FIRST_ENDPOINT

    im = Image.open(requests.get(CAPTCHA_ENDPOINT, headers=headers, cookies=cookies, stream=True, proxies=proxies).raw)
    cap = pytesseract.image_to_string(im)

    headers['Referer'] = FORM_ENDPOINT

    req = requests.post(FORM_ENDPOINT, data={
        'r_token': r_token,
        'captcha': cap,
        'regfield': reg_no,
        'Submit': 'Get'}, headers=headers, cookies=cookies, proxies=proxies)

    return req.content.decode('utf-8')


def parse_keralamvd_page(page_str):
    soup = BeautifulSoup(page_str, 'html.parser')
    extracted = soup.findAll('td', {'class': 'style1'})

    return {
        'OwnerName': extracted[16].get_text().strip(),
        'WithEffectFrom': extracted[17].get_text().strip(),
        'Guadian': extracted[18].get_text().strip(),
        'Address': extracted[19].get_text().strip(),
        'DealerName': extracted[20].get_text().strip(),
        'TaxLicenseNo': extracted[21].get_text().strip(),
        'TaxPaidOn': extracted[22].get_text().strip(),
        'TaxPaidFrom': extracted[23].get_text().strip(),
        'TaxPaidTo': extracted[24].get_text().strip(),
        'TaxAmount': extracted[25].get_text().strip(),
        'TaxPaidOffice': extracted[26].get_text().strip(),
        'CessPaid': extracted[27].get_text().strip(),
        'CessPaidDate': extracted[28].get_text().strip(),
        'Category': extracted[29].get_text().strip(),
        'VehicleClass': extracted[30].get_text().strip(),
        'MakerName': extracted[31].get_text().strip(),
        'MakerClass': extracted[32].get_text().strip(),
        'CC': extracted[33].get_text().strip(),
        'BHP': extracted[34].get_text().strip(),
        'Body': extracted[35].get_text().strip(),
        'Cylinders': extracted[36].get_text().strip(),
        'MfdMonth': extracted[37].get_text().strip(),
        'MfdYear': extracted[38].get_text().strip(),
        'SeatCap': extracted[39].get_text().strip(),
        'ULW': extracted[40].get_text().strip(),
        'Fuel': extracted[41].get_text().strip(),
        'WheelBase': extracted[42].get_text().strip(),
        'Color': extracted[43].get_text().strip(),
        'RegistrationDate': extracted[44].get_text().strip(),
        'ValidUpto': extracted[45].get_text().strip(),
        'DeliveryDate': extracted[46].get_text().strip(),

    }


def get_keralamvd_prevowners(reg_no):
    PREVOWNER_ENDPOINT = 'https://smartweb.keralamvd.gov.in/kmvdnew/services/registration/ownerlists.php'
    FIRST_ENDPOINT = 'https://smartweb.keralamvd.gov.in/kmvdnew/services/registration/regnw.php'
    FORM_ENDPOINT = 'https://smartweb.keralamvd.gov.in/kmvdnew/services/registration/registrationnew.php'

    headers = {
        'Referer': 'https://mvd.kerala.gov.in/',
        'Host': 'smartweb.keralamvd.gov.in',
        'User-Agent': generate_user_agent(),
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate, br'
    }

    req = requests.get(FIRST_ENDPOINT, headers=headers, proxies=proxies)

    soup = BeautifulSoup(req.content.decode('utf-8'), 'html.parser')
    r_token = soup.find('input', {'name': 'r_token'})['value']

    cookies = {
        'PHPSESSID': req.cookies.get('PHPSESSID')
    }

    headers['Referer'] = FORM_ENDPOINT

    req = requests.post(PREVOWNER_ENDPOINT, data={
        'r_token': r_token,
        'ownerlists': 'History',
        'regfield': reg_no,
    }, headers=headers, cookies=cookies, proxies=proxies)

    return req.content.decode('utf-8')


def parse_keralamvd_prevowners(page_str) -> list:
    soup = BeautifulSoup(page_str, 'html.parser')
    owners = soup.findAll('td', {'class': 'style1'})
    owner_list = list()


    for i in range(0, (len(owners) // 6) * 6, 6):
        owner_list.append({
            'OwnerName': owners[i].get_text().strip(),
            'WithEffectFrom': owners[i + 1].get_text().strip(),
            'Guardian': owners[i + 2].get_text().strip(),
            'PRAOffice': owners[i + 3].get_text().strip(),
            'ReceivedFrom': owners[i + 4].get_text().strip(),
        })

    return owner_list

print('======Current Details======')

print('\n\n')

page = get_keralamvd_page('KL-08-BF-5307')
pprint(parse_keralamvd_page(page))

print('======Previous Owners======')
print('\n\n')
page = get_keralamvd_prevowners('KL-08-BF-5307')
pprint(parse_keralamvd_prevowners(page))

