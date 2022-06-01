#!/usr/bin/env python3
"""
Test the Output class.
"""

__author__ = "Jason Beach"
__version__ = "0.1.0"
__license__ = "MIT"

from cbdc_scraper.output import Output
from config._constants import (
    emails_file,
    report_dir,
    country_record
)



output = Output(
    report_dir = report_dir,
    emails_file = emails_file
    )



def test_send_notification():
    checks = output.send_notification()
    assert checks != []

def test_create_report():
    recs = []
    rec = country_record(
                Country = 'country',
                Status = 'status',
                CentralBank = 'bank',
                Currency = 'currency',
                Purpose = 'purpose',
                PartnerFirm = 'partner',
                DLT = 'dlt',
                Technology = 'tech',
                Summary = 'summary',
                Change = 'status_change',
                StatusLastQtr = 'status_last_qtr'
                )
    recs.append(rec)
    check = output.create_report(recs=recs)
    assert check == True