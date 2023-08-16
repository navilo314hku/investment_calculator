import json
import pandas as pd 


# If the 'date' column is redundant (as the date is also the index), you can drop it
    #df = df.drop(columns=['date'])
    #print(fin)
with open('AAPLfundamental.json') as json_file:#TODO: remove hardcode
    data = json.load(json_file)
    for key in data["Financials"]:
        print(key)
        # yearly_cashflow=data[
        # #yearly_cashflow=get_first_n_elements(yearly_cashflow,2) #TODO: remove this line for storing full statement
        # df = pd.DataFrame.from_dict(yearly_cashflow, orient='index')
        # print(df)
        

    # for key in fin["Cash_Flow"]:#key="Cash_Flow"
    #     #print(key)
    #     print(key)

    #print(data["Financials"]["Cash_Flow"])
    #for key in data["Financials"]["Cash_Flow"]["yearly"]:
     #   print(key)
    #print(data["Cash_Flow"])
    
