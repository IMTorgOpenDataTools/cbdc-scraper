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


    def send_notification(self, error = False):
        """Send email notification that report is updated."""

        #constants
        subject = 'CBDC Tracker Update'
        df_emails = pd.read_csv(self.emails_file)

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

        df = pd.DataFrame(recs)
        df.to_excel(file_path, index=False)
        
        return True