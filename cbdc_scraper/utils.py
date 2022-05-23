#!/usr/bin/env python3
"""
Module Docstring
"""

__author__ = "Your Name"
__version__ = "0.1.0"
__license__ = "MIT"

from pathlib import Path
from collections import namedtuple

import requests
import pandas as pd
import numpy as np
import xlsxwriter



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




def get_data():
    """Get the data file from web page."""
    url_head= "https://cbdctracker.org/api"
    files = {"currencies":"currencies", 
            "tags":"/currencies/tags", 
            "technologies":"technologies",
            "columns":"currencies/columns",
            "history":"history-of-changes?page=0&size=1"
            }
    
    headers = {
        "User-Agent": "Test User",
        "Accept-Encoding": "gzip, deflate",
        "Host": "efts.sec.gov"
        }

    data = {}
    for k,v in files.items():
        url = f"{url_head}/{v}"
        resp = requests.get(url, headers=headers)
        if resp.status_code == 200:
            content = resp.json()
            data[k] = content
    
    return data


def process_data(data_dict):
    recs = []
    for item in data_dict["currencies"]:
        tag = [tag for tag in data_dict["tags"] if tag["name"] == item["tag"]][0]
        content = data_dict["history"]["content"][0]
        step1 = [hist for hist in content["tags"] 
                    if (hist["tag"]["name"]==item["tag"])
                    ]
        changes = step1[0]["changes"] if len(step1)>0 else []
        change_list = [chg for chg in changes if chg["property"]=="status"]
        change = change_list[0] if len(change_list) > 0 else {}

        country = item["country"] if "country" in item.keys() else np.nan
        status = item["status"] if "status" in item.keys() else np.nan
        bank = item["centralBank"] if "centralBank" in item.keys() else np.nan
        currency = tag["currency"] if "currency" in tag.keys() else np.nan
        purpose = item["type"] if "type" in item.keys() else np.nan
        partner = item["technology"] if "technology" in item.keys() else np.nan
        dlt = item["dlt"] if "dlt" in item.keys() else np.nan
        tech = item["goals"] if "goals" in item.keys() else np.nan
        summary = item["description"] if "description" in item.keys() else np.nan
        status_change = 'Yes' if change else 'No'
        status_last_qtr = change["valueNew"] if "valueNew"in change.keys() else np.nan

        rec = country_record(
            Country = country,
            Status = status,
            CentralBank = bank,
            Currency = currency,
            Purpose = purpose,
            PartnerFirm = partner,
            DLT = dlt,
            Technology = tech,
            Summary = summary,
            Change = status_change,
            StatusLastQtr = status_last_qtr
        )
        recs.append(rec)
    return recs


def download_data(recs):
    """Download the data to a file."""
    download_path = Path("./downloads/").absolute()
    file_path = download_path / 'monthly_report.csv'

    df = pd.DataFrame(recs)
    df.to_csv(file_path, index=False)
    #TODO: determine what the output format should be.

    return True