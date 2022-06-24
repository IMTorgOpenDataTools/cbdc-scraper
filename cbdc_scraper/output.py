#!/usr/bin/env python3
"""
Output to excel, email notifications, etc.
"""

__author__ = "Your Name"
__version__ = "0.1.0"
__license__ = "MIT"

import datetime
from pathlib import Path
import subprocess
from subprocess import PIPE, STDOUT
from collections import namedtuple

import pandas as pd
import numpy as np



class Output:

    def __init__(self, report_copy_dir = None, report_dir = None, emails_file_or_dictlist = None, email_network_drive = None, logger = None):

        if report_copy_dir is None:
            report_copy_dir = './downloads'
        self.report_copy_dir = Path(report_dir).absolute()
        self.report_copy_dir.mkdir(parents=True, exist_ok=True)

        if report_dir is None:
            report_dir = './downloads'
        self.report_dir = Path(report_dir).absolute()
        self.report_dir.mkdir(parents=True, exist_ok=True)

        if type(emails_file_or_dictlist) == list:
            self.emails_df = pd.DataFrame(emails_file_or_dictlist)
        elif type(emails_file_or_dictlist) == str:
            self.emails_df = pd.read_csv(emails_file_or_dictlist)
        else:
            logger.debug('Output class must be instantiated with file or dict-list')
            exit()
        self.email_network_drive = email_network_drive
        self.logger = logger

    
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
                self.logger.error("error in checking dfs")
                results.append(False)
        result = all(results) == True
        return result


    def send_notification(self, error = False):
        """Send email notification that report is updated."""

        #constants
        subject = 'CBDC Tracker Update'
        df = self.emails_df
        df_emails = df[df['notify'] == True]

        #scenarios
        template_success = f'''\\
                Dear Sir/Ma'am,\\
                This is a notification that the Central Bank Digital Currency 
                (CBDC) Tracker report is updated.  You can find it in the following shared drive:\\ 
                {self.email_network_drive}\\
                '''
        body_success = bytes(template_success, encoding='utf8')
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
            self.logger.error("failed to send email notification.")
            
        return checks


    def create_report(self, recs):
        """Download the data to a file."""

        #copy for archives
        year_wk = f'{datetime.datetime.now().year}_{datetime.datetime.now().isocalendar().week}'
        copy_path = self.report_dir
        copy_file_path = copy_path / f'monthly_report-{year_wk}.csv'

        #output to network drive
        output_path = self.report_dir
        output_file_path = output_path / 'monthly_report.xlsx'

        data_dict = {'recs': recs}
        result = self.check_dataframes(data_dict)
        if result:
            df = pd.DataFrame(recs)
            df.to_csv(copy_file_path, index=False)
            df.to_excel(output_file_path, index=False)
            return True
        else:
            return False