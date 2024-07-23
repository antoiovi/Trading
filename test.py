import logging
import logging.handlers
import os

import requests

import urllib.request
import gzip



logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger_file_handler = logging.handlers.RotatingFileHandler(
    "status.log",
    maxBytes=1024 * 1024,
    backupCount=1,
    encoding="utf8",
)
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger_file_handler.setFormatter(formatter)
logger.addHandler(logger_file_handler)


if __name__ == "__main__":
    url="https://www.borsaitaliana.it/borsa/derivati/indicatori-opzioni/open-interest.html"
    try:
        request = urllib.request.Request(url)
        request.add_header('Accept-encoding', 'gzip')
        data = gzip.GzipFile(fileobj=urllib.request.urlopen(request)).read()
        html = data.decode("utf-8")
        logger.info(f'Html OK')
        print("OK OK OK ")
    except Exception as e:
        logger.info(f'Exception raggiunta')
        print(e)
        
    '''
    r = requests.get(url)
    if r.status_code == 200:
        data = r.json()
        print("STATUS 200")
    else:
      print("ERROR")
    '''
