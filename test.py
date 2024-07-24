import logging
import logging.handlers
import os
#from bs4 import BeautifulSoup
import re
import pandas as pd

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


# Funzione per estrarre le tabelle da un HTML e creare dataframe
def extract_tables_from_html(html):
    # Trova tutte le tabelle nell'HTML
    tables = re.findall(r'<table.*?>.*?</table>', html, re.DOTALL)
    
    dataframes = []
    
    for table in tables:
        # Trova tutte le righe della tabella
        rows = re.findall(r'<tr.*?>.*?</tr>', table, re.DOTALL)
        
        table_data = []
        
        for row in rows:
            # Trova tutte le celle della riga (sia th che td)
            cells = re.findall(r'<t[dh].*?>(.*?)</t[dh]>', row, re.DOTALL)
            # Pulisce il contenuto delle celle da eventuali tag HTML
            clean_cells = [re.sub(r'<.*?>', '', cell).strip() for cell in cells]
            # Aggiungi la riga alla tabella, saltando l'ultima colonna
            if clean_cells:
                table_data.append(clean_cells[:-1])
        
        if table_data:
            # Usa la prima riga come header
            header = table_data[0]
            data = table_data[1:]
            df = pd.DataFrame(data, columns=header)
            dataframes.append(df)
    
    return dataframes


if __name__ == "__main__":
    url="https://www.borsaitaliana.it/borsa/derivati/indicatori-opzioni/open-interest.html"
    try:
        # Effettua una richiesta GET
        response = requests.get(url)
        # Controlla che la richiesta sia stata completata con successo
        if response.status_code == 200:
            # Decodifica il contenuto della risposta in 'utf-8'
            html_content = response.content.decode('utf-8')
            # Estrae le tabelle e crea i dataframe
            dfs = extract_tables_from_html(html_content)
            if len(dfs)==0:
                print("nessuna tabella...")
            # Stampa i dataframe creati
            for i, df in enumerate(dfs):
                print(f"Tabella {i + 1}")
                print(df)
            print("OK OK OK ")
            logger.info(f'OK OK')
        else:
            print(f"Errore nella richiesta: {response.status_code}")        
    except Exception as e:
        logger.info(f'Exception raggiunta')
        print(e)
