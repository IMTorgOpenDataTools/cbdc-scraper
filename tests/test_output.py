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

import pandas as pd
import numpy as np



output = Output(
    report_dir = report_dir,
    emails_file = emails_file
    )


def test_check_dataframes():
    df = pd.DataFrame()
    data_dict = {'df': df}
    check = output.check_dataframes(data_dict)
    assert check == False

def test_send_notification():
    checks = output.send_notification(error=True)
    assert checks != []

def test_create_report_fail():
    recs = []
    rec = country_record(
                Country="n/a",
                Status="n/a",
                StatusChange="n/a",
                StatusLastQtr="n/a",

                CentralBank="n/a",
                NationalBankPresence="n/a",
                BankNames="n/a",

                CurrencyName="n/a",
                Purpose="n/a",
                PartnerFirm="n/a",
                Software="n/a",
                LedgerType="n/a",
                BlockChainPermissions="n/a",

                Technology="n/a",
                Summary="n/a",
                )
    recs.append(rec)
    check = output.create_report(recs=recs)
    assert check == False

def test_create_report_succeed():
    recs = []
    rec = country_record(
                Country= "Nowhere",
                Status= "Good",
                StatusChange= np.nan,
                StatusLastQtr= np.nan,

                CentralBank= "First Central Bank",
                NationalBankPresence= np.nan,
                BankNames= np.nan,

                CurrencyName= "eDollar",
                Purpose= np.nan,
                PartnerFirm= np.nan,
                Software= np.nan,
                LedgerType= np.nan,
                BlockChainPermissions= np.nan,

                Technology= np.nan,
                Summary= np.nan,
                )
    recs.append(rec)
    check = output.create_report(recs=recs)
    assert check == True