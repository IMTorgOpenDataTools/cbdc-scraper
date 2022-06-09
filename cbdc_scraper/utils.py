#!/usr/bin/env python3
"""
Utility functions
"""

__author__ = "Your Name"
__version__ = "0.1.0"
__license__ = "MIT"



import sys
from pathlib import Path

import requests
import datetime as dt
import numpy as np
import pandas as pd
pd.options.mode.chained_assignment = None  # default='warn'

sys.path.append(Path('config').absolute().as_posix() )
from _constants import (
    logger,
    output,
    country_record
)






def get_data_cbdc():
    """Get the data file from web page.
    Return dict of lists (records).
    """
    #constants
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

    #request data
    data = {}
    for k,v in files.items():
        url = f"{url_head}/{v}"
        try:
            resp = requests.get(url, headers=headers)
            if resp.status_code == 200:
                content = resp.json()
                data[k] = content
                logger.info("Data from cbdc is scraped.")
        except:
            logger.error("Data from cbdc is NOT scraped.")
            output.send_notification(error=True)
            exit()

    #corrections for 'currencies'
    df_currencies = pd.DataFrame(data["currencies"])
    df_currencies.sort_values(by=['country','digitalCurrency'], inplace=True)                      #<<<SELECTION_CHOICE
    df_currencies.drop_duplicates(subset=["country"], inplace=True)
    data["currencies"] = df_currencies.to_dict("records")
    
    return data



def get_data_atlantic():
    """Get `atlanticcouncil` data from `docs.google` api.
    Return dict of dataframes.
    """
    url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vQh27kpYjCRmNoWa4FEpWqLSxLLaqK_hlgqP6wGQLp8Pum7guAYS6i0qt6wIRAPvb5Up6-6wvmTN05s/pub?gid=0&single=true&output=csv"
    files = {"Atlantic": "CBDC Tracker Current Updates"}
    columns = ["Name", "Present Status", "Underlying technology"]            #TODO: add as primary Status and change from prev qtr status
    prev_qtr_month = {1:"February Status", 2:"April Status", 3:"June Status", 4:"October Status"}

    data_dict = {}
    try:
        loaded_df = pd.read_csv(url)

        current_qtr = pd.Timestamp(dt.date.today()).quarter
        columns.append( prev_qtr_month[current_qtr] )
        df = loaded_df[columns]
        column_replacements = {v:'Previous Status' for k,v in prev_qtr_month.items()}
        df.rename(columns=column_replacements, inplace=True)
        df["Changed Status"] = "No"
        df.loc[ df["Previous Status"] != df["Present Status"], "Changed Status"] = "Yes"

        k,v = list(files.items())[0]
        data_dict[k] = df.to_dict("records")
        logger.info("Data from atlantic council is scraped.")
    except:
        logger.error("failed to get `atlantic_council` data")
        output.send_notification(error=True)
        exit()

    return data_dict



def check_dataframe(df):
    """Check dataframe for basic problems"""
    columns = ["country", "mod_status", "centralBank", "tag", 
                "type", "technology", "Underlying technology", "dlt", 
                "description", "Changed Status", "Previous Status"
                ]
    idx_cols = ['country','mod_status']

    cols = all( [col in df.columns for col in columns] )
    obs = df.shape[0] > 0
    dups = df[df.duplicated(subset=idx_cols) == True].shape[0] == 0
    missing = df[df[idx_cols].isnull().any(axis=1)].shape[0] == 0  if obs == True else False

    checks = [cols, obs, dups, missing]
    check = all(checks) == True
    return check



def process_data(data_dict):
    """Transform data from original dataframe to output records.

    input: dict_of_records
    output: recs
    """
    recs = []
    df_currencies = pd.DataFrame(data_dict["currencies"])
    df_atlantic = pd.DataFrame(data_dict["Atlantic"])
    
    df = pd.merge(df_currencies, df_atlantic, 
            left_on="country", right_on="Name",
            suffixes=["","atlantic"],
            how = "left"
            )
    df["mod_status"] = df["Present Status"]
    df['mod_status'][df["mod_status"].isna()==True] = df['status']                      #<<<SELECTION_CHOICE

    check = check_dataframe(df)
    if not check:
        logger.error("dataframe did not meet `check_dataframe()` requirements")
        output.send_notification(error=True)
        exit()
    data_dict["merged"] = df.to_dict("records")

    for item in data_dict["merged"]:

        # additional tables (may not be useful)
        tag = [tag for tag in data_dict["tags"] if tag["name"] == item["tag"]][0]
        content = data_dict["history"]["content"][0]
        step1 = [hist for hist in content["tags"] 
                    if (hist["tag"]["name"]==item["tag"])
                    ]
        changes = step1[0]["changes"] if len(step1)>0 else []
        change_list = [chg for chg in changes if chg["property"]=="status"]

        # merged table
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
        status_change = item["Changed Status"]
        status_last_qtr = item["Previous Status"] if status_change == "Yes" else np.nan
        
        # append record
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