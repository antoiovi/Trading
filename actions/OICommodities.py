import pandas as pd
import numpy as np 
import yfinance as yf
import datetime

class OIcommodities():
    
    commodities=['SI=F','GC=F','HG=F','CL=F','BZ=F','NG=F','ZC=F','KE=F','ZS=F','CC=F','KC=F','SB=F']
        
    def __init__(self,filename='csv/oicommodities.csv'):
        self.filename=filename
        print("Read file")
        self.df=self.read_file()
        print("Df readed :")
        print(self.df)
        
    def read_file(self):
        try:
            df=pd.read_csv(self.filename,index_col=False) 
            df['Date']=pd.to_datetime(df['Date'])
            df.set_index(['Symbol','Date'],inplace=True,drop=True)
            return df
        except Exception as e:
            print(e)
            print("Error Reading : ",self.filename)
            return None
        
        
    def update(self):
        try:
            print("Read infos start")
            df1=self.read_infos()
            print("Read infos ok")
            print(df1.head(3))
            print(df1.tail(3))            
            print("try to concat")
            df2=pd.concat([self.df,df1])
            print("Concat ok")
            print(df2.head(3))
            print(df2.tail(3))                        
            print("remove duplicated...")
            df2=df2.reset_index().drop_duplicates(subset=['Symbol','Date'], keep="last").set_index(['Symbol','Date'])
            print("#"*10,"duplicated removed","#"*10)
            print(df2.head(3))
            print(df2.tail(3))                        
            print("#"*10,"Reset index ...","#"*10)
            df2.reset_index(inplace=True)
            print(df2.head(3))
            print(df2.tail(3))                   
            print("#"*50)
            print("Try to save ...",self.filename)
            df2.to_csv(self.filename,index=False)
            print("Saved OK")
            self.df=df2
            return self.df
        except:
            return None
        
    def read_infos(self):
        infos={}
        for symbol in self.commodities:
            try:
                data=yf.Ticker(symbol)
                infos[symbol]=data.info
            except :
                print("Error in raed infos reading ticker")
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
    df=oicomm.update()
    if df is None:
        print("Problems updating open interst file.")
        print(df.head(3))
        print(". . "*20)
    else:
        print("Open interests updated .")
    print('#'*20,'  FINE  ','#'*20)
