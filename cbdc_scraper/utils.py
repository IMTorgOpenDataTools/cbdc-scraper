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
        change = [chg for chg in changes if chg["property"]=="status"]

        country = item["country"] if hasattr(item, "country") else np.nan
        status = item["status"] if hasattr(item, "status") else np.nan
        bank = item["centralBank"] if hasattr(item, "centralBank") else np.nan
        currency = tag["currency"] if hasattr(tag, "currency") else np.nan
        purpose = item["type"] if hasattr(item, "type") else np.nan
        partner = item["technology"] if hasattr(item,"technology") else np.nan
        dlt = item["dlt"] if hasattr(item,"dlt") else np.nan
        tech = item["goals"] if hasattr(item,"goals") else np.nan
        summary = item["description"] if hasattr(item,"description") else np.nan
        change = 'Yes' if change else 'No'
        status_last_qtr = change["valueNew"] if hasattr(change,'valueNew') else np.nan

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
            Change = change,
            StatusLastQtr = status_last_qtr
        )
        recs.append(rec)
    return recs


def download_data(recs):
    """Download the data to a file."""
    download_path = Path("../downloads/").absolute()

    df = pd.DataFrame(recs)
    #TODO: determine what the output format should be.
    return True