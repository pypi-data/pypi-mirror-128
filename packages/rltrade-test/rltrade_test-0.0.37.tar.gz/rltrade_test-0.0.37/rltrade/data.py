import time
import numpy as np
import pandas as pd
import yfinance as yf
from stockstats import StockDataFrame as Sdf

import threading
from datetime import datetime
from ibapi.client import EClient
from ibapi.wrapper import EWrapper
from ibapi.contract import Contract


def time_series_split(df, start, end, target_date_col="date"):
    """
    split the dataset into training or testing using date
    :param data: (df) pandas dataframe, start, end
    :return: (df) pandas dataframe
    """
    df = df.copy()
    data = df[(df[target_date_col] >= start) & (df[target_date_col] < end)]
    data = data.sort_values([target_date_col, "tic"], ignore_index=True)
    data.index = data[target_date_col].factorize()[0]
    return data

def add_cov_matrix(df,lookback=252):
    # add covariance matrix as states
    df=df.sort_values(['date','tic'],ignore_index=True)
    df.index = df.date.factorize()[0]

    cov_list = []
    for i in range(lookback,len(df.index.unique())):
        data_lookback = df.loc[i-lookback:i,:]
        price_lookback=data_lookback.pivot_table(index = 'date',columns = 'tic', values = 'close')
        return_lookback = price_lookback.pct_change().dropna()
        covs = return_lookback.cov().values 
        cov_list.append(covs)
    
    df_cov = pd.DataFrame({'date':df.date.unique()[lookback:],'cov_list':cov_list})
    df = df.merge(df_cov, on='date')
    df = df.sort_values(['date','tic']).reset_index(drop=True)
    return df
    

class YahooDownloader:
    """Provides methods for retrieving daily stock data from
    Yahoo Finance API
    Attributes
    ----------
        start_date : str
            start date of the data (modified from neofinrl_config.py)
        end_date : str
            end date of the data (modified from neofinrl_config.py)
        ticker_list : list
            a list of stock tickers (modified from neofinrl_config.py)
    Methods
    -------
    fetch_data()
        Fetches data from yahoo API
    """

    def __init__(self, start_date: str, end_date: str, ticker_list: list):

        self.start_date = start_date
        self.end_date = end_date
        self.ticker_list = ticker_list

    def fetch_data(self) -> pd.DataFrame:
        """Fetches data from Yahoo API
        Parameters
        ----------
        Returns
        -------
        `pd.DataFrame`
            7 columns: A date, open, high, low, close, volume and tick symbol
            for the specified stock ticker
        """
        # Download and save the data in a pandas DataFrame:
        data_df = pd.DataFrame()
        not_downloaded = list()
        for tic in self.ticker_list:
            try:
                temp_df = yf.download(tic, start=self.start_date, end=self.end_date)
                temp_df["tic"] = tic
                data_df = data_df.append(temp_df)
            except:
                not_downloaded.append(tic)
        # reset the index, we want to use numbers as index instead of dates
        data_df = data_df.reset_index()
        if len(not_downloaded) > 0:
            print("Yahoo was not able to download this ticker",not_downloaded)
        try:
            # convert the column names to standardized names
            data_df.columns = [
                "date",
                "open",
                "high",
                "low",
                "close",
                "adjcp",
                "volume",
                "tic",
            ]
            # use adjusted close price instead of close price
            data_df["close"] = data_df["adjcp"]
            # drop the adjusted close price column
            data_df = data_df.drop(labels="adjcp", axis=1)
        except NotImplementedError:
            print("the features are not supported currently")
        # create day of the week column (monday = 0)
        data_df["day"] = data_df["date"].dt.dayofweek
        # convert date to standard string format, easy to filter
        data_df["date"] = data_df.date.apply(lambda x: x.strftime("%Y-%m-%d"))
        # drop missing data
        data_df = data_df.dropna()
        data_df = data_df.reset_index(drop=True)
        print("Shape of DataFrame: ", data_df.shape)
        # print("Display DataFrame: ", data_df.head())

        data_df = data_df.sort_values(by=["date", "tic"]).reset_index(drop=True)

        return data_df

    def select_equal_rows_stock(self, df):
        df_check = df.tic.value_counts()
        df_check = pd.DataFrame(df_check).reset_index()
        df_check.columns = ["tic", "counts"]
        mean_df = df_check.counts.mean()
        equal_list = list(df.tic.value_counts() >= mean_df)
        names = df.tic.value_counts().index
        select_stocks_list = list(names[equal_list])
        df = df[df.tic.isin(select_stocks_list)]
        return df

class IBapi(EWrapper,EClient):
    def __init__(self):
        EClient.__init__(self,self)
        self.data = []
    
    def historicalData(self, reqId, bar):
        self.data.append([bar.date,bar.open,bar.high,bar.low,bar.close,bar.volume])
    
    def get_df(self):
        df = pd.DataFrame(self.data,
        columns=['date','open','high','low','close','volume'])
        df['date'] = pd.to_datetime(df['date'],unit='s') 
        return df


class IBKRDownloader:
    """Provides methods for retrieving daily stock data from
    Interactive Broker API
    Attributes
    ----------
        start_date : str
            start date of the data (modified from neofinrl_config.py)
        end_date : str
            end date of the data (modified from neofinrl_config.py)
        ticker_list : list
            a list of stock tickers (modified from neofinrl_config.py)
    Methods
    -------
    fetch_data()
        Fetches data from API
    """
    def __init__(self,start_date,end_date,ticker_list):
        self.start_date = ''.join(start_date.split('-'))
        self.end_date = ''.join(end_date.split('-'))
        self.ticker_list = ticker_list
        self.days = (datetime.strptime(self.end_date,"%Y%m%d") -
                    datetime.strptime(self.start_date,"%Y%m%d")).days
        self.years = self.days / 365
    
    def create_contract(self,symbol,sectype='STK',exchange='SMART',currency='USD'):
        cnt = Contract()
        cnt.symbol = symbol
        cnt.secType = sectype
        cnt.exchange = exchange
        cnt.currency = currency
        return cnt
    
    def fetch_One_day_data(self,**kwargs):
        df = pd.DataFrame()
        not_downloaded = list()
        print("connecting to server...")
        app = IBapi()
        app.connect('127.0.0.1',7497,123)

        thread = threading.Thread(target=app.run,daemon=True)
        thread.start()
        time.sleep(1)

        for i,tic in enumerate(self.ticker_list):
            stock_contract = self.create_contract(tic,**kwargs)
            try:
                print("Trying to download: ",tic)
                app.reqMktData(i,stock_contract,self.end_date+" 00:00:00",'1 Y','1 day','BID',0,2,False,[])
                df = df.append(app.get_df())
                time.sleep(2)
                df['tic'] = tic
            except:
                print("Not able to download",tic)
                not_downloaded.append(tic)
        if len(not_downloaded) > 0:
            print("IB was not able to download this ticker",not_downloaded)
        app.disconnect()
        
        df = df.reset_index()
        df["day"] = df["date"].dt.dayofweek
        df["date"] = df.date.apply(lambda x: x.strftime("%Y-%m-%d"))
        df = df.dropna()
        df = df.reset_index(drop=True)
        print("Shape of DataFrame: ", df.shape)

        df = df.sort_values(by=["date", "tic"]).reset_index(drop=True)

        return df
    
    def fetch_data(self,**kwargs):
        df = pd.DataFrame()
        not_downloaded = list()
        print("connecting to server...")
        app = IBapi()
        app.connect('127.0.0.1',7497,123)

        thread = threading.Thread(target=app.run,daemon=True)
        thread.start()
        time.sleep(1)

        for i,tic in enumerate(self.ticker_list):
            stock_contract = self.create_contract(tic,**kwargs)
            try:
                print("Trying to download: ",tic)
                app.reqHistoricalData(i,stock_contract,self.end_date+" 00:00:00",'1 Y','1 day','BID',0,2,False,[])
                df = df.append(app.get_df())
                time.sleep(2)
                df['tic'] = tic
            except:
                print("Not able to download",tic)
                not_downloaded.append(tic)
        if len(not_downloaded) > 0:
            print("IB was not able to download this ticker",not_downloaded)
        app.disconnect()
        
        df = df.reset_index()
        df["day"] = df["date"].dt.dayofweek
        df["date"] = df.date.apply(lambda x: x.strftime("%Y-%m-%d"))
        df = df.dropna()
        df = df.reset_index(drop=True)
        print("Shape of DataFrame: ", df.shape)

        df = df.sort_values(by=["date", "tic"]).reset_index(drop=True)

        return df


class FeatureEngineer:
    """Provides methods for preprocessing the stock price data
    Attributes
    ----------
        stock_indicators : boolean
             stock indicators or not
        stock_indicator_list : list
            a list of technical indicator names (modified from neofinrl_config.py)
        turbulence : boolean
            use turbulence index or not
    Methods
    -------
    create_data()
        main method to do the feature engineering
    """
    
    def __init__(self,stock_indicator_list = [],
                   additional_indicators = [],
                   cov_matrix = False):
        self.stock_indicator_list = stock_indicator_list
        self.additional_indicators = additional_indicators
        self.cov_matrix = cov_matrix
    
    def create_data(self,df):
        df = self.clean_data(df)
        if 'hurst_exp' in self.additional_indicators:
            df = self.add_hurst_exponent(df)

        if 'vix_fix_1year' in self.additional_indicators:
            df = self.add_vix_fix(df,1)
        if 'sharpe_1year' in self.additional_indicators:
            df = self.add_sharpe(df,1)
        if 'sortino_1year' in self.additional_indicators:
            df = self.add_sortino(df,1)
        if 'calamar_1year' in self.additional_indicators:
            df = self.add_clamar(df,1)
        
        if 'vix_fix_3year' in self.additional_indicators:
            df = self.add_vix_fix(df,3)
        if 'sharpe_3year' in self.additional_indicators:
            df = self.add_sharpe(df,3)
        if 'sortino_3year' in self.additional_indicators:
            df = self.add_sortino(df,3)
        if 'calamar_3year' in self.additional_indicators:
            df = self.add_clamar(df,3)
        
        if 'vix_fix_5year' in self.additional_indicators:
            df = self.add_vix_fix(df,5)
        if 'sharpe_5year' in self.additional_indicators:
            df = self.add_sharpe(df,5)
        if 'sortino_5year' in self.additional_indicators:
            df = self.add_sortino(df,5)
        if 'calamar_5year' in self.additional_indicators:
            df = self.add_clamar(df,5)

        if len(self.stock_indicator_list)>0:
            df = self.add_stock_indicators(df)
        
        # if self.turbulence:
        #     df = self.add_turbulence(df)
        
        if self.cov_matrix:
            df = self.add_cov_matrix(df)
    
        #fill the missing values created during preprocessing
        df.loc[:,self.stock_indicator_list] = df[self.stock_indicator_list].replace([np.inf, -np.inf], np.nan)
        df = df.fillna(method="ffill").fillna(method="bfill")
        df = df.sort_values(["date", "tic"], ignore_index=True)
        df.index = df["date"].factorize()[0]
        return df
    
    def train_test_split(self,df,train_period,test_period):
        df = self.create_data(df)
        train = time_series_split(df, start = train_period[0], end = train_period[1])
        test = time_series_split(df, start = test_period[0], end = test_period[1])
        return train,test
    
    def add_cov_matrix(self,df,lookback=252):
        # add covariance matrix as states
        df=df.sort_values(['date','tic'],ignore_index=True)
        df.index = df.date.factorize()[0]

        cov_list = []
        for i in range(lookback,len(df.index.unique())):
            data_lookback = df.loc[i-lookback:i,:]
            price_lookback=data_lookback.pivot_table(index = 'date',columns = 'tic', values = 'close')
            return_lookback = price_lookback.pct_change().dropna()
            covs = return_lookback.cov().values 
            cov_list.append(covs)
        
        df_cov = pd.DataFrame({'date':df.date.unique()[lookback:],'cov_list':cov_list})
        df = df.merge(df_cov, on='date',how='left')
        df = df.sort_values(['date','tic']).reset_index(drop=True)
        return df
    
    def add_hurst_exponent(self,data,max_lag=20):
        df = data.copy()
        unique_ticker = df.tic.unique()
        indicator_df = pd.DataFrame()
        for ticker in unique_ticker:
            temp = df[(df['tic'] == ticker)].copy()
            temp['hurst_exp'] = temp['close'].rolling(max_lag*2).apply(lambda x:self.get_hurst_exponent(x.values))
            indicator_df = indicator_df.append(temp, ignore_index=True )
        df = df.merge(indicator_df[["tic", "date", f'hurst_exp']], on=["tic", "date"], how="left")
        return df

    def get_hurst_exponent(self,time_series, max_lag=20):
        """Returns the Hurst Exponent of the time series"""
        lags = range(2, max_lag)

        # variances of the lagged differences
        tau = [np.std(np.subtract(time_series[lag:], time_series[:-lag])) for lag in lags]

        # calculate the slope of the log plot -> the Hurst Exponent
        reg = np.polyfit(np.log(lags), np.log(tau), 1)

        return reg[0]


    def add_sharpe(self,data,years):
        df = data.copy()
        days = years * 252
        unique_ticker = df.tic.unique()
        indicator_df = pd.DataFrame()
        for ticker in unique_ticker:
            temp = df[(df['tic'] == ticker)].copy()
            temp['daily_return'] = temp['close'].pct_change(1)
            temp['daily_return'].fillna(0,inplace=True)
            temp[f'sharpe_{years}year'] = temp['daily_return'].rolling(days,min_periods=1).mean() / temp['daily_return'].rolling(days,min_periods=1).std()
            indicator_df = indicator_df.append(temp, ignore_index=True )
        df = df.merge(indicator_df[["tic", "date", f'sharpe_{years}year']], on=["tic", "date"], how="left")
        return df
    
    def add_sortino(self,data,years):
        df = data.copy()
        days = years * 252
        unique_ticker = df.tic.unique()
        indicator_df = pd.DataFrame()
        for ticker in unique_ticker:
            temp = df[(df['tic'] == ticker)].copy()
            temp['daily_return'] = temp['close'].pct_change(1)
            temp['daily_return'].fillna(0,inplace=True) 
            temp['daily_negative_return'] = temp['daily_return'] 
            temp.loc[(temp['daily_negative_return']>0),'daily_negative_return'] = 0
            temp[f'sortino_{years}year'] = temp['daily_negative_return'].rolling(days,min_periods=1).mean() / temp['daily_negative_return'].rolling(days,min_periods=1).std()
            indicator_df = indicator_df.append(temp, ignore_index=True)
        df = df.merge(indicator_df[["tic", "date", f'sortino_{years}year']], on=["tic", "date"], how="left")
        return df
    
    def add_clamar(self,data,years):
        df = data.copy()
        days = years * 252
        unique_ticker = df.tic.unique()
        indicator_df = pd.DataFrame()
        for ticker in unique_ticker:
            temp = df[(df['tic'] == ticker)].copy()
            temp['daily_return'] = temp['close'].pct_change(1)
            temp['daily_drawndown'] = temp['daily_return'].diff(1)
            temp['daily_return'].fillna(0,inplace=True)
            temp[f'calamar_{years}year'] = temp['daily_return'].rolling(days,min_periods=1).mean()/temp['daily_drawndown'].rolling(days,min_periods=1).min()
            indicator_df = indicator_df.append(temp, ignore_index=True)
        df = df.merge(indicator_df[["tic", "date", f'calamar_{years}year']], on=["tic", "date"], how="left")
        return df
    
    def add_vix_fix(self,data,years):
        df = data.copy()
        days = years * 252
        unique_ticker = df.tic.unique()
        indicator_df = pd.DataFrame()
        for ticker in unique_ticker:
            temp = df[(df['tic'] == ticker)].copy()
            temp[f'vix_fix_{years}year'] = ((temp['close'].rolling(days,min_periods=1).max() \
                                         - temp['low'])/temp['close'].rolling(days,min_periods=1).max()) * 100
            indicator_df = indicator_df.append(temp, ignore_index=True)
        df = df.merge(indicator_df[["tic", "date", f'vix_fix_{years}year']], on=["tic", "date"], how="left")
        return df

    def add_stock_indicators(self,data):
        df = data.copy()
        df = df.sort_values(by=["tic", "date"])
        stock = Sdf.retype(df.copy())
        unique_ticker = stock.tic.unique()
        for indicator in self.stock_indicator_list:
            indicator_df = pd.DataFrame()
            for i in range(len(unique_ticker)):
                try:
                    temp_indicator = stock[stock.tic == unique_ticker[i]][indicator]
                    temp_indicator = pd.DataFrame(temp_indicator)
                    temp_indicator["tic"] = unique_ticker[i]
                    temp_indicator["date"] = df[df.tic == unique_ticker[i]][
                        "date"
                    ].to_list()
                    indicator_df = indicator_df.append(
                        temp_indicator, ignore_index=True
                    )
                except Exception as e:
                    print(e)
            df = df.merge(
                indicator_df[["tic", "date", indicator]], on=["tic", "date"], how="left")
        df = df.sort_values(by=["date", "tic"])
        return df

    def add_turbulence(self,data):
        """
        add turbulence index from a precalcualted dataframe
        :param data: (df) pandas dataframe
        :return: (df) pandas dataframe
        """
        df = data.copy()
        turbulence_index = self.calculate_turbulence(df)
        df = df.merge(turbulence_index, on="date")
        df = df.sort_values(["date", "tic"]).reset_index(drop=True)
        return df

    def clean_data(self,data):
        df = data.copy()
        df = df.sort_values(["date", "tic"], ignore_index=True)
        df.index = df.date.factorize()[0]
        merged_closes = df.pivot_table(index="date", columns="tic", values="close")
        merged_closes = merged_closes.dropna(axis=1)
        tics = merged_closes.columns
        df = df[df.tic.isin(tics)]
        return df

    def calculate_turbulence(self, data):
        """calculate turbulence index based on dow 30"""
        # can add other market assets
        df = data.copy()
        df_price_pivot = df.pivot(index="date", columns="tic", values="close")
        # use returns to calculate turbulence
        df_price_pivot = df_price_pivot.pct_change()

        unique_date = df.date.unique()
        # start after a year
        start = 252
        turbulence_index = [0] * start
        # turbulence_index = [0]
        count = 0
        for i in range(start, len(unique_date)):
            current_price = df_price_pivot[df_price_pivot.index == unique_date[i]]
            # use one year rolling window to calcualte covariance
            hist_price = df_price_pivot[
                (df_price_pivot.index < unique_date[i])
                & (df_price_pivot.index >= unique_date[i - 252])
            ]
            # Drop tickers which has number missing values more than the "oldest" ticker
            filtered_hist_price = hist_price.iloc[
                hist_price.isna().sum().min() :
            ].dropna(axis=1)

            cov_temp = filtered_hist_price.cov()
            current_temp = current_price[[x for x in filtered_hist_price]] - np.mean(
                filtered_hist_price, axis=0
            )
            # cov_temp = hist_price.cov()
            # current_temp=(current_price - np.mean(hist_price,axis=0))

            temp = current_temp.values.dot(np.linalg.pinv(cov_temp)).dot(
                current_temp.values.T
            )
            if temp > 0:
                count += 1
                if count > 2:
                    turbulence_temp = temp[0][0]
                else:
                    # avoid large outlier because of the calculation just begins
                    turbulence_temp = 0
            else:
                turbulence_temp = 0
            turbulence_index.append(turbulence_temp)

        turbulence_index = pd.DataFrame(
            {"date": df_price_pivot.index, "turbulence": turbulence_index}
        )
        return turbulence_index
    
