#!/usr/bin/env python3
"""
Output to excel, email notifications, etc.
"""

__author__ = "Your Name"
__version__ = "0.1.0"
__license__ = "MIT"


from asyncio.log import logger
from pathlib import Path
import subprocess
from subprocess import PIPE, STDOUT
from collections import namedtuple

import pandas as pd
import numpy as np



class Output:

    def __init__(self, report_dir = None, emails_file = None):
        if report_dir is None:
            report_dir = './downloads'
        self.report_dir = Path(report_dir).absolute()
        self.report_dir.mkdir(parents=True, exist_ok=True)
        self.emails_file = emails_file

    
    def check_dataframes(self, data_dict):
        """Check both dataframes for basic problems, and compare for validity.
        """

        columns_before_processing = ['Country', 'Status', 'Changed Status', 'Last Qtr Status', 
                    'Central Bank', 'Digital Currency Name', 'Purpose', 
                    'Technology provider', 'Software', 'Ledger Type', 'Permission']
        columns_after_processing = ['Country', 'Status', 'StatusChange', 'StatusLastQtr', 
                    'CentralBank', 'NationalBankPresence', 'BankNames', 
                    'CurrencyName', 'Purpose', 'PartnerFirm', 'Software', 
                    'LedgerType', 'BlockChainPermissions', 'Technology', 'Summary']
        idx_cols = ['Country','Status']

        results = []
        for key, recs in data_dict.items():
            df = pd.DataFrame(recs)
            try:
                cols = all( [col in df.columns for col in columns_before_processing] )
                if cols == False:
                    cols = all( [col in df.columns for col in columns_after_processing] )
                obs = df.shape[0] > 0
                dups = df[df.duplicated(subset=idx_cols) == True].shape[0] == 0
                missing = df[df[idx_cols].isnull().any(axis=1)].shape[0] == 0  if obs == True else False
                checks = [cols, obs, dups, missing]
                check = all(checks) == True
                results.append(check)
            except:
                logger.error("error in checking dfs")
                results.append(False)
        result = all(results) == True
        return result


    def send_notification(self, error = False):
        """Send email notification that report is updated."""

        #constants
        subject = 'CBDC Tracker Update'
        df = pd.read_csv(self.emails_file)
        df_emails = df[df['notify'] == True]

        #scenarios
        body_success = b'''Dear Sir/Ma'am, this is a notification that the Central Bank Digital Currency 
                (CBDC) Tracker report is updated.  You can find it in the following shared drive: 
                `\hqfile01\sec_edgar\cbdc_tracker\`.
                '''
        emails_success = df_emails['address'].tolist()

        body_fail = b'''*** There was an error ***'''
        df_admin_only = df_emails[df_emails['admin']==True]
        emails_fail = df_admin_only['address'].tolist()

        if not error:
            body_content = body_success
            emails = emails_success
        else:
            body_content = body_fail
            emails = emails_fail

        #execute
        checks = []
        bashCommand = ["mailx", "-s", subject, *emails]
        try:
            p = subprocess.Popen(bashCommand, stdin=PIPE, stdout=PIPE, stderr=STDOUT)
            result = p.communicate(input=body_content)[0]
            checks.append(result)
        except:
            print("failed to send email notification.")

        return checks


    def create_report(self, recs):
        """Download the data to a file."""
        download_path = self.report_dir
        file_path = download_path / 'monthly_report.xlsx'

        data_dict = {'recs': recs}
        result = self.check_dataframes(data_dict)
        if result:
            df = pd.DataFrame(recs)
            df.to_excel(file_path, index=False)
            return True
        else:
            return False
        