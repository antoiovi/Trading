import pandas as pd
import numpy as np 
import yfinance as yf
      
      
def test_yf():      
    try:
        ticker=yf.Ticker('A2A.MI')
        df=ticker.history('1y')
        print(df.head(5))
    except Exception as e:
        print(e)
        print("[TEST_YF() ] Errore ")


if __name__ == "__main__":
    print("Running OICommodities.....")
    test_yf()
    print('#'*20,'  FINE  ','#'*20)