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
from collections import namedtuple

import requests
import pandas as pd
import numpy as np
import xlsxwriter



class Output:

    def __init__(self, report_dir = None, emails_file = None):
        self.report_dir = report_dir
        self.emails_file = emails_file
        pass


    def send_notification(self):
        """Send email notification that report is updated."""

        subject = 'SEC Report Update'
        body = "Dear Sir/Ma'am, this is a notification that the SEC earnings report is updated.  You can find it in the following shared drive: `\hqfile01\sec`."

        df_emails = pd.read_csv(self.emails_file)
        emails = df_emails['address'].tolist()

        checks = []
        for email in emails:
            #test = subprocess.Popen(, stdout=subprocess.PIPE)
            bashCommand = ["mailx", "-s", subject, email, "<", body]
            test = subprocess.run(bashCommand, capture_output=True, text=True)
            output = test.communicate()[0]
            checks.append(output)

        return checks


    def create_report(self, recs):
        """Download the data to a file."""
        download_path = Path( self.report_dir ).absolute()
        file_path = download_path / 'monthly_report.xlsx'

        df = pd.DataFrame(recs)
        df.to_excel(file_path, index=False)
        
        return True