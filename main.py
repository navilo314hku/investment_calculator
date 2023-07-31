#safety margin calculator
from const import *
import pandas as pd
from growth_rate import *
import os 
MARKET_PRICE=56
# Load the CSV file into a DataFrame
def eps_intrinsic_value(growth_rate):
    past_12_month_eps=0.68+0.45+0.69+0.7
    #Intrinsic value =current_eps*(8.5+2*expected_annual_growth):Intr_value
    Intri_val=past_12_month_eps*(8.5+2*growth_rate)*4.4/Y
    return Intri_val


if __name__=="__main__":
    df = pd.read_csv(os.path.join("csv_files","cash_flow","ALLY.csv"))
    list = df['FCF'].tolist()
    list.reverse()
    print(f"AAGR {get_AAGR(list)}")   
    print(f"CAGR {get_CAGR(list)}")
    growth_rate=get_growth_rate_by_best_fit(df,plot=1)
    print(f"Growth rate by best fit: {growth_rate}")

    #print(get_intrinsic_value(growth_rate))
#print(eps_list)
# Print the DataFrame
