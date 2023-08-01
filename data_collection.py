import const 
import csv
import pandas as pd
import requests
import os
import yfinance as yf

class yfin:
    def download_price_volume(ticker_code):
        data = yf.download(ticker_code, interval="3mo")
        folder_path = const.PRICE_VOLUME_CSV_DIR # Replace with the path to the folder you want to create

        if not os.path.exists(folder_path):#create if not exist folder 
            os.makedirs(folder_path)
        data.to_csv(os.path.join(const.PRICE_VOLUME_CSV_DIR,f"{ticker_code}.csv"))
    def GetHistoricalMarketCap(ticker_code):
        ticker = yf.Ticker(ticker_code)  # Replace "AAPL" with the symbol of the stock you want to analyze

    # Get the historical market cap data
        hist = ticker.history(period="max")

        # Calculate the market cap
        market_cap = hist['Close'] * ticker.info['sharesOutstanding']

        # Print the market cap
        print(market_cap)
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
    #save_stock_list()
    #yfin.download_price_volume("AAPL")
    yfin.GetHistoricalMarketCap()
    #alpha_vantage.download_cash_flow('AAPL')
    #yfin.GetCurrentPriceAndVolume("AAPL")