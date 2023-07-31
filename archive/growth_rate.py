import pandas as pd  
import matplotlib.pyplot as plt
import numpy as np 
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

def get_growth_rate_by_best_fit(eps_df,plot=1):
    df=eps_df
    # Load the data from the CSV file
 

    # Extract the year and eps data as numpy arrays
    years = df['year'].to_numpy()
    eps = df['FCF'].to_numpy()
    # Calculate the best fit line using numpy's polyfit function
    slope, intercept = np.polyfit(years, eps, 1)
    first_year_value=slope*(years[len(years)-1])+intercept
    last_year_value=slope*(years[0])+intercept
    n=len(years)-1
    growth_rate= ((last_year_value/first_year_value)**(1/n))-1
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

