import logging
import logging.handlers
import os
import re
import pandas as pd

import requests
import datetime as dt



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

def extract_day(html):
    pattern = r'<span class="[^"]*">[^<]*Ultimo Aggiornamento[^<]*</span>'
    
    # Cerchiamo tutte le occorrenze nel testo html
    matches = re.findall(pattern, html, re.IGNORECASE)
    test=None
    last_date=None
    today=dt.datetime.now().date()

    # Stampa i risultati
    for l in matches:
        match = re.search(r'(\d+/\d+/\d+)',l)
        if match is None:
            continue
        test=match.group(1)
        print("Data from html OK : ",test)

    if test is None:
        last_date=today
        print("Data not found in html : put today: ",today)
    else:
        print("Data ok found in html : put : ",test)
        last_date=pd.to_datetime(test,format='%d/%m/%y').date()
    return last_date

def display(x):
    print(x)


def open_file():
    filename="openinterst.csv"
    dflocal=pd.read_csv(filename,index_col=False)
    dflocal['Date']=pd.to_datetime(dflocal['Date'])
    return dflocal

def merge_df(dflocal,dftemp):
    today=dt.datetime.now()
    try:
        print(dflocal['Date'].max().date())
        print(dftemp['Date'].max().date())
        if dftemp['Date'].max().date()>dflocal['Date'].max().date():
            print("dftemp date> dflocal date..")
            dfz=pd.concat([dflocal,dftemp]).reset_index(drop=True)
            return dfz
        else:
            print("dftemp date <= dflocal date..Non faccio il merge")
            return None

    except FileNotFoundError:
        print("FILE NON ESISTE: CREO NUOVO FILE")
        return None
        

if __name__ == "__main__":
    url="https://www.borsaitaliana.it/borsa/derivati/indicatori-opzioni/open-interest.html"
    try:
        filename="openinterst.csv"
        # Effettua una richiesta GET
        response = requests.get(url)
        # Controlla che la richiesta sia stata completata con successo
        if response.status_code == 200:
            logger.info(f'Response status 200 : OK')
            # Decodifica il contenuto della risposta in 'utf-8'
            html_content = response.content.decode('utf-8')
            # Estrae le tabelle e crea i dataframe
            dfs = extract_tables_from_html(html_content)
            # Stampa i dataframe creati
            if len(dfs)>0:
                df=dfs[0] 
                last_date=extract_day(html_content)
                print("*Last day ",last_date )
                df=df.iloc[:,:]
                df['Date']=pd.to_datetime(last_date)
                df.dropna(inplace=True)
                print("#################")
                print(df)
                print("OK OK OK ")
                logger.info(f'OK OK')
                dflocal=open_file()  
                ##################################################
                #   SOLO PER TEST
                ##################################################
                h=dt.datetime.now().hour
                m=dt.datetime.now().minute
                s=dt.datetime.now().second
                fn="test{}-{}-{}-{}.csv".format(str(dt.datetime.now().date()),h,m,s)
                #dflocal.to_csv(fn,index=False)
                ##################################################
                
                newdf=merge_df(dflocal,df)
                print(newdf)
                if newdf is not None:
                    newdf.to_csv(filename,index=False)
                    logger.info(f'Dati aggiornati')
                else:
                    logger.info(f'Dati NON aggiornati')
                    
            else:
                logger.warn(f'Nessuna tabella ne file html...')
        else:
            print(f"Errore nella richiesta: {response.status_code}")        
            logger.error(f"Errore nella richiesta: {response.status_code}")        
    except Exception as e:
        logger.error(f'Exception raggiunta')
        print(e)
