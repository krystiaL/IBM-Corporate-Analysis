#---------------------------------------------------
#          LIBRARY AND MODULE IMPORTS
#---------------------------------------------------
import os
import numpy as np
import pandas as pd
import requests

from edgar_utils.params import *
#---------------------------------------------------


class Edgar():
    def __init__(self):
        self.sec_url = SEC_URL
        self.data_path = CSV_PATH

    def fetch_data(self, user_email: str):
        '''
        This function takes a user_email(str) as a parameter
        and returns all publicly listed companies' metadata.
        '''
        #store the response from API call
        headers = {'User-Agent': user_email}
        response = requests.get(self.sec_url, headers=headers)

        # Check if the request was successful
        if response.status_code == 200:
            print("Connection Successful!")
        else:
            print("Connection Failed:", response.status_code)

        #save response data as json
        data = response.json()

        #transform json into dataframe
        companies_df = pd.DataFrame.from_dict(data, orient='index')

        #modify data || add leading zeros to CIK no.
        companies_df['cik_str'] = companies_df['cik_str'].astype(str).str.zfill(10)

        #modify data || set company title to lowercase
        companies_df['title'] = companies_df['title'].str.lower()

        #write df into a csv file and save to data folder
        saved_df = companies_df.to_csv(CSV_PATH)

        # Check if the DataFrame was saved successfully
        if saved_df is None:
            print(f"Companies' metadata saved successfully in {CSV_PATH}")
        else:
            print("Failed to save metadata!")

    def fetch_ticker(self, company_name: str):
        '''
        This function takes a company name as a parameter
        and returns the possible company_ticker(str).
        '''
        #store the company input name and turn into lower case
        title = company_name.lower()

        metadata = pd.read_csv(CSV_PATH)

        title_data = metadata[metadata['title'].str.contains(title, case=False)]
        # ticker = []

        if not title_data.empty:  # Check if DataFrame is not empty
            # for index, row in title_data.iterrows():
            #     ticker.append({row['ticker']: row['title']})
            ticker_dict = {}  # Initialize an empty dictionary to store ticker-title pairs
            for index, row in title_data.iterrows():
                ticker_dict[row['ticker']] = row['title']

            ticker_df = pd.DataFrame(list(ticker_dict.items()), columns=['ticker', 'title'])
            print(ticker_df)
            return ticker_df
        else:
            print(f"No data found for company with name: {company_name}")
            return None

    def fetch_cik():
        '''
        This function takes the company_ticker(str) as a parameter
        and returns the listed company's 10-digit cik number.
        '''
        pass
