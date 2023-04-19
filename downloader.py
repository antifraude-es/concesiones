from datetime import date, datetime, timedelta
from utils import month_to_date, month_to_str
from time import sleep
import calendar
import requests
import random
import time
import re
import os


class Downloader:
    def __init__(self, agent_id, month: date, output_folder):
        # create non existing folder

        self.agent_id = agent_id
        self.month = month

        self.days_in_month = self.get_dates_in_month(self.month)
        self.folder = os.path.join(output_folder, str(month.year))
        if not os.path.exists(self.folder):
            os.makedirs(self.folder)

    def start(self):
        print("Starting downloader")
        print("Agent ID: " + self.agent_id)
        print("Month: " + month_to_str(self.month))
        candidates = self.get_candidates_list(self.days_in_month)
        while candidates:
            candidate = random.choice(candidates)
            time.sleep(random.randint(1, 3))
            self.save_response(candidate, 'test')
            candidates = self.get_candidates_list(self.days_in_month)

    def stop(self):
        print("Stopping downloader")

    def get_dates_in_month(self, date_month):
        year = date_month.year
        month = date_month.month
        num_days = calendar.monthrange(year, month)[1]
        dates = [date(year, month, day) for day in range(1, num_days+1)]
        return dates

    def get_candidates_list(self, days_in_month):
        candidates = []
        for x in days_in_month:
            if not os.path.exists(self.get_output_file_path(x)):
                candidates.append(x)
        return candidates

    def get_output_file_path(self, date_obj: date) -> str:
        filename = date_obj.strftime('%m-%d.json')
        return os.path.join(self.folder, filename)

    def save_response(self, date, content):
        self.get_output_file_path(date)
        output_file = self.get_output_file_path(date)
        print(output_file)
        with open(output_file, 'w') as f:
            f.write(content)


def get_csrf(session: requests.Session):
    url = 'https://www.pap.hacienda.gob.es/bdnstrans/GE/es/concesiones'
    response = session.get(url, verify=False)
    csrf_regex = r'<input.*?name="_csrf".*?value="(.*?)".*?>'
    csrf_value = re.findall(csrf_regex, response.text)[0]
    return csrf_value


def make_post_request(session, day_date, _csrf):
    # date to dd/mm/yyyy
    query_date = month_to_str(day_date)
    url = 'https://www.pap.hacienda.gob.es/bdnstrans/GE/es/concesiones'
    body = {
        '_ministerios': '1',
        '_organos': '1',
        '_cAutonomas': '1',
        '_departamentos': '1',
        '_locales': '1',
        '_localesOculto': '1',
        'beneficiarioFilter': 'DNI',
        'beneficiarioDNI': '',
        'beneficiarioNombre': '',
        'beneficiario': '',
        'fecDesde': query_date,
        'fecHasta': query_date,
        'tipoBusqPalab': '1',
        'titulo': '',
        '_regiones': '1',
        '_actividadesNACE': '1',
        '_instrumentos': '1',
        '_csrf': _csrf
    }
    response = session.post(url, data=body)
    return response
