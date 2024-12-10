#---------------------------------------------------
#          LIBRARY AND MODULE IMPORTS
#---------------------------------------------------
import os
import shutil

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

        #modify data || add leading zeros to CIK and typecast the entire column to str
        companies_df['cik_str'] = companies_df['cik_str'].astype(str).str.zfill(10)
        companies_df['cik_str'] = companies_df['cik_str'].astype(str)

        #modify data || set company title to lowercase
        companies_df['title'] = companies_df['title'].str.lower()

        try:
            companies_df.to_csv(CSV_PATH)
            print(f"Companies' metadata saved successfully in {CSV_PATH}")
        except Exception as e:
            print("Failed to save metadata!", e)

        return companies_df


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

    def fetch_cik(self, ticker: str):
        '''
        This function takes the company_ticker(str) as a parameter
        and returns the listed company's 10-digit cik number.
        '''
        metadata = pd.read_csv(CSV_PATH)
        #retain leading zeros for the 10-digit cik as str
        metadata['cik_str'] = metadata['cik_str'].astype(str).str.zfill(10)

        #search for cik using unique company ticker
        company_data = metadata.loc[metadata['ticker'] == ticker]
        company_cik = company_data['cik_str'].iloc[0]

        return company_cik

    def fetch_form_submissions(self, cik: str,
                               user_email: str,
                               form_type: str
                               ):
        '''
        filing submission info request
        '''
        ####### parameters ######
        '''
        form_type = ['8-K', 'PX14A6G', 'ARS', 'DEFA14A', 'DEF 14A', '10-K', '4',
       'SC 13G/A', '424B5', 'FWP', '424B3', 'S-3ASR', '3', '10-Q', '11-K',
       'SD', '25-NSE', 'CERT', '8-A12B', 'UPLOAD', 'CORRESP', '8-K/A',
       'IRANNOTICE', 'SC 13G', 'S-8', 'S-8 POS', '3/A', '4/A']
        '''


        headers = {'User-Agent': user_email}
        response = requests.get(
                    f'https://data.sec.gov/submissions/CIK{cik}.json',
                    headers=headers
                    )
        submission = response.json()['filings']['recent']

        submission_df = pd.DataFrame.from_dict(submission)
        #filter df depending on specific form
        filtered_df = submission_df.loc[submission_df['form'] == form_type]

        return filtered_df

    def fetch_facts_data(self, cik: str, user_email: str):
        '''
        company facts request
        '''
        headers = {'User-Agent': user_email}
        response = requests.get(
                    f'https://data.sec.gov/api/xbrl/companyfacts/CIK{cik}.json',
                    headers=headers
                    )
        facts = response.json()

        return facts

    def fetch_common_stock(self, facts, fy):
        '''
        DEI
        '''
        ####### parameters ######
        '''
        facts = json file from fetch_facts_data function
        fy = for the year ended
        
        '''
        pass

    def fetch_acc_items():
        '''
        US-GAAP
        '''
        pass
