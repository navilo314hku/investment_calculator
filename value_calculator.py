import pandas as pd   
import matplotlib.pyplot as plt
import numpy as np 
import const
import os
class growth_rate:
    def get_CAGR(list):
        n=len(list)-1
        CAGR=(float(list[n-1]/list[0])**(1/n))-1
        CAGR=CAGR*100
        #print(f"CAGR: {CAGR}")
        return CAGR
    def get_AAGR(list):
        n=len(list)
        AAGR=0
        #calculate AAGR, AAGR can't handle extreme drop 
        for indx,eps in enumerate(list):
            AGR=0
            if indx==n-1: 
                continue
            #(new-old)/old
            AGR=(list[indx+1]-eps)/eps
            AGR=AGR*100
            #print(f"AGR: {AGR}")

            AAGR+=AGR
        AAGR/=n
        #print(f"AAGR: {AAGR}")
        return AAGR
    def get_growth_rate_by_best_fit(df,value_col,year_col='year',plot=0):
        # Load the data from the CSV file
    

        # Extract the year and eps data as numpy arrays
        years = df[year_col].to_numpy()
        eps = df[value_col].to_numpy()
        # Calculate the best fit line using numpy's polyfit function
        slope, intercept = np.polyfit(years, eps, 1)
        print(f"years[len(years)-1]: {years[len(years)-1]}")
        last_year_value=slope*(years[len(years)-1])+intercept
        print(f"last_year_value: {last_year_value}")
        
        first_year_value=slope*(years[0])+intercept
        print(f"first_year_value: {first_year_value}")
        n=len(years)-1
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
        return growth_rate*100

def get_FCF_growth_rate(fcf):
    fcf = fcf.sort_values(by='year')# order year by ascending order
    fcf_list=fcf['FCF'].tolist()
    aagr=growth_rate.get_AAGR(fcf_list)
    cagr=growth_rate.get_CAGR(fcf_list)
    best_fit_gr=growth_rate.get_growth_rate_by_best_fit(fcf,'FCF',plot=0)
    print(f"aagr: {aagr}")
    print(f"cagr: {cagr}")
    print(f"gr by best fit {best_fit_gr}")
    return aagr,cagr,best_fit_gr
def fcf_from_cash_flow(cash_flow_df):
    """calculate fcf from cash flow statement df"""
    fcf = pd.DataFrame()
    fcf['year'] = cash_flow_df['fiscalDateEnding'].str[:4].astype(int)
    fcf['operatingCashflow']=cash_flow_df['operatingCashflow']
    fcf['capitalExpenditures']=cash_flow_df['capitalExpenditures']
    fcf['FCF'] = cash_flow_df['operatingCashflow'] - cash_flow_df['capitalExpenditures']
    return fcf
def get_quarterly_market_cap(price_volume_df):
    quarterly_market_cap = pd.DataFrame()
    quarterly_market_cap['year'] = price_volume_df['Date'].str[:4].astype(int)
    quarterly_market_cap['market_cap'] = price_volume_df['Close'] * price_volume_df['Volume']
    print("writing csv")
    quarterly_market_cap.to_csv("tmp.csv",index=0)
    return quarterly_market_cap
def get_average_FCF_multiple(market_cap_df,fcf_df):
    # Merge the two dataframes on the 'year' column
    merged_df = market_cap_df.merge(fcf_df, on='year')
    #print(merged_df)
    # Calculate the average FCF multiple
    # calculate FCF multiple for every year 
    FCF_multiple_col = merged_df['market_cap'] / merged_df['FCF']
    merged_df['FCF_multiple'] = FCF_multiple_col
    average_FCF_multiple = (merged_df['market_cap'] / merged_df['FCF']).mean()

    #print(merged_df)
    #print(average_FCF_multiple)
    return average_FCF_multiple
def get_DCF_safety_margin(ticker_code):
    #read cash flow and price_volume csv
    cash_flow_df=pd.read_csv(os.path.join(const.CASH_FLOW_CSV_DIR,f"{ticker_code}.csv"))
    price_volume_df=pd.read_csv(os.path.join(const.PRICE_VOLUME_CSV_DIR,f"{ticker_code}.csv"))
    quarterly_market_cap=get_quarterly_market_cap(price_volume_df)
    #print(quarterly_market_cap)


    fcf_df=fcf_from_cash_flow(cash_flow_df)
    latest_year_FCF = fcf_df.iloc[0]['FCF']
    aagr,cagr,best_fit_gr=get_FCF_growth_rate(fcf_df)
    annual_market_cap = quarterly_market_cap.groupby('year')['market_cap'].mean().reset_index()
    average_FCF_multiple=get_average_FCF_multiple(annual_market_cap,fcf_df)
    
# get_terminal_value
# get_intrinsic_value=discounted_terminal_value
# get_current_market_value=current_price*current_share #try to use yahoo finance to avoid quota limit
    #return check_safety_margin()
if __name__=="__main__":
    get_DCF_safety_margin("AAPL")
