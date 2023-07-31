from fredapi import Fred
def get_current_AAA_bond_yield():
        
    API_KEY="7960b0817f6f00396c2a130fdb10dcbd"
    fred = Fred(api_key=API_KEY)
    yield_data = fred.get_series('BAMLC0A1CAAAEY')
    #print(type(yield_data))
    #print(yield_data.tail(1))
    #yield_data = fred.get_series('AAA')
    return yield_data.tail(1)

