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
from requests.adapters import HTTPAdapter, Retry
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
    url_head= "https://cbdctracker.org/api/"
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
    columns = {"country":"Country", "status":"Status", "Changed Status":"Changed Status", "valueOld":"Last Qtr Status",
                "centralBank":"Central Bank", 
                "digitalCurrency":"Digital Currency Name", "type":"Purpose",
                'technology':"Technology provider", "technologyName":"Software",
                'dlt':"Ledger Type", 'Permission':"Permission"
    }

    # requests session
    session = requests.Session()
    retries = Retry(total=5,
                    backoff_factor=0.1,
                    status_forcelist=[ 500, 502, 503, 504 ])
    session.mount(url_head, HTTPAdapter(max_retries=retries))


    #request data
    data = {}
    for key, url_stem in files.items():
        url = f"{url_head}/{url_stem}"
        try:
            resp = session.get(url, headers=headers)
            if resp.status_code == 200:
                content = resp.json()
                data[key] = content
                logger.info("Data from cbdc is scraped.")
        except:
            logger.error("Data from cbdc is NOT scraped.")
            output.send_notification(error=True)
            exit()

    #corrections for 'currencies'
    df_currencies = pd.DataFrame(data["currencies"])
    df_currencies.sort_values(by=['country','digitalCurrency'], inplace=True)                      #<<<SELECTION_CHOICE
    df_currencies.drop_duplicates(subset=["country"], inplace=True)

    # additional tables
    df_tags = pd.DataFrame(data['tags'])
    changed = []
    content = data["history"]["content"][0]
    for item in df_tags.to_dict('records'):
        step1 = [hist for hist in content["tags"] 
                    if (hist["tag"]["name"]==item["name"])
                    ]
        changes = step1[0]["changes"] if len(step1)>0 else []
        change_list = [chg for chg in changes if chg["property"]=="status"]
        if change_list != []:
            change_list[0]['name'] = item['name']
            changed.extend(change_list)
        else:
            continue
    df_changed = pd.DataFrame(changed)

    # merge tables
    df1 = pd.merge(df_currencies, df_tags, 
            left_on="tag", right_on="name",
            suffixes=["","tags"],
            how = "left"
            )
    df2 = pd.merge(df1, df_changed[['name','valueOld','valueNew']], 
            left_on="tag", right_on="name",
            suffixes=["","chgd"],
            how = "left"
            )
    df2["Changed Status"] = np.nan
    df2.loc[ ~df2["valueNew"].isnull(), "Changed Status"] = "Yes"
    df2['Permission'] = np.nan

    df2.rename(columns=columns, inplace=True)
    df3 = df2[ list(columns.values()) ]

    data_dict = {}
    data_dict["cbdc"] = df3.to_dict("records")
    return data_dict



def get_data_atlantic():
    """Get `atlanticcouncil` data from `docs.google` api.
    Return dict of dataframes.
    """
    url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vQh27kpYjCRmNoWa4FEpWqLSxLLaqK_hlgqP6wGQLp8Pum7guAYS6i0qt6wIRAPvb5Up6-6wvmTN05s/pub?gid=0&single=true&output=csv"
    files = {"Atlantic": "CBDC Tracker Current Updates"}

    qtr_month = {4:"February Status", 1:"April Status", 2:"June Status", 3:"October Status"}

    columns = {"Name":"Country", "Present Status": "Status",
                "Central Bank Name":"Central Bank", 
                "Name of CBDC":"Digital Currency Name", "Use case":"Purpose",
                'Technology partnership':"Technology provider", "Underlying technology":"Software",
                'Infrastructure: DLT or conventional':"Ledger Type", 'Access: token or account':"Permission"
    }
    
    def get_prev_qtr(current_qtr):
        match current_qtr:
            case 2 | 3 | 4: 
                prev_qtr = current_qtr - 1
            case 1: 
                prev_qtr = 4
        return prev_qtr


    data_dict = {}
    try:
        loaded_df = pd.read_csv(url)

        current_qtr = pd.Timestamp(dt.date.today()).quarter
        #current_qtr_month = qtr_month[current_qtr]
        #columns[current_qtr_month] = "Status"
        last_qtr_month = qtr_month[ get_prev_qtr(current_qtr) ]
        columns[last_qtr_month] = "Last Qtr Status"
        loaded_df.rename(columns=columns, inplace=True)
        df = loaded_df[ list(columns.values()) ]
        df["Changed Status"] = "No"
        df.loc[ df["Last Qtr Status"] != df["Status"], "Changed Status"] = "Yes"

        k,v = list(files.items())[0]
        data_dict[k] = df.to_dict("records")
        logger.info("Data from atlantic council is scraped.")
    except:
        logger.error("failed to get `atlantic_council` data")
        output.send_notification(error=True)
        exit()

    return data_dict



def process_data(data_dict):
    """Transform data from original dataframe to output records.

    input: dict_of_records
    output: recs
    """

    check = output.check_dataframes(data_dict)
    if not check:
        logger.error("dataframe did not meet `check_dataframe()` requirements")
        output.send_notification(error=True)
        exit()

    df_cbdc = pd.DataFrame(data_dict["cbdc"])
    df_atlantic = pd.DataFrame(data_dict["Atlantic"])  
    df = df_atlantic  
    '''
    df = pd.merge(df_atlantic, df_cbdc, 
            left_on="Country", right_on="Country",
            suffixes=["","-CBDC"],
            how = "left"
            )
    '''

    data_dict["merged"] = df.to_dict("records")
    return data_dict
    


def export_data(data_dict):
    """Export data records from pd.DataFrame to excel.
    """
    recs = []
    for item in data_dict["merged"]:

        # merged table
        country = item["Country"] if "Country" in item.keys() else np.nan
        status = item["Status"] if "Status" in item.keys() else np.nan
        bank = item["Central Bank"] if "Central Bank" in item.keys() else np.nan
        currency = item["Digital Currency Name"] if "Digital Currency Name" in item.keys() else np.nan          
        purpose = item["Purpose"] if "Purpose" in item.keys() else np.nan                                       
        partner = item["Technology provider"] if "Technology provider" in item.keys() else np.nan
        software = item["Software"] if "Software" in item.keys() else np.nan                                    
        dlt = item["Ledger Type"] if "Ledger Type" in item.keys() else np.nan                                                  
        permission = item["Permission"] if "Permission" in item.keys() else np.nan

        tech = item["goals"] if "goals" in item.keys() else np.nan
        summary = item["description"] if "description" in item.keys() else np.nan
        status_change = item["Changed Status"]
        status_last_qtr = item["Last Qtr Status"] if status_change == "Yes" else np.nan
        
        # append record
        rec = country_record(
            Country = country,
            Status = status,
            StatusChange = status_change,
            StatusLastQtr = status_last_qtr,

            CentralBank = bank,
            NationalBankPresence = '<edw_query>',
            BankNames = '<edw_query>',

            CurrencyName = currency,
            Purpose = purpose,
            PartnerFirm = partner,
            Software = software,
            LedgerType = dlt,

            BlockChainPermissions = permission,
            Technology = '<manual>',
            Summary = '<manual>',
        )
        recs.append(rec)
    return recs