import requests
import pandas as pd
import timeit
from datetime import datetime, timezone, timedelta
import logging
from dotenv import dotenv_values
import sys

# from modules.send_email_alert import send_email
from modules.check_item_token import check_token_status

# from modules.endpoints import sf_endpoints
import json
import os
import pyarrow.parquet as pq
import pyarrow as pa
import time
import re
from modules.sql_calls.team_time_cards_max_start_date import get_team_time_cards_max_start_date


script_name = os.path.splitext(os.path.basename(__file__))[0]
# Get the absolute path of the current script
script_path = os.path.abspath(__file__)
# Get the directory containing the current script
base_path = os.path.dirname(script_path)

config = dotenv_values(f"{base_path}/.env")

region_file_path = f"{base_path}/files/company_region_id.json"

log_path = f"{base_path}/logs/"

# log_path = "C:/Users/eviadmin/Documents/Datawarehouse/test_schedule_scripts/From_BC/python/logs/"
output_folder = "prod"
# output_path = f'C:/Users/eviadmin/Documents/Datawarehouse/python_scripts/DataLake/{output_folder}/files/'
output_path = (
    f"E:/Datawarehouse/python_scripts_output/DataLake/{output_folder}/from_adp/"
)



# logger
logger = logging.getLogger(__name__)

def setup_logging(log_file):
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    if not logger.handlers:
        handler = logging.FileHandler(log_file)
        formatter = logging.Formatter(
            # "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
            "%(asctime)s | %(levelname)s | %(name)s | %(funcName)s | %(message)s"
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
    
        # Silence noisy libraries
    logging.getLogger("urllib3").setLevel(logging.WARNING)
    logging.getLogger("requests").setLevel(logging.WARNING)

    return logger


def export_to_files(df, file_name, export_selection=[False, True, True]):
    if export_selection[0]:
        logger.debug(f"Exporting to CSV: {file_name}")
        df.to_csv(
            f"{output_path}/csv/{file_name}.csv.gz", index=False, compression="gzip"
        )
    if export_selection[1]:
        logger.debug(f"Exporting to Parquet: {file_name}")
        df.to_parquet(f"{output_path}/parquet/{file_name}.parquet", index=False)
    if export_selection[2]:
        logger.debug(f"Exporting to Excel: {file_name}")
        df.to_excel(f"{output_path}/excel/{file_name}.xlsx", index=False)


def add_dw_columns(df, date_time, endpoint, region, erp="Salesforce"):
    # df["DW_EVI_BU"] = company
    # df["DW_ERP_Company"] = company
    df["DW_ERP_System"] = erp
    df["DW_Timestamp"] = date_time.strftime("%Y-%m-%d %H:%M:%S.%f")
    df["DW_ERP_Source_Table"] = endpoint
    df["Region_Id"] = regions_list[region]
    df["region"] = region
    return df


def get_workers_list():
    active_token = check_token_status()
    # API endpoint
    url = "https://accounts.adp.com/hr/v2/workers?skip=0&top=1000"

    # Build headers with the token
    headers = {
        "Authorization": f"Bearer {active_token['access_token']}",
        "Accept": "application/json",
    }

    # Cert + key paths (from your .env)
    CLIENT_CERT = config["adp_client_cert"]
    CLIENT_KEY = config["adp_client_key"]

    response = requests.get(
        url,
        headers=headers,
        cert=(CLIENT_CERT, CLIENT_KEY),  # mTLS
        verify=True,  # or path to ADP CA if provided
    )

    # Raise exception if request failed
    response.raise_for_status()

    data = response.json()

    # Save JSON to file with timestamp
    timestamp = datetime.now().strftime("%Y%m%d")
    filename = f"{base_path}/files/workers_{timestamp}.json"

    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)

    print(f"✅ Workers data exported to {filename}")
    return data


def fetch_all_workers(
    region, date_time, cert=None, key=None, top=50, pause=0.1, max_pages=10000
):
    """
    Fetch all workers using $top/$skip pagination.
      - cert,key: paths to client cert and private key for mTLS, or None
      - top: page size (ADP default is 50; synchronous calls return max 50)
      - pause: small sleep between requests to be polite
    Returns: list of worker dicts
    """
    logger.info(f"Starting function")
    
    active_token = check_token_status(region.lower())
    CLIENT_CERT = config[f"{region.lower()}_adp_client_cert"]
    CLIENT_KEY = config[f"{region.lower()}_adp_client_key"]

    headers = {
        "Authorization": f"Bearer {active_token['access_token']}",
        "Accept": "application/json",
    }

    base_url = "https://accounts.adp.com/hr/v2/workers"
    all_workers = []
    skip = 0
    page = 0

    while True:
        url = f"{base_url}?$top={top}&$skip={skip}"
        print(f"➡️ Fetching: {url}")

        resp = requests.get(
            url, headers=headers, cert=(CLIENT_CERT, CLIENT_KEY), verify=True
        )

        if resp.status_code == 200:
            data = resp.json()
            batch = data.get("workers") or []
            if not batch:
                print("⚠️ Empty workers array, stopping.")
                break

            all_workers.extend(batch)

        elif resp.status_code == 204:
            print("✅ No content (204) – reached the end of records.")
            break

        else:
            print(f"❌ Unexpected status {resp.status_code}: {resp.text}")
            break  # stop loop on error

        page += 1
        skip += top

        if page >= max_pages:
            raise RuntimeError(
                f"Reached max_pages ({max_pages}); stopping to avoid infinite loop."
            )

        time.sleep(pause)

    # Save JSON to file with timestamp
    # timestamp = datetime.now().strftime("%Y%m%d")
    filename = f"{base_path}/files/{region}_workers_{date_time.strftime('%m%d%y')}.json"

    with open(filename, "w", encoding="utf-8") as f:
        json.dump(all_workers, f, indent=4)

    print(f"📁 Workers data exported to {filename}")

    return all_workers


def get_field(d, path, default=None):
    """Traverse nested dict by path (list of keys)."""
    for key in path:
        if d is None or key not in d:
            return default
        d = d[key]
    return d


def read_json_file_workers():
    # Load JSON file
    with open(f"{base_path}/files/workers_20250912.json", "r", encoding="utf-8") as f:
        workers_data = json.load(f)

    # Print top-level keys
    # print("Top-level keys:", workers_data.keys())
    # print("workers keys:", workers_data["workers"][0].keys())
    # print("workers keys:",
    #       workers_data["workers"][0]["workAssignments"][0].keys())
    # exit()

    workers = workers_data["workers"]

    # Flatten into list of rows
    rows = []
    for w in workers:
        # Worker-level fields
        associateOID = w.get("associateOID")
        workerID = get_field(w, ["workerID", "idValue"])
        statusCode = get_field(w, ["workerStatus", "statusCode", "codeValue"])
        originalHireDate = get_field(w, ["workerDates", "originalHireDate"])
        terminationDate = get_field(w, ["workerDates", "terminationDate"])
        formattedName = get_field(w, ["person", "legalName", "formattedName"])
        familyName1 = get_field(w, ["person", "legalName", "familyName1"])
        middleName = get_field(w, ["person", "legalName", "middleName"])
        givenName = get_field(w, ["person", "legalName", "givenName"])

        # Work assignments (list → expand)
        assignments = w.get("workAssignments", [])
        if assignments:
            for wa in assignments:
                row = {
                    "associateOID": associateOID,
                    "workerID": workerID,
                    "statusCode": statusCode,
                    "originalHireDate": originalHireDate,
                    "terminationDate": terminationDate,
                    "formattedName": formattedName,
                    "familyName": familyName1,
                    "middleName": middleName,
                    "givenName": givenName,
                    "assignmentStatus": get_field(
                        wa, ["assignmentStatus", "statusCode", "codeValue"]
                    ),
                    "assignmentStatusName": get_field(
                        wa, ["assignmentStatus", "statusCode", "longName"]
                    ),
                    "jobCode": get_field(wa, ["jobCode", "codeValue"]),
                    "jobTitle": wa.get("jobTitle"),
                    "positionID": wa.get("positionID"),
                }
                rows.append(row)
        else:
            # Worker with no assignments → still include row
            rows.append(
                {
                    "associateOID": associateOID,
                    "workerID": workerID,
                    "statusCode": statusCode,
                    "originalHireDate": originalHireDate,
                    "terminationDate": terminationDate,
                    "assignmentStatus": None,
                    "assignmentStatusName": None,
                    "jobCode": None,
                    "jobTitle": None,
                    "positionID": None,
                }
            )

    # Convert to DataFrame
    df = pd.DataFrame(rows)
    print(df)
    df.to_excel(f"{base_path}/files/workers.xlsx", index=False)
    df.to_parquet(f"{base_path}/files/workers.parquet", index=False)

    # for worker in workers_data["workers"]:
    #     print(worker['associateOID'])
    #     print(len(worker["workAssignments"]))

    # # If it's a dict with nested 'workers' or 'data'
    # if "workers" in workers_data:
    #     print(f"Number of workers: {len(workers_data['workers'])}")
    #     print("First worker keys:", workers_data['workers'][0].keys())
    # elif "data" in workers_data:
    #     print(f"Number of items: {len(workers_data['data'])}")
    #     print("First item keys:", workers_data['data'][0].keys())
    # else:
    #     # Just preview part of it
    #     print("Preview JSON structure:")
    #     print(json.dumps(workers_data, indent=2)[:1000])  # limit output

def extract_org_unit(org_units, target_type):
    """
    Returns (code_value, short_name) for the given org unit type
    """
    if not org_units:
        return None, None

    for ou in org_units:
        type_name = get_field(ou, ["typeCode", "shortName"])
        if type_name == target_type:
            return (
                get_field(ou, ["nameCode", "codeValue"]),
                get_field(ou, ["nameCode", "shortName"]),
            )

    return None, None

def read_workers_json_file(region, date_time):
    logger.info(f"Starting function")
    
    # Load JSON file
    with open(
        f"{base_path}/files/{region}_workers_{date_time.strftime('%m%d%y')}.json",
        "r",
        encoding="utf-8",
    ) as f:
        workers_data = json.load(f)

    # Print top-level keys
    # print("Top-level keys:", workers_data.keys())
    # print("workers keys:", workers_data[0].keys())
    # print("workers keys:",
    #       workers_data[0]["workAssignments"][0].keys())


    workers = workers_data

    # Flatten into list of rows
    rows = []
    for w in workers:
        # Worker-level fields
        associateOID = w.get("associateOID")
        workerID = get_field(w, ["workerID", "idValue"])
        statusCode = get_field(w, ["workerStatus", "statusCode", "codeValue"])
        originalHireDate = get_field(w, ["workerDates", "originalHireDate"])
        terminationDate = get_field(w, ["workerDates", "terminationDate"])
        formattedName = get_field(w, ["person", "legalName", "formattedName"])
        familyName1 = get_field(w, ["person", "legalName", "familyName1"])
        middleName = get_field(w, ["person", "legalName", "middleName"])
        givenName = get_field(w, ["person", "legalName", "givenName"])

        # Work assignments (list → expand)
        assignments = w.get("workAssignments", [])
        if assignments:
            for wa in assignments:
                org_units = wa.get("homeOrganizationalUnits", [])
                bu_code, bu_name = extract_org_unit(org_units, "Business Unit")
                dept_code, dept_name = extract_org_unit(org_units, "Department")
                cost_code, cost_name = extract_org_unit(org_units, "Cost Number")
                row = {
                    "associateOID": associateOID,
                    "workerID": workerID,
                    "statusCode": statusCode,
                    "originalHireDate": originalHireDate,
                    "terminationDate": terminationDate,
                    "formattedName": formattedName,
                    "familyName": familyName1,
                    "middleName": middleName,
                    "givenName": givenName,
                    "assignmentStatus": get_field(
                        wa, ["assignmentStatus", "statusCode", "codeValue"]
                    ),
                    "assignmentStatusName": get_field(
                        wa, ["assignmentStatus", "statusCode", "longName"]
                    ),
                    "jobCode": get_field(wa, ["jobCode", "codeValue"]),
                    "jobTitle": wa.get("jobTitle"),
                    "positionID": wa.get("positionID"),
                    "supervisorAssociateOID": get_field(
                        wa,
                        ["workerTimeProfile", "timeServiceSupervisor", "associateOID"],
                    ),
                    "supervisorWorkerID": get_field(
                        wa,
                        [
                            "workerTimeProfile",
                            "timeServiceSupervisor",
                            "workerID",
                            "idValue",
                        ],
                    ),
                    "workerTypeCode": get_field(wa, ["workerTypeCode", "shortName"]),
                    "homeWorkLocation": get_field(
                        wa, ["homeWorkLocation", "nameCode", "codeValue"]
                    ),
                    "serviceSupervisorAssociateOID": get_field(
                        wa,
                        ["workerTimeProfile", "timeServiceSupervisor", "associateOID"],
                    ),
                    "workerTimeProfilePositionID": get_field(wa, ["positionID"]),
                    "payCycleCode": get_field(wa, ["payCycleCode", "shortName"]),
                    "payrollGroupCode": get_field(wa, ["payrollGroupCode"]),
                    "businessUnitCodeValue": bu_code,
                    "businessUnitShortName": bu_name,

                    "departmentCodeValue": dept_code,
                    "departmentShortName": dept_name,

                    "costNumberCodeValue": cost_code,
                    "costNumberShortName": cost_name,
                }
                rows.append(row)
        else:
            # Worker with no assignments → still include row
            rows.append(
                {
                    "associateOID": associateOID,
                    "workerID": workerID,
                    "statusCode": statusCode,
                    "originalHireDate": originalHireDate,
                    "terminationDate": terminationDate,
                    "assignmentStatus": None,
                    "assignmentStatusName": None,
                    "jobCode": None,
                    "jobTitle": None,
                    "positionID": None,
                    "supervisorAssociateOID": None,
                    "supervisorWorkerID": None,
                    "workerTypeCode": None,
                    "homeWorkLocation": None,
                    "serviceSupervisorAssociateOID": None,
                    "workerTimeProfilePositionID": None,
                    "payCycleCode": None,
                }
            )

    # Convert to DataFrame
    df = pd.DataFrame(rows)
    df = add_dw_columns(df, date_time, "workers", region, "ADP")
    print(df)
    df.to_excel(
        f"{base_path}/files/{region}_workers_{date_time.strftime('%m%d%y')}.xlsx", index=False
    )
    df.to_parquet(
        f"{base_path}/files/{region}_workers_{date_time.strftime('%m%d%y')}.parquet", index=False
    )


def parse_period_totals(period_totals):
    """Flatten periodTotals list into columns like REGULAR_timeDuration, OVERTIME_timeDuration."""
    flat = {}
    for pt in period_totals:
        code = get_field(pt, ["payCode", "codeValue"], "UNKNOWN")
        
        # duration
        duration = get_field(pt, ["timeDuration"])
        flat[f"{code}_periodTimeDuration"] = duration
        
        # rate fields
        base_multiplier = get_field(pt, ["rate", "baseMultiplierValue"])
        amount_value = get_field(pt, ["rate", "amountValue"])

        flat[f"{code}_periodRateBaseMultiplier"] = base_multiplier
        flat[f"{code}_periodRateAmount"] = amount_value
        
    return flat


def extract_time_cards_from_json_by_period(data):
    print(data.keys())
    team_time_cards = data["teamTimeCards"]

    print(len(team_time_cards))
    print(team_time_cards[0].keys())

    print(len(team_time_cards[0]["timeCards"]))
    print(team_time_cards[0]["timeCards"][0].keys())

    rows = []
    for w_time_cards in team_time_cards:
        # Worker-level fields
        associateOID = w_time_cards.get("associateOID")
        workerID = get_field(w_time_cards, ["workerID", "idValue"])
        formattedName = get_field(w_time_cards, ["personLegalName", "formattedName"])
        familyName1 = get_field(w_time_cards, ["personLegalName", "familyName1"])
        givenName = get_field(w_time_cards, ["personLegalName", "givenName"])
        # Work assignments (list → expand)
        time_cards = w_time_cards.get("timeCards", [])
        if time_cards:
            for tc in time_cards:
                row = {
                    "associateOID": associateOID,
                    "workerID": workerID,
                    "formattedName": formattedName,
                    "familyName": familyName1,
                    "givenName": givenName,
                    "processingStatusCode": get_field(
                        tc, ["processingStatusCode", "codeValue"]
                    ),
                    "periodCode": get_field(tc, ["periodCode", "codeValue"]),
                    "periodCodeShortName": get_field(tc, ["periodCode", "shortName"]),
                    "timePeriodStartDate": get_field(tc, ["timePeriod", "startDate"]),
                    "timePeriodEndDate": get_field(tc, ["timePeriod", "endDate"]),
                    "periodStatus": get_field(tc, ["timePeriod", "periodStatus"]),
                    # "periodTotals": get_field(pt, ["payCode", 'codeValue']),
                    # "timeDuration": get_field(pt, ["timeDuration"]),
                }
                # ✅ Add periodTotals info as extra columns in same row
                row.update(parse_period_totals(tc.get("periodTotals", [])))

                rows.append(row)
                print(row)


def parse_daily_totals(daily_totals):
    """
    Flatten dailyTotals list into a dict keyed by entryDate.
    Each row = one date; payCodes become columns (e.g. REGULAR_timeDuration).
    """
    daily_dict = {}

    for dt in daily_totals:
        entry_date = get_field(dt, ["entryDate"])
        code = get_field(dt, ["payCode", "codeValue"], "UNKNOWN")
        # duration
        duration = get_field(dt, ["timeDuration"])
        
        # rate fields
        base_multiplier = get_field(dt, ["rate", "baseMultiplierValue"])
        amount_value = get_field(dt, ["rate", "amountValue"])
        

        if entry_date not in daily_dict:
            daily_dict[entry_date] = {"entryDate": entry_date}

        # Example column: REGULAR_timeDuration
        daily_dict[entry_date][f"{code}_timeDuration"] = duration
        daily_dict[entry_date][f"{code}_rateBaseMultiplier"] = base_multiplier
        daily_dict[entry_date][f"{code}_rateAmount"] = amount_value

    # Return as list of dicts (so we can merge into main worker rows)
    return list(daily_dict.values())


def extract_time_cards_from_json_by_day(data):
    print(data.keys())
    team_time_cards = data["teamTimeCards"]

    print(len(team_time_cards))
    print(team_time_cards[0].keys())

    print(len(team_time_cards[0]["timeCards"]))
    print(team_time_cards[0]["timeCards"][0].keys())

    rows = []
    for w_time_cards in team_time_cards:
        # Worker-level fields
        associateOID = w_time_cards.get("associateOID")
        workerID = get_field(w_time_cards, ["workerID", "idValue"])
        formattedName = get_field(w_time_cards, ["personLegalName", "formattedName"])
        familyName1 = get_field(w_time_cards, ["personLegalName", "familyName1"])
        givenName = get_field(w_time_cards, ["personLegalName", "givenName"])

        # Each worker may have multiple timeCards
        time_cards = w_time_cards.get("timeCards", [])
        for tc in time_cards:
            # ✅ time-card level fields (repeat for every daily row)
            base_info = {
                "associateOID": associateOID,
                "workerID": workerID,
                "formattedName": formattedName,
                "familyName": familyName1,
                "givenName": givenName,
                "processingStatusCode": get_field(
                    tc, ["processingStatusCode", "codeValue"]
                ),
                "periodCode": get_field(tc, ["periodCode", "codeValue"]),
                "periodCodeShortName": get_field(tc, ["periodCode", "shortName"]),
                "timePeriodStartDate": get_field(tc, ["timePeriod", "startDate"]),
                "timePeriodEndDate": get_field(tc, ["timePeriod", "endDate"]),
                "periodStatus": get_field(tc, ["timePeriod", "periodStatus"]),
            }
            # ✅ Add periodTotals info as extra columns in same row
            base_info.update(parse_period_totals(tc.get("periodTotals", [])))

            # ✅ Expand dailyTotals into multiple rows
            daily_rows = parse_daily_totals(tc.get("dailyTotals", []))
            for dr in daily_rows:
                row = {**base_info, **dr}  # merge the two dicts
                rows.append(row)
    # Convert to DataFrame
    df = pd.DataFrame(rows)
    print(df)
    # df.to_excel('files/G3VV32149FAZE2C0_daily_time_cards.xlsx', index=False)
    return df


def extract_time_cards_from_json_by_day_from_file(data):
    print(data.keys())
    team_time_cards = data["teamTimeCards"]

    print(len(team_time_cards))
    print(team_time_cards[0].keys())

    print(len(team_time_cards[0]["timeCards"]))
    print(team_time_cards[0]["timeCards"][0].keys())

    rows = []
    for w_time_cards in team_time_cards:
        # Worker-level fields
        associateOID = w_time_cards.get("associateOID")
        workerID = get_field(w_time_cards, ["workerID", "idValue"])
        formattedName = get_field(w_time_cards, ["personLegalName", "formattedName"])
        familyName1 = get_field(w_time_cards, ["personLegalName", "familyName1"])
        givenName = get_field(w_time_cards, ["personLegalName", "givenName"])

        # Each worker may have multiple timeCards
        time_cards = w_time_cards.get("timeCards", [])
        for tc in time_cards:
            # ✅ time-card level fields (repeat for every daily row)
            base_info = {
                "associateOID": associateOID,
                "workerID": workerID,
                "formattedName": formattedName,
                "familyName": familyName1,
                "givenName": givenName,
                "processingStatusCode": get_field(
                    tc, ["processingStatusCode", "codeValue"]
                ),
                "periodCode": get_field(tc, ["periodCode", "codeValue"]),
                "periodCodeShortName": get_field(tc, ["periodCode", "shortName"]),
                "timePeriodStartDate": get_field(tc, ["timePeriod", "startDate"]),
                "timePeriodEndDate": get_field(tc, ["timePeriod", "endDate"]),
                "periodStatus": get_field(tc, ["timePeriod", "periodStatus"]),
            }
            # ✅ Add periodTotals info as extra columns in same row
            base_info.update(parse_period_totals(tc.get("periodTotals", [])))

            # ✅ Expand dailyTotals into multiple rows
            daily_rows = parse_daily_totals(tc.get("dailyTotals", []))
            for dr in daily_rows:
                row = {**base_info, **dr}  # merge the two dicts
                rows.append(row)
    # Convert to DataFrame
    df = pd.DataFrame(rows)
    print(df)
    # df.to_excel('files/G3VV32149FAZE2C0_daily_time_cards.xlsx', index=False)
    return df


def get_team_time_cards(
    region, date_time, aoid="G3VV32149FAZE2C0", start_date="2025-07-01"
):
    active_token = check_token_status(region.lower())
    CLIENT_CERT = config[f"{region.lower()}_adp_client_cert"]
    CLIENT_KEY = config[f"{region.lower()}_adp_client_key"]

    headers = {
        "Authorization": f"Bearer {active_token['access_token']}",
        "Accept": "application/json",
    }
    top = "10"
    top = "10"
    base_url = f"https://accounts.adp.com/time/v2/workers/{aoid}/team-time-cards?$expand=dayEntries&$filter=timeCards/timePeriod/startDate ge '{start_date}'"
    # base_url = f"https://accounts.adp.com/time/v2/workers/{aoid}/team-time-cards?$expand=dayEntries"
    # base_url = f"https://accounts.adp.com/time/v2/workers/{aoid}/team-time-cards?$expand=dayEntries&$top={top}&$skip={skip}"

    # base_url = f"https://accounts.adp.com/time/v2/workers/{aoid}/team-time-cards?$expand=timeEntries"
    # base_url = f"https://accounts.adp.com/time/v2/workers/{aoid}/team-time-cards"
    # base_url = f"https://accounts.adp.com/time/v2/workers/{aoid}/team-time-cards?$filter=timeCards/timePeriod/startDate ge '2025-07-01'"
    # base_url = f"https://accounts.adp.com/time/v2/workers/{aoid}/team-time-cards?$filter=teamTime Cards/timeCards/exceptionsIndicator"
    # base_url = f"https://accounts.adp.com/time/v2/workers/{aoid}/team-time-cards?$filter=timeCards/timePeriod/startDate ge '2025-07-01'"
    # base_url = f"https://accounts.adp.com/time/v2/workers/{aoid}/team-time-cards?$filter=timeCards/periodCode/codeValue eq 'current'"

    # "https://accounts.adp.com/time/v2/workers/G3JRZ3MWBDABF6FK/team-time-cards"
    response = requests.get(
        base_url,
        headers=headers,
        cert=(CLIENT_CERT, CLIENT_KEY),  # mTLS
        verify=True,  # or path to ADP CA if provided
    )
    try:
        # Raise exception if request failed
        response.raise_for_status()
        data = response.json()
        # Save JSON to file with timestamp
        filename = (
            f"{base_path}/files/{region}_{aoid}_time_cards_{date_time.strftime('%m%d%y')}.json"
        )

        with open(filename, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)

        print(f"📁 Time Cards data exported to {filename}")
        return data

    except requests.exceptions.HTTPError as e:
        print("Status code:", response.status_code)
        print("Response body:", response.text)  # API error details
        return []


def get_worker_payment_list(region, date_time, aoid="G3Q0HZMV4ZYJYRN1"):
    active_token = check_token_status(region.lower())
    CLIENT_CERT = config[f"{region.lower()}_adp_client_cert"]
    CLIENT_KEY = config[f"{region.lower()}_adp_client_key"]

    headers = {
        "Authorization": f"Bearer {active_token['access_token']}",
        "Accept": "application/json",
    }

    # base_url = f"https://accounts.adp.com/time/v2/workers/{aoid}/team-time-cards?$expand=dayEntries&$filter=timeCards/timePeriod/startDate ge '{start_date}'"
    # base_url = f"https://accounts.adp.com/time/v2/workers/{aoid}/team-time-cards?$expand=dayEntries"
    # base_url = f"https://accounts.adp.com/time/v2/workers/{aoid}/team-time-cards?$expand=timeEntries"
    # base_url = f"https://accounts.adp.com/time/v2/workers/{aoid}/team-time-cards"
    # base_url = f"https://accounts.adp.com/time/v2/workers/{aoid}/team-time-cards?$filter=timeCards/timePeriod/startDate ge '2025-07-01'"
    # base_url = f"https://accounts.adp.com/time/v2/workers/{aoid}/team-time-cards?$filter=teamTime Cards/timeCards/exceptionsIndicator"
    # base_url = f"https://accounts.adp.com/time/v2/workers/{aoid}/team-time-cards?$filter=timeCards/timePeriod/startDate ge '2025-07-01'"
    # base_url = f"https://accounts.adp.com/time/v2/workers/{aoid}/team-time-cards?$filter=timeCards/periodCode/codeValue eq 'current'"
    base_url = f"https://accounts.adp.com/payroll/v1/workers/{aoid}/organizational-pay-statements"
    # base_url = f"https://accounts.adp.com/payroll/v1/workers/{aoid}/organizational-pay-statements/0304809525338201005308001484099"
    # base_url = f"https://accounts.adp.com/payroll/v1/workers/{aoid}/pay-statements"

    # base_url = f"https://accounts.adp.com/payroll/v1/workers/{aoid}/organizational-pay-statements?$filter=payStatements/payDate ge 2025-09-01"
    # base_url = f"https://accounts.adp.com/payroll/v1/workers/{aoid}/organizational-pay-statements"

    # "https://accounts.adp.com/time/v2/workers/G3JRZ3MWBDABF6FK/team-time-cards"

    try:
        response = requests.get(
            base_url,
            headers=headers,
            cert=(CLIENT_CERT, CLIENT_KEY),  # mTLS
            verify=True,  # or path to ADP CA if provided
        )
        filename = f"{base_path}/files/{region}_{aoid}_worker_payment_list_{date_time.strftime('%m%d%y')}.json"

        if response.status_code == 204:
            print(
                f"ℹ️ 204 No Content for {aoid} ({region}). Creating empty JSON file..."
            )
            with open(filename, "w", encoding="utf-8") as f:
                json.dump({}, f, indent=4)
            return None

        response.raise_for_status()

        data = response.json()

        # Save JSON to file with timestamp
        # timestamp = datetime.now().strftime("%Y%m%d")

        with open(filename, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)

        print(f"📁 Payroll data exported to {filename}")
        return data

    except requests.exceptions.HTTPError as e:
        print(f"❌ HTTPError for {aoid}: {e}")
        print("Status code:", response.status_code)
        print("Response body:", response.text)
        return None

    except Exception as e:
        print(f"⚠️ Unexpected error for {aoid}: {e}")
        return None


def read_worker_payment_list_json_file(region, date_time, aoid):
    # Load JSON file
    filename = (
        f"{base_path}/files/{region}_{aoid}_worker_payment_list_{date_time.strftime('%m%d%y')}.json"
    )

    # Handle missing file
    if not os.path.exists(filename):
        print(f"⚠️ File not found for {aoid} ({region}) — skipping.")
        return pd.DataFrame()  # empty df for concatenation safety

    # Load JSON file
    with open(filename, "r", encoding="utf-8") as f:
        payment_list_data = json.load(f)

    # Handle empty JSON (from 204 response)
    if not payment_list_data or "payStatements" not in payment_list_data:
        print(
            f"ℹ️ Empty or invalid JSON for {aoid} ({region}) — returning empty DataFrame."
        )
        return pd.DataFrame()

    payments = payment_list_data["payStatements"]
    if not payments:
        print(
            f"ℹ️ No payStatements found for {aoid} ({region}) — returning empty DataFrame."
        )
        return pd.DataFrame()

    # # Print top-level keys
    # print("Top-level keys:", payment_list_data.keys())
    # print("count of payStatements:", len(payment_list_data["payStatements"]))
    # # print("workers keys:", payment_list_data[0].keys())
    # print("payStatements keys:",
    #       payment_list_data["payStatements"][0].keys())

    # Flatten into list of rows
    rows = []
    for p in payments:
        # Worker-level fields
        payDate = p.get("payDate")
        netPayAmount = get_field(p, ["netPayAmount", "amountValue"])
        grossPayAmount = get_field(p, ["grossPayAmount", "amountValue"])
        totalHours = p.get("totalHours")
        payDetailUri = get_field(p, ["payDetailUri", "href"])
        statementImageUri = get_field(p, ["statementImageUri", "href"])

        row = {
            "associateOID": aoid,
            "region": region,
            "payDate": payDate,
            "netPayAmount": netPayAmount,
            "grossPayAmount": grossPayAmount,
            "totalHours": totalHours,
            "payDetailUri": payDetailUri,
            "payStatementId": payDetailUri.split("/")[-1],
            "statementImageUri": statementImageUri,
            # "periodTotals": get_field(pt, ["payCode", 'codeValue']),
            # "timeDuration": get_field(pt, ["timeDuration"]),
        }
        rows.append(row)

    # Convert to DataFrame
    df = pd.DataFrame(rows)
    print(df)
    return df
    # df.to_excel(f'files/{region}_workers.xlsx', index=False)
    # df.to_parquet(
    #     f'files/{region}_workers_{date_time.strftime("%m%d%y")}.parquet', index=False)


def get_team_time_cards_top_skip(
    aoid="G3FGQ8G17K3Q62EQ", cert=None, key=None, top=100, pause=0.1, max_pages=10000
):
    active_token = check_token_status()
    CLIENT_CERT = config["adp_client_cert"]
    CLIENT_KEY = config["adp_client_key"]

    headers = {
        "Authorization": f"Bearer {active_token['access_token']}",
        "Accept": "application/json",
    }

    base_url = f"https://accounts.adp.com/time/v2/workers/{aoid}/team-time-cards?$expand=dayEntries"
    # "https://accounts.adp.com/time/v2/workers/G3JRZ3MWBDABF6FK/team-time-cards"

    all_workers = []
    skip = 0
    page = 0

    while True:
        url = f"{base_url}&$top={top}&$skip={skip}"
        print(f"➡️ Fetching: {url}")

        resp = requests.get(
            url, headers=headers, cert=(CLIENT_CERT, CLIENT_KEY), verify=True
        )

        if resp.status_code == 200:
            data = resp.json()
            batch = data.get("teamTimeCards") or []
            print(batch)
            if not batch:
                print("⚠️ Empty workers array, stopping.")
                break

            all_workers.extend(batch)

        elif resp.status_code == 204:
            print("✅ No content (204) – reached the end of records.")
            break

        else:
            print(f"❌ Unexpected status {resp.status_code}: {resp.text}")
            break  # stop loop on error

        page += 1
        skip += top

        if page >= max_pages:
            raise RuntimeError(
                f"Reached max_pages ({max_pages}); stopping to avoid infinite loop."
            )

        time.sleep(pause)

    # Save JSON to file with timestamp
    timestamp = datetime.now().strftime("%Y%m%d")
    filename = f"{base_path}/files/{aoid}_teamTimeCards_{timestamp}.json"

    with open(filename, "w", encoding="utf-8") as f:
        json.dump(all_workers, f, indent=4)

    print(f"📁 teamTimeCards data exported to {filename}")

    return all_workers


def select_all_period_times(region, date_time, start_date="2025-08-15"):
    logger.info(f"Starting function")
    df_all_workers = pd.read_parquet(
        f"{base_path}/files/{region}_workers_{date_time.strftime('%m%d%y')}.parquet"
    )
    print(df_all_workers)
    all_team_time_cards_dfs = []
    for supervisorAssociateOID in df_all_workers["supervisorAssociateOID"].unique():
        # for supervisorAssociateOID in ["G3CK8PRN7AMFCPDN"]:
        if supervisorAssociateOID != None:
            print(supervisorAssociateOID)
            json_team_time_cards = get_team_time_cards(
                region, date_time, supervisorAssociateOID, start_date
            )
            if json_team_time_cards != []:
                if len(json_team_time_cards["teamTimeCards"]) > 0:
                    df_team_time_cards = extract_time_cards_from_json_by_day_from_file(
                        json_team_time_cards
                    )
                    all_team_time_cards_dfs.append(df_team_time_cards)

    print(len(all_team_time_cards_dfs))
    final_df = pd.concat(all_team_time_cards_dfs, ignore_index=True)
    final_df = add_dw_columns(final_df, date_time, "team_time_cards", region, "ADP")
    final_df.to_excel(
        f"{base_path}/files/{region}_team_time_cards_{date_time.strftime('%m%d%y')}.xlsx",
        index=False,
    )
    final_df.to_parquet(
        f"{base_path}/files/{region}_team_time_cards_{date_time.strftime('%m%d%y')}.parquet",
        index=False,
    )


def get_all_workers_payments_details(region, date_time):
    active_token = check_token_status(region.lower())
    CLIENT_CERT = config[f"{region.lower()}_adp_client_cert"]
    CLIENT_KEY = config[f"{region.lower()}_adp_client_key"]

    headers = {
        "Authorization": f"Bearer {active_token['access_token']}",
        "Accept": "application/json",
    }

    df_all_workers_payments = pd.read_parquet(
        f"{base_path}/files/{region}_pay_statements_{date_time.strftime('%m%d%y')}.parquet"
    )
    print(df_all_workers_payments)
    print(df_all_workers_payments.columns)

    all_payment_details = []

    for _, row in df_all_workers_payments.iterrows():
        aoid = row["associateOID"]
        region = row["region"]
        pay_detail_uri = row["payDetailUri"]
        pay_statement_id = row["payStatementId"]

        print(f"Fetching payment detail for {aoid} - {pay_statement_id}")
        adp_url = f"https://accounts.adp.com"
        base_url = f"{adp_url}{pay_detail_uri}"
        print(base_url)
        

        response = requests.get(
            base_url,
            headers=headers,
            cert=(CLIENT_CERT, CLIENT_KEY),  # mTLS
            verify=True,  # or path to ADP CA if provided
        )

        if response.status_code == 200:
            data = response.json()
            data["associateOID"] = aoid
            data["region"] = region
            data["payStatementId"] = pay_statement_id
            data["payDetailUri"] = pay_detail_uri
            all_payment_details.append(data)

        elif response.status_code == 204:
            # Optional: Track missing data
            print(f"No data for {aoid} - {pay_statement_id} (204)")
            all_payment_details.append(
                {
                    "associateOID": aoid,
                    "region": region,
                    "payStatementId": pay_statement_id,
                    "payDetailUri": pay_detail_uri,
                    "status": 204,
                    "data": None,
                }
            )

        else:
            print(f"Error {response.status_code} for {pay_detail_uri}")

    # ✅ Save all results into ONE JSON file
    output_path = (
        f"{base_path}/files/{region}_all_worker_payment_details_{date_time.strftime('%m%d%y')}.json"
    )
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(all_payment_details, f, ensure_ascii=False, indent=4)

    print(f"Saved all payment details → {output_path}")
    return output_path


def normalize_earn_code(code: str) -> str:
    """Clean up an earning code name for use as a safe column name."""
    if code is None:
        return "UNKNOWN"
    s = str(code).strip()
    # Replace spaces with underscores
    s = re.sub(r"\s+", "_", s)
    # Replace non-alphanumeric characters (except underscore) with underscore
    s = re.sub(r"[^0-9a-zA-Z_]", "_", s)
    return s


def parse_earnings(earnings):
    """
    Flatten earnings list into columns:
    e.g. REGULAR_amount, REGULAR_hours, OVERTIME_amount, etc.
    """
    flat = {}
    for e in earnings:
        # code = get_field(e, ["earningCode", "codeValue"], "UNKNOWN")
        code_raw = e.get("earningCodeName") or e.get("earningCode") or "UNKNOWN"
        code = normalize_earn_code(code_raw)
        amt = get_field(e, ["earningAmount", "amountValue"])
        ytd_amt = get_field(e, ["ytdEarningAmount", "amountValue"])
        hours = get_field(e, ["payPeriodHours"])
        pay_rate = get_field(e, ["payRate", "rateValue"])
        pre_tax = get_field(e, ["preTaxIndicator"])

        flat[f"{code}_amount"] = amt
        flat[f"{code}_ytdAmount"] = ytd_amt
        flat[f"{code}_hours"] = hours
        flat[f"{code}_payRate"] = pay_rate
        flat[f"{code}_preTaxIndicator"] = pre_tax

    return flat


def read_all_workers_payments_details_json_file(region, date_time):
    filename = (
        f"{base_path}/files/{region}_all_worker_payment_details_{date_time.strftime('%m%d%y')}.json"
    )
    # Load JSON file
    with open(filename, "r", encoding="utf-8") as f:
        payment_details_data = json.load(f)
    # Print top-level keys
    print("Top-level keys:", payment_details_data[0].keys())
    print("Top-level keys:", payment_details_data[0]["payStatement"].keys())
    # print("workers keys:", workers_data[0].keys())
    # print("workers keys:",
    #       workers_data[0]["workAssignments"][0].keys())
    # Flatten into list of rows
    rows = []
    for p in payment_details_data:
        # Worker-level fields
        ps = p.get("payStatement")
        associateOID = p.get("associateOID")
        region = p.get("region")
        payStatementId = p.get("payStatementId")
        payDetailUri = p.get("payDetailUri")

        payDate = get_field(ps, ["payDate"])
        payPeriodStartDate = get_field(ps, ["payPeriod", "startDate"])
        payPeriodEndDate = get_field(ps, ["payPeriod", "endDate"])
        netPayAmount = get_field(ps, ["netPayAmount", "amountValue"])
        grossPayAmount = get_field(ps, ["grossPayAmount", "amountValue"])
        grossPayYTDAmount = get_field(ps, ["grossPayYTDAmount", "amountValue"])
        totalHours = get_field(ps, ["totalHours"])

        base_info = {
            "associateOID": associateOID,
            "region": region,
            "payStatementId": payStatementId,
            "payDetailUri": payDetailUri,
            "payDate": payDate,
            "payPeriodStartDate": payPeriodStartDate,
            "payPeriodEndDate": payPeriodEndDate,
            "netPayAmount": netPayAmount,
            "grossPayAmount": grossPayAmount,
            "grossPayYTDAmount": grossPayYTDAmount,
            "totalHours": totalHours,
        }

        # --- Flatten earnings section into columns ---
        earnings = ps.get("earnings", [])
        earnings_flat = parse_earnings(earnings)
        row = {**base_info, **earnings_flat}

        rows.append(row)

    # Convert to DataFrame
    df = pd.DataFrame(rows)
    print(df)
    print(df.columns)
    df = add_dw_columns(df, date_time, "pay_statement_details", region, "ADP")

    df.to_parquet(
        f"{base_path}/files/{region}_pay_statement_details_{date_time.strftime('%m%d%y')}.parquet",
        index=False,
    )
    df.to_excel(
        f"{base_path}/files/{region}_pay_statement_details_{date_time.strftime('%m%d%y')}.xlsx",
        index=False,
    )
    return df


def select_all_workers(region, date_time):
    fetch_all_workers(region, date_time)
    read_workers_json_file(region, date_time)


def select_all_workers_payments_list(region, date_time):
    # df_workers_time_cards = pd.read_parquet(
    #     f"{base_path}/files/{region}_team_time_cards_{date_time.strftime('%m%d%y')}.parquet"
    # )
    # workers_associate_oid = df_workers_time_cards["associateOID"].unique()
    
    df_all_workers = pd.read_parquet(
        f"{base_path}/files/{region}_workers_{date_time.strftime('%m%d%y')}.parquet"
    )
    workers_associate_oid = df_all_workers["associateOID"].unique()
    
    
    # workers_associate_oid = ['G33DNYRPPMZ5BAE0']
    all_dfs_workers_payments_list = []
    for aoid in workers_associate_oid:
        print(aoid)
        get_worker_payment_list(region, date_time, aoid)
        df = read_worker_payment_list_json_file(region, date_time, aoid)
        # Append only if the dataframe is not empty
        if df is not None and not df.empty:
            all_dfs_workers_payments_list.append(df)

    # Concatenate all into one final dataframe
    df_all_workers_payments = pd.concat(
        all_dfs_workers_payments_list, ignore_index=True
    )
    print(df_all_workers_payments)
    df_all_workers_payments = add_dw_columns(
        df_all_workers_payments, date_time, "pay_statements", region, "ADP"
    )
    df_all_workers_payments.to_parquet(
        f"{base_path}/files/{region}_pay_statements_{date_time.strftime('%m%d%y')}.parquet",
        index=False,
    )
    df_all_workers_payments.to_excel(
        f"{base_path}/files/{region}_pay_statements_{date_time.strftime('%m%d%y')}.xlsx",
        index=False,
    )


def select_all_workers_payments_detail(region, date_time):
    get_all_workers_payments_details(region, date_time)
    read_all_workers_payments_details_json_file(region, date_time)


regions_list = {
    "Southeast": 1,
    "Central":7
}




def main():
    date_time = datetime.now()
    # date_time = datetime.now() - timedelta(days=2)
    
    if len(sys.argv) == 2:
        region_name = sys.argv[1]
        print(sys.argv)
    
        logger = setup_logging(f"{log_path}{region_name}_{script_name}.log")
        logger.info(f"-------- Executing {script_name} ---------")
        logger.info(f"Datetime = {date_time.strftime('%m-%d-%y %H:%M:%S')}")
    
    # for region in regions_list:
        print(region_name)
        region_id = regions_list[region_name]
        print(region_id)
        # Step 1 Select all Workers
        select_all_workers(region_name, date_time)
        
        # Step 2 Select Period times
        # two_weeks_before = "2025-08-15"
        start_date = get_team_time_cards_max_start_date(region_id)
        two_weeks_before = start_date - timedelta(days=14)
        select_all_period_times(region_name, date_time, two_weeks_before)
        
        # aoid = 'G3DQE7YYDMVA0VTW'
        # filename = (
        #     f"{base_path}/files/{region_name}_{aoid}_time_cards_{date_time.strftime('%m%d%y')}.json"
        # )
        
        #     # Load JSON file
        # with open(
        #     filename,
        #     "r",
        #     encoding="utf-8",
        # ) as f:
        #     json_team_time_cards = json.load(f)

        # df_team_time_cards = extract_time_cards_from_json_by_day_from_file(
        #                 json_team_time_cards
        #             )
        
        # print(df_team_time_cards)
        # print(df_team_time_cards.columns)
        # df_team_time_cards.to_excel("files/test/df_team_time_cards.xlsx", index=False)
        
        # # Step 3 Select Payments (5 last Payments)
        # select_all_workers_payments_list(region_name, date_time)
        # select_all_workers_payments_detail(region_name, date_time)


if __name__ == "__main__":
    start = timeit.default_timer()
    main()
    end = timeit.default_timer()
    logger.info(f"Duration: {end - start} secs")
    logger.info(f"Duration: {(end - start) / 60} mins")
