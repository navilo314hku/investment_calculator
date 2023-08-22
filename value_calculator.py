import pandas as pd   
import matplotlib.pyplot as plt
import numpy as np 
import const
import os
import data_collection
import util
class growth_rate:
    def get_CAGR(l,period=10):
        
        l=l[-period:]
        n=len(l)-1
        CAGR=(float(l[n]/l[0])**(1/n))-1
        #print(f"CAGR: {CAGR}")
        return CAGR
    def get_AAGR(l,period=10):
        #print(f"full data: {l}")
        l = l[-period:] #last <period> amount of elements
        #print(l)
        n=len(l)
        AAGR=0
        #calculate AAGR, AAGR can't handle extreme drop 
        for indx,value in enumerate(l):
            AGR=0
            if indx==n-1: 
                continue
            #(new-old)/old
            AGR=(l[indx+1]-value)/value
            #print(f"AGR: {AGR}")

            AAGR+=AGR
        AAGR/=n-1
        #print(f"AAGR: {AAGR}")
        return AAGR
    def get_growth_rate_by_best_fit(df,value_col,year_col='year',period=10,plot=0):
        # Load the data from the CSV file
        #print(f"original df: {df}")
        df=df.tail(period)
        #print(f"new df: {df}")
        #exit(0)

        # Extract the year and eps data as numpy arrays
        years = df[year_col].to_numpy()
        eps = df[value_col].to_numpy()
        # Calculate the best fit line using numpy's polyfit function
        slope, intercept = np.polyfit(years, eps, 1)
        

        first_year_value=slope*(years[0])+intercept
        print(f"first_year: {years[0]}")
        print(f"first_year_value: {first_year_value}")
        
        last_year_value=slope*(years[len(years)-1])+intercept
        print(f"last_year: {years[len(years)-1]}")
        print(f"last_year_value: {last_year_value}")

        # first_year_value=slope*(years[0])+intercept
        # print(f"first_year: {years[0]}")
        # print(f"first_year_value: {first_year_value}")
        n=len(years)-1
        print(f"number of year: n: {n}")
        growth_rate= (float(last_year_value/first_year_value)**(1/n))-1
        # Print the slope and intercept of the best fit line
        print(f'Best fit line equation: y = {slope:.2f}x + {intercept:.2f}')
        if plot:
            # Plot the data and the best fit line using matplotlib
            plt.scatter(years, eps)
            plt.plot(years, slope * years + intercept, color='red')
            plt.xlabel('Year')
            plt.ylabel('value')
            plt.title('Best Fit Line ')
            plt.show()
        return growth_rate
class DCF:
    # def get_FCF_growth_rate(fcf):#TODO: remove this function after the new one
    #     fcf = fcf.sort_values(by='year')# order year by ascending order

    #     fcf_list=fcf['FCF'].tolist()
    #     aagr=growth_rate.get_AAGR(fcf_list)
    #     cagr=growth_rate.get_CAGR(fcf_list)
    #     best_fit_gr=growth_rate.get_growth_rate_by_best_fit(fcf,'FCF',plot=0)
    #     print(f"aagr: {aagr}")
    #     print(f"cagr: {cagr}")
    #     print(f"gr by best fit {best_fit_gr}")
    #     return aagr,cagr,best_fit_gr
    def get_FCF_growth_rate(cash_flow_df):
        print("get_FCF_growth_rate()")
        #create new col year
        cash_flow_df['year'] = cash_flow_df['date'].str[:4].astype(int)
        cash_flow_df=cash_flow_df.sort_values(by="year")
        #print(cash_flow_df)
        fcf_list=cash_flow_df["freeCashFlow"].tolist()
      
        aagr=growth_rate.get_AAGR(fcf_list,period=5)
        #print(aagr)
        
        cagr=growth_rate.get_CAGR(fcf_list,period=5)
        
        best_fit_gr=growth_rate.get_growth_rate_by_best_fit(cash_flow_df,"freeCashFlow",year_col='year',period=5,plot=1)
        print(f"aagr: {aagr}")
        print(f"cagr: {cagr}")
        print(f"gr by best fit {best_fit_gr}")
        return aagr,cagr,best_fit_gr
        

    # def fcf_from_cash_flow(cash_flow_df):
    #     """calculate fcf from cash flow statement df"""
    #     fcf = pd.DataFrame()
    #     fcf['year'] = cash_flow_df['fiscalDateEnding'].str[:4].astype(int)
    #     fcf['operatingCashflow']=cash_flow_df['operatingCashflow']
    #     fcf['capitalExpenditures']=cash_flow_df['capitalExpenditures']
    #     fcf['FCF'] = cash_flow_df['operatingCashflow'] - cash_flow_df['capitalExpenditures']
    #     return fcf

    def get_average_FCF_multiple(market_cap_df,fcf_df,period=-1):
        # Merge the two dataframes on the 'year' column
        
        merged_df = market_cap_df.merge(fcf_df, on='year')
   
        #print(merged_df)
        # Calculate the average FCF multiple
        # calculate FCF multiple for every year 
        if period!=-1: #period==-1 indicate using all years
            merged_df=merged_df.tail(period)
        print("""
              ***
              ***
              ***
              """)
        print(f"merged_df: {merged_df}")
        FCF_multiple_col = merged_df['market cap'] / merged_df['FCF']
        merged_df['FCF_multiple'] = FCF_multiple_col
        average_FCF_multiple = (merged_df['market cap'] / merged_df['FCF']).mean()

        #print(merged_df)
        print("average_FCF_multiple: ")
        print(average_FCF_multiple)
        return average_FCF_multiple
    def GetIntrinsicValue(current_CF,growth_rate,discount_rate,FCF_multiple,period=10):
        #1. get terminal value
        intrinsic_value=0
        terminal_value=current_CF*(1+growth_rate)**period*FCF_multiple
        discounted_terminal_value=terminal_value/(1+discount_rate)**period
        FCF_list=[ current_CF*((1+growth_rate)/(1+discount_rate))**i for i in range(1,period+1)]
        for fcf in FCF_list:
            intrinsic_value+=fcf
        
        intrinsic_value+=discounted_terminal_value
        # print(f"terminal value: {terminal_value}")
        # print(f"discounted_terminal_value: {discounted_terminal_value}")
        # print(f"intrinsic value: {intrinsic_value}")
        print(f"intrinsic value: {intrinsic_value}")
        return intrinsic_value
    def CreateRequiredFolders():
        util.CreateFolderIfNotExist(const.CSV_FILES)
        util.CreateFolderIfNotExist(const.FIN_STATEMENT_DIR)
        util.CreateFolderIfNotExist(const.CASH_FLOW_CSV_DIR)
        util.CreateFolderIfNotExist(const.BALANCE_SHEET_CSV_DIR)
        util.CreateFolderIfNotExist(const.INCOME_STATEMENT_CSV_DIR)
        
        util.CreateFolderIfNotExist(const.MARKET_CAP_DIR)
    def CollectRequiredCsv(cashflow_file_path,market_cap_file_path, ticker_code):
      
        if not os.path.exists(cashflow_file_path):
            print("cashflow not exist")
            #data_collection.alpha_vantage.download_cash_flow(ticker_code)
            data_collection.EOD.getFinStatements(ticker_code)
            print(f"{ticker_code} fin statements downloaded from EOD")
            
        else:
            print("cashflow exists")
        if not os.path.exists(market_cap_file_path):
            print("market cap not exist")
            data_collection.EOD.getHistoricalMarketCap(ticker_code)
            print(f"{ticker_code} historical market cap downloaded from EOD")
        else:
            print("market cap exists")
    def get_DCF_safety_margin(ticker_code):   
        DCF.CreateRequiredFolders()
        #check if folder exist, else: create folder
        cashflow_file_path=os.path.join(const.CASH_FLOW_CSV_DIR,f"{ticker_code}.csv")
        market_cap_file_path=os.path.join(const.MARKET_CAP_DIR,f"{ticker_code}.csv")
        #check if cashflow and market_cap file exist, else: collect csv file 
        DCF.CollectRequiredCsv(cashflow_file_path,market_cap_file_path,ticker_code)
        #completed test
        cash_flow_df=pd.read_csv(cashflow_file_path)
        market_cap_df=pd.read_csv(market_cap_file_path)
        #totalCashFromOperatingActivities 
        latest_year_FCF = cash_flow_df.iloc[0]['freeCashFlow']
        aagr,cagr,best_fit_gr=DCF.get_FCF_growth_rate(cash_flow_df)
        min_growth_rate=min(aagr,cagr,best_fit_gr)#TODO fix bug
        #annual_market_cap = quarterly_market_cap.groupby('year')['market_cap'].mean().reset_index()
        average_FCF_multiple=DCF.get_average_FCF_multiple(market_cap_df,fcf_df,period=5)
        intrinsic_value=DCF.GetIntrinsicValue(current_CF=latest_year_FCF,
                                              growth_rate=min_growth_rate,FCF_multiple=average_FCF_multiple,
                                              discount_rate=0.1,period=10)
        current_market_cap=data_collection.yfin.GetCurrentMarketCap(ticker_code)
        safety_margin=(intrinsic_value-current_market_cap)/intrinsic_value
        print(f"safety_margin: {safety_margin}")
        return safety_margin
# get_current_market_value=current_price*current_share #try to use yahoo finance to avoid quota limit
    #return check_safety_margin()
if __name__=="__main__":
    DCF.get_DCF_safety_margin("AAPL")
    #DCF.CreateRequiredFolders()
