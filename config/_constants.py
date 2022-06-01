#!/usr/bin/env python3
"""
Constants used throughout app.
"""

from collections import namedtuple


emails_file = './config/emails.csv'
report_dir = './downloads'



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