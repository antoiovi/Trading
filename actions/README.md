
# Daily collection of open interest of stocks of "Borsa Italiana"


* File OIStocks.py
* [root of repo ]requirements.txt
* [root of repo ]./github/workflows/main.yml

  The github workflow main.yml, using requirements.txt, launch OIStocks.py once every day, which
  scraps data from web site of "Borsa Italiana" , to extract "Open Interest" about stocks of FTSEMIB.
  The data are saved (appended ) into csv/openinterest.csv and status.log is updated.

    ### 13 February 2025
    The action is has been temprarly disabled : a lot of data has been collected, useful to study the
    SHARES openinterst. 


# Daily collection of open interst data concerning commodities
 
 * File OICommodities.py
* [root of repo ]requirements2.txt
* [root of repo ]./github/workflows/oicommod.yml

The workflow oicommod.yml runs every day the file OICommodities.py, and 
throughout the library yfinance the open interest of a few commodities are
collected and saved into the file [root_of_repo]csv/oicommodities.csv