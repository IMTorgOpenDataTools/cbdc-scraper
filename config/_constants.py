#!/usr/bin/env python3
"""
Constants used throughout app.
"""

import sys
from pathlib import Path
import logzero
from logzero import logger
from collections import namedtuple

sys.path.append(Path('cbdc_scraper').absolute().as_posix() )
from output import Output



emails_file = './config/emails.csv'
report_dir = './downloads'
logging_dir = './downloads/process.log'

logzero.loglevel(logzero.INFO)                                           #set a minimum log level: debug, info, warning, error
logzero.logfile(logging_dir, maxBytes=1000000, backupCount=3)            #set rotating log file

output = Output(
    report_dir = report_dir,
    emails_file = emails_file
    )



country_record = namedtuple(
    "CountryRecord",
        ["Country",
        "Status",
        "StatusChange",
        "StatusLastQtr",

        "CentralBank",
        "NationalBankPresence",
        "BankNames",

        "CurrencyName",
        "Purpose",
        "PartnerFirm",
        "Software",
        "LedgerType",
        "BlockChainPermissions",

        "Technology",
        "Summary",
        ]
)

notable = ["China", "Jamaica", "Nigeria", "Russia"]