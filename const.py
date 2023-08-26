import os 
CSV_FILES="csv_files"
FIN_STATEMENT_DIR=os.path.join(CSV_FILES,"fin_statements")
CASH_FLOW_CSV_DIR=os.path.join(FIN_STATEMENT_DIR,"cash_flow")
INCOME_STATEMENT_CSV_DIR=os.path.join(FIN_STATEMENT_DIR,"income_statement")
BALANCE_SHEET_CSV_DIR=os.path.join(FIN_STATEMENT_DIR,"balance_sheet")

MARKET_CAP_DIR=os.path.join(CSV_FILES,"market_cap")

STOCK_LIST_DIR=os.path.join(CSV_FILES,"stock_list")
DELISTED_STOCK_DIR=os.path.join(STOCK_LIST_DIR,"delisted")
AVAILABLE_STOCK_DIR=os.path.join(STOCK_LIST_DIR,"available")
PRICE_VOLUME_CSV_DIR=os.path.join(CSV_FILES,"price_volume") #data source from yfinance 
