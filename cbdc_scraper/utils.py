#!/usr/bin/env python3
"""
Utility functions
"""

__author__ = "Your Name"
__version__ = "0.1.0"
__license__ = "MIT"

from asyncio.log import logger
from pathlib import Path
from collections import namedtuple

import sys
import requests
import pandas as pd
import numpy as np
import xlsxwriter

sys.path.append(Path('config').absolute().as_posix() )
from _constants import (
    country_record
)






def get_data_cbdc():
    """Get the data file from web page.
    Return dict of lists (records).
    """
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


def get_data_atlantic():
    """Get `atlanticcouncil` data from `docs.google` api.
    Return dict of dataframes.
    """
    url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vQh27kpYjCRmNoWa4FEpWqLSxLLaqK_hlgqP6wGQLp8Pum7guAYS6i0qt6wIRAPvb5Up6-6wvmTN05s/pub?gid=0&single=true&output=csv"
    files = {"CBDC Tracker": "CBDC Tracker Current Updates"}
    columns = ["Name", "Present Status", "Underlying technology"]

    data_dict = {}
    try:
        loaded_df = pd.read_csv(url)
        df = loaded_df[columns]
        k,v = list(files.items())[0]
        data_dict[k] = df
    except:
        logger.info("failed to get `atlanticc_ouncil` data")

    return data_dict



def process_data(data_dict):
    """Transform data from original dataframe to output records.

    input: dict_of_df
    output: recs
    """
    recs = []
    df_currencies = pd.DataFrame(data_dict["currencies"])
    
    df = pd.merge(df_currencies, data_dict["CBDC Tracker"], 
            left_on="country", right_on="Name",
            suffixes=["","atlantic"],
            how = "left"
            )

    def check_launch_status(row):
        if row["Present Status"] == "Launched" and row["status"] != "Launched":
            return "Launched"
        else:
            return row["status"]

    df["mod_status"] = df.apply(check_launch_status, axis=1)
    data_dict["merged"] = df.to_dict("records")

    for item in data_dict["merged"]:
        tag = [tag for tag in data_dict["tags"] if tag["name"] == item["tag"]][0]
        content = data_dict["history"]["content"][0]
        step1 = [hist for hist in content["tags"] 
                    if (hist["tag"]["name"]==item["tag"])
                    ]
        changes = step1[0]["changes"] if len(step1)>0 else []
        change_list = [chg for chg in changes if chg["property"]=="status"]
        change = change_list[0] if len(change_list) > 0 else {}

        country = item["country"] if "country" in item.keys() else np.nan
        status = item["mod_status"] if "mod_status" in item.keys() else np.nan
        bank = item["centralBank"] if "centralBank" in item.keys() else np.nan
        currency = tag["currency"] if "currency" in tag.keys() else np.nan
        purpose = item["type"] if "type" in item.keys() else np.nan
        partner = item["technology"] if "technology" in item.keys() else np.nan
        software = item["Underlying technology"] if "Underlying technology" in item.keys() else np.nan
        dlt = item["dlt"] if "dlt" in item.keys() else np.nan
        tech = item["goals"] if "goals" in item.keys() else np.nan
        summary = item["description"] if "description" in item.keys() else np.nan
        status_change = 'Yes' if change else 'No'
        status_last_qtr = change["valueNew"] if "valueNew"in change.keys() else np.nan

        rec = country_record(
            Country = country,
            Status = status,
            StatusChange = status_change,
            StatusLastQtr = status_last_qtr,

            CentralBank = bank,
            NationalBankPresence = '',
            BankNames = '',

            CurrencyName = currency,
            Purpose = purpose,
            PartnerFirm = partner,
            Software = software,
            LedgerType = dlt,

            BlockChainPermissions = '',
            Technology = tech,
            Summary = summary,
        )
        recs.append(rec)
    return recs