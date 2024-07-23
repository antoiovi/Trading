import logging
import logging.handlers
import os
from bs4 import BeautifulSoup

import requests

#import urllib.request
#import gzip



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


def elabora_html(html):
    soup = BeautifulSoup(html, features="html.parser")
    soup.find_all('tbody')
    soup = BeautifulSoup(html,features="html.parser")
    tables = soup.findChildren('table')
    # This will get the first (and only) table. Your page may have more.
    my_table = tables[0]
    # You can find children with multiple tags by passing a list of strings
    rows = my_table.findChildren(['thead','th'])#, 'tr'])
    righe=[]
    for row in rows:
        #print(">>>>>>>>>>>>>>>>>>>>>\n",row)
        cells = row.findChildren('th')
        r=[]
        for cell in cells:
            #print(cell)
            value = cell.string
            r.append(value)
            #print("The value in this cell is %s" % value)
        righe.append(r)
    header=righe[0]
    header[-1]='Open Interest' #Perche non mi legge svg
    rows = my_table.findChildren(['th', 'tr'])
    table=[]
    for row in rows:
        #print(">>>>>>>>>>>>>>>>>>>>>\n",row)
        cells = row.findChildren('td')
        r=[]
        for cell in cells:
            value = cell.string
            r.append(value)
            #print("The value in this cell is %s" % value)
        if len(r)>0:
            table.append(r)
    
    
    df = pd.DataFrame(table)#, columns=header)
    return df



if __name__ == "__main__":
    url="https://www.borsaitaliana.it/borsa/derivati/indicatori-opzioni/open-interest.html"
    try:
        # Effettua una richiesta GET
        response = requests.get(url)
        # Controlla che la richiesta sia stata completata con successo
        if response.status_code == 200:
            # Decodifica il contenuto della risposta in 'utf-8'
            html_content = response.content.decode('utf-8')
            df=elabora_html(html_content)
            print(df)
            print("OK OK OK ")
            logger.info(f'OK OK')
        else:
            print(f"Errore nella richiesta: {response.status_code}")        
    except Exception as e:
        logger.info(f'Exception raggiunta')
        print(e)
