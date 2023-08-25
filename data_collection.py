import const 
import csv
import pandas as pd
import requests
import os
import json
import yfinance as yf
import util
class NasDaq:
    api_key="f1gVr-j9kJdBb25jNKXM"
class EOD:
    api_key="64c9d7111332d8.91672679"
    def storeMarketCap(ticker_code,data_dict):
        """store market cap json to a csv file """
      
        # Create a list of dictionaries to store the date and value data
        data_list = []
        for key in data_dict:
            date = data_dict[key]['date']
            value = data_dict[key]['value']
            data_list.append({'date': date, 'value': value})

        # Create a Pandas dataframe from the data list
        df = pd.DataFrame(data_list)
        df.rename(columns={'date': 'year'}, inplace=True)
        df['year'] = df['year'].str.slice(stop=4)
        #find the average market cap 
        averageMarketCapDF = df.groupby('year', as_index=False)['value'].mean()
        averageMarketCapDF.rename(columns={'value': 'market cap'}, inplace=True)
        if not os.path.exists(const.MARKET_CAP_DIR):
            # If not, create the folder
            os.makedirs(const.MARKET_CAP_DIR)
            print(f"Folder created: {const.MARKET_CAP_DIR}")
        store_path=os.path.join(const.MARKET_CAP_DIR,f"{ticker_code}.csv")
        print(f"save market cap to {store_path}")
        averageMarketCapDF.to_csv(store_path,index=0)
        # Print the resulting dataframe
        print(averageMarketCapDF)
        # Print the resulting dataframe
        #print(df)
    def getHistoricalMarketCap(ticker_code="AAPL"):#TODO: remove AAPL as default ticker
        #url = f"https://eodhistoricaldata.com/api/historical-market-cap/{ticker_code}"
        #url=f"https://eodhistoricaldata.com/api/historical-market-cap/AAPL.US?api_token={EOD.api_key}"
        
        url=f"https://eodhistoricaldata.com/api/historical-market-cap/{ticker_code}?api_token=demo" #TODO: add api_token
        #TODO change url back to referencing ticker_code
        #params = {'api_token': EOD.api_key}

        response = requests.get(url)
        #response=requests.get(url)

        if response.ok:
            market_cap_data = response.json()
            print(market_cap_data)
            EOD.storeMarketCap(ticker_code,market_cap_data)
        else:
            print('Request failed with status code', response.status_code)
            exit(0)

    def storeFinStatementToCSV(ticker_code,data_dict,statement_type):
        statement_dir={"Balance_Sheet":const.BALANCE_SHEET_CSV_DIR,
                       "Cash_Flow":const.CASH_FLOW_CSV_DIR,
                       "Income_Statement":const.INCOME_STATEMENT_CSV_DIR}
        def get_first_n_rows(d,n): 
            """This function is used to get the statement partially, for better understanding"""
            keys = list(d.keys())[:n]
            return {key: d[key] for key in keys}
        if not statement_type in ["Balance_Sheet","Cash_Flow","Income_Statement"]:
            print("Invalid statement type")
            exit(1)
        
        yearly_cashflow=data_dict["Financials"][statement_type]["yearly"]
        #yearly_cashflow=get_first_n_rows(yearly_cashflow,2) 
        df = pd.DataFrame.from_dict(yearly_cashflow, orient='index')
        print(df)
        df_path=os.path.join(statement_dir[statement_type],f"{ticker_code}.csv")
        df.to_csv(df_path)
        print(f"updated {df_path}")

    def getFinStatements(ticker_code="AAPL"):
        url=f"https://eodhistoricaldata.com/api/fundamentals/{ticker_code}?api_token=demo"#TODO: change the api_token
        data_dict=util.GetJsonDictFromUrl(url)
        #data_dict=json.loads(json_file)
        statement_type = ["Balance_Sheet","Cash_Flow","Income_Statement"]
        for s_type in statement_type:
            EOD.storeFinStatementToCSV(ticker_code,data_dict,statement_type=s_type)
            print(f"stored {s_type}")

        return
class yfin:
    def download_price_volume(ticker_code):
        data = yf.download(ticker_code, interval="3mo")
        folder_path = const.PRICE_VOLUME_CSV_DIR # Replace with the path to the folder you want to create

        if not os.path.exists(folder_path):#create if not exist folder 
            os.makedirs(folder_path)
        data.to_csv(os.path.join(const.PRICE_VOLUME_CSV_DIR,f"{ticker_code}.csv"))
 
    def GetCurrentMarketCap(ticker_code):
        ticker = yf.Ticker(ticker_code)  # Replace "AAPL" with the symbol of the stock you want to analyze

    # Get the historical market cap data
        hist = ticker.history(period="max",interval="1mo")
        # Calculate the market cap
        market_cap = hist['Close'] * ticker.info['sharesOutstanding']
        # Print the market cap
        print("current market cap: ")
        print(market_cap[len(market_cap)-1])
        return market_cap[len(market_cap)-1]
class alpha_vantage:
    ALPHA_API_KEY="UN03HRG3Z941GLAP"

    def download_cash_flow(ticker_code):
        """
        save to csv_files/cash_flow
        """
        def cash_flow_dict_to_csv(dict):
            #
            #get the list of annualCashFlow from the dict 
            annual_cash_flow_dict=dict["annualReports"]
            column_names = list(annual_cash_flow_dict[0].keys())
            output_csv_path= os.path.join(const.CASH_FLOW_CSV_DIR,f"{ticker_code}.csv")
            # Open a new CSV file and write the data
            with open(output_csv_path, "w", newline="") as file:
                writer = csv.DictWriter(file, fieldnames=column_names)
                writer.writeheader()
                for item in annual_cash_flow_dict:
                    writer.writerow(item)
            print(f"updated file in {output_csv_path}")
            return
        # replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
        url = f"https://www.alphavantage.co/query?function=CASH_FLOW&symbol={ticker_code}&apikey={alpha_vantage.ALPHA_API_KEY}"
        r = requests.get(url)
        data_dict = r.json()
        cash_flow_dict_to_csv(data_dict)
        return 
    def download_stock_list():
        CSV_URL = f"https://www.alphavantage.co/query?function=LISTING_STATUS&apikey={alpha_vantage.ALPHA_API_KEY}"
        with requests.Session() as s:
            download = s.get(CSV_URL)
            decoded_content = download.content.decode('utf-8')
            cr = csv.reader(decoded_content.splitlines(), delimiter=',')
            my_list = list(cr)
            with open("alpha_vantage_tickers.csv", "w", newline="") as csvfile:
                writer = csv.writer(csvfile)
                for row in my_list:
                    writer.writerow(row)
            print("Tickers saved to alpha_vantage_tickers.csv")
        return 

if __name__=="__main__":
    #EOD.storeFinStatementToCSV("demo",statement_type="Balance_Sheet")
    #EOD.getFinStatements()
    EOD.getHistoricalMarketCap()
    #EOD.getHistoricalMarketCap("demo")
    #EODHD.storeMarketCapAsDf()

    #alpha_vantage.download_cash_flow('AAPL')
    #yfin.GetCurrentPriceAndVolume("AAPL")