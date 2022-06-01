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
        "CentralBank",
        "Currency",
        "Purpose",
        "PartnerFirm",
        "DLT",
        "Technology",
        "Summary",
        "Change",
        "StatusLastQtr"
        ]
)

notable = ["China", "Jamaica", "Nigeria", "Russia"]