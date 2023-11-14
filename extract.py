# extract.py
import requests
from bs4 import BeautifulSoup
import pandas as pd

def scrape_hospital_data():
    url = 'removed-for-privacy.url'
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    return soup.find_all(class_='card')

def extract_hospital_info(hsp):
    try:
        num = hsp.find_all('strong')[1].text
    except:
        num = None

    return {
        'id': hsp['id'],
        'Hospital Name': hsp.h5.text,
        'Address': hsp.p.text,
        'Phone Number': num,
        'Website': hsp.a['href']
    }
