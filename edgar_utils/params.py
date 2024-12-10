import os

##################  VARIABLES  ##################
SEC_URL = "https://www.sec.gov/files/company_tickers.json"
EXAMPLE_EMAIL = 's1d102100128@toyo.jp'
SOURCE_PATH = "ticker_metadata.csv"
CSV_PATH = os.path.join("data", "ticker_metadata.csv")

##################  CONSTANTS  #####################
USER_AGENT = os.environ.get("EMAIL")
