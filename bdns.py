

import datetime
import os
import time
from requests.packages.urllib3.util.retry import Retry
from requests.adapters import HTTPAdapter
from fake_useragent import UserAgent

import requests
import re

# base_url = 'https://www.infosubvenciones.es/'
base_url = 'https://www.pap.hacienda.gob.es/'

url_concesiones = base_url+'bdnstrans/GE/es/concesiones'
url_datos = base_url+'bdnstrans/busqueda'

page_size = 200

headers1 = {
    'Connection': 'keep-alive',
    'Pragma': 'no-cache',
    'Cache-Control': 'no-cache',
    'sec-ch-ua': '"Chromium";v="112", "Google Chrome";v="112", "Not:A-Brand";v="99"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"macOS"',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-User': '?1',
    'Sec-Fetch-Dest': 'document',
    'Referer': 'https://www.pap.hacienda.gob.es/bdnstrans/GE/es/concesiones',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'en-GB,en-US;q=0.9,en;q=0.8,nl;q=0.7,es;q=0.6',
    'Origin': 'https://www.pap.hacienda.gob.es',

}

headers_page = {    
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'X-Requested-With': 'XMLHttpRequest',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Dest': 'empty',
}

class BDNS:
    def __init__(self, date,output_folder):
        self.date = date
        self.output_folder = output_folder
        self.session = requests.Session()
        requests.urllib3.disable_warnings()
        self.retry_strategy = Retry(
            total=6, backoff_factor=1.2, status_forcelist=[500, 502, 503, 504])
        adapter = HTTPAdapter(max_retries=self.retry_strategy)
        self.session.mount('http://', adapter)
        self.session.mount('https://', adapter)
        # Generate a random user agent for the session
        self.user_agent = UserAgent().random
        self.header_init = headers1.copy()
        self.header_init['User-Agent']=UserAgent().random
        self.header_data = self.header_init.copy()
        self.header_data.update(headers_page)
        self.__get_csrf()

    def __get_csrf(self):
        response = self.session.get(url_concesiones, headers=self.header_init, verify=False)
        csrf_regex = r'<input.*?name="_csrf".*?value="(.*?)".*?>'
        csrf_value = re.findall(csrf_regex, response.text)[0]
        self.csrf = csrf_value
        # print(csrf_value)

    def __start_query(self):
        day = self.date.strftime("%d/%m/%Y")
        response = self.session.post(url_concesiones, headers=self.header_init, data={
            '_ministerios': '1',
            '_organos': '1',
            '_cAutonomas': '1',
            '_departamentos': '1',
            'entLocSearch': '',
            '_locales': '1',
            '_localesOculto': '1',
            'beneficiarioFilter': 'DNI',
            'beneficiarioDNI': '',
            'beneficiarioNombre': '',
            'beneficiario': '',
            'fecDesde': day,
            'fecHasta': day,
            'tipoBusqPalab': '1',
            'titulo': '',
            '_regiones': '1',
            '_actividadesNACE': '1',
            '_instrumentos': '1',
            '_csrf': self.csrf
        },verify=False)
        # print(response.content)
        

    def download(self):
        self.__start_query()
        all_data = []
        json = self.download_page(1)
        all_data.append(json)
        total_pages = json['total']
        page = json['page']
        total_rows = json['records']-len(json['rows'])
        while page < total_pages:
            page += 1
            json = self.download_page(page)
            all_data.append(json)
            total_rows -= len(json['rows'])
        
        if total_rows != 0:
            
            with open(os.path.join(self.output_folder,'error.log'),'a') as f:
                timestamp = datetime.datetime.now().isoformat()
                f.write(f'{timestamp} ERROR {self.date} rows = {total_rows}\n')
        
        return all_data
        
        


    def download_page(self,page_num):
        nd_value = str(int(time.time() * 1000))
        params = {
            'type': 'concs',
            '_search': 'false',
            'nd': nd_value,
            'rows': page_size,
            'page': page_num,
            'sidx': 8,
            'sord': 'asc'
        }
        return self.session.get(url_datos, headers=headers_page, params=params, verify=False).json()









