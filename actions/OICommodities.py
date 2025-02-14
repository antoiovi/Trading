import pandas as pd
import numpy as np 
import yfinance as yf
import datetime

class OIcommodities():
    
    commodities=['SI=F','GC=F','HG=F','CL=F','BZ=F','NG=F','ZC=F','KE=F','ZS=F','CC=F','KC=F','SB=F']
    filename='test.csv'
    
    def __init__(self):
        self.read_csv()
        
    def read_file(self):
        try:
            self.df=pd.read_csv(self.filename,index_col=False) 
            self.df['Date']=pd.to_datetime(self.df['Date'])
            self.df.set_index(['Symbol','Date'],inplace=True,drop=True)
        except Exception as e:
            print(e)
            print("Error Reading : ",self.filename)
            self.df=None
        
        
    def update(self):
        try:
            df1=self.read_infos()
            df2=pd.concat([self.df,df1])
            df2=df2.reset_index().drop_duplicates(subset=['Symbol','Date'], keep="last").set_index(['Symbol','Date'])
            df2.to_csv(self.filename,index=False)
            self.df=df2
        except:
            return None
        
    def read_infos(self):
        infos={}
        for symbol in self.commodities:
            try:
                data=yf.Ticker(symbol)
                infos[symbol]=data.info
            except :
                continue
        fields=['openInterest', 'currency', 'exchange', 'quoteType', 'symbol', 'underlyingSymbol', 'shortName']#,'uuid']
        records={}
        for info in infos.items():
            try:
                s=info[0]
                i=info[1]
                record=[]
                for f in fields:
                    #print(infos[s][f])
                    record.append(infos[s][f])
                    #print(info[f])
                records[s]=record
            except :
                continue
        today=datetime.datetime.now()
        df=pd.DataFrame(records,index=fields).T
        df['Date']=pd.to_datetime(today.date())
        df.index.name='Symbol'
        df.reset_index(inplace=True)
        df.set_index(['Symbol','Date'],inplace=True,drop=True)
        return df


if __name__ == "__main__":
    print("Running OICommodities.....")
    oicomm=OIcommodities()
    test=oicomm.update()
    if test is None:
        print("Problems updating open interst file.")
    else:
        print("Open interests updated .")
    print('#'*20,'  FINE  ','#'*20)