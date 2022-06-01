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

import requests
import pandas as pd
import numpy as np
import xlsxwriter



class Output:

    def __init__(self, report_dir = None, emails_file = None):
        if report_dir is None:
            report_dir = './downloads'
        self.report_dir = Path(report_dir).absolute()
        self.report_dir.mkdir(parents=True, exist_ok=True)
        self.emails_file = emails_file


    def send_notification(self):
        """Send email notification that report is updated."""

        subject = 'CBDC Tracker Update'
        body = b"Dear Sir/Ma'am, this is a notification that the Central Bank Digital Currency (CBDC) Tracker report is updated.  You can find it in the following shared drive: `\hqfile01\sec_edgar\cbdc_tracker\`."

        df_emails = pd.read_csv(self.emails_file)
        emails = df_emails['address'].tolist()

        checks = []
        bashCommand = ["mailx", "-s", subject, *emails]
        try:
            p = subprocess.Popen(bashCommand, stdin=PIPE, stdout=PIPE, stderr=STDOUT)
            result = p.communicate(input=body)[0]
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