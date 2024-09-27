# Trading

This is a collaction of python routines and jupyter notebooks oriented to 
financial trading.
## Daily collection of open interest of stocks of "Borsa Italiana"
* File test.py
* requirements.txt
* status.log
* ./github/workflows/main.yml
* status.log

  The github workflow main.yml, using requirements.txt, launch test.py once every day, which
  scraps data from web site of "Borsa Italiana" , to extract "Open Interest" about stocks of FTSEMIB.
  The data are saved (appended ) into openinterest.csv and status.log is updated.
 
## Url to download yahoo financial data

https://query2.finance.yahoo.com/v8/finance/chart/{symbol}?period1={start_date}&period2={end_date}&interval=1d&events=history
