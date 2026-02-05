import pandas as pd
import timeit
from datetime import datetime
from dotenv import dotenv_values
import pyodbc
import timeit
from datetime import datetime, timedelta
import logging
import os
from modules.utilities.export_to_files import export_to_files
from modules.columns_mapping_adp_dw import columns_mapping_dict
import isodate
import sys
import numpy as np


script_name = os.path.splitext(os.path.basename(__file__))[0]

# Get the absolute path of the current script
script_path = os.path.abspath(__file__)
# Get the directory containing the current script
base_path = os.path.dirname(script_path)

# print(f"{base_path}/.env")

config = dotenv_values(f"{base_path}/.env")

output_folder = "prod"
log_path = f"{base_path}/logs/"

output_path = f"{base_path}/files/"

output_path = (
    f"E:/Datawarehouse/python_scripts_output/DataLake/{output_folder}/from_salesforce"
)
from_datalake_path = (
    f"E:/Datawarehouse/python_scripts_output/DataLake/{output_folder}/from_datalake"
)

# output_path = (
#     f"E:/Datawarehouse/python_scripts_output/DataLake/{output_folder}/from_salesforce"
# )
# from_datalake_path = (
#     f"E:/Datawarehouse/python_scripts_output/DataLake/{output_folder}/from_datalake"
# )


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

    return logger

def duration_to_minutes(x):
    if pd.isna(x) or x in ["None", None]:
        return np.nan
    try:
        return isodate.parse_duration(x).total_seconds() / 60
    except:
        return np.nan

def transform_team_time_cards(df):
    # 1) Select all duration columns
    duration_cols = [col for col in df.columns if col.endswith('_duration')]
    
    
    # 2) Function to convert ISO-8601 duration -> minutes
    for col in duration_cols:
        df[col + '_minutes'] = df[col].apply(duration_to_minutes)
        

    return(df)

def transform_and_schema_assign(region, endpoint_name, df, date_time):
    columns = columns_mapping_dict[endpoint_name]["columns_list"]
    if ((endpoint_name == 'pay_statement_details') | (endpoint_name == 'team_time_cards')):
        columns = columns[region]
        
        
    key_columns = columns_mapping_dict[endpoint_name]["key_columns"]

    key_columns.append("region")
    df["id"] = df[key_columns].apply(lambda x: "_".join(x.astype(str)), axis=1)

    rename_dict = {col["name"]: col["alias"] for col in columns}
    type_dict = {col["alias"]: col["type"] for col in columns}

    # Extract only the source column names
    source_columns = [col["name"] for col in columns]
    
    # --- Ensure all expected columns exist ---
    missing_columns = [c for c in source_columns if c not in df.columns]
    if missing_columns:
        print("⚠️ Missing columns detected:", missing_columns)
        logger.warning(
            f"Missing columns detected: {', '.join(missing_columns)}"
        )
        
        
        for col in missing_columns:
            df[col] = None  # Create column with empty values

    print("Step 0: Filtering columns from source DataFrame")
    logger.debug("Step 0: Filtering columns from source DataFrame")
    
    
    
    df = df[source_columns]  # Keep only the relevant columns

    print("Step 1: Renaming Dataframe using mapping")
    logger.debug("Step 1: Renaming Dataframe using mapping")
    # Step 1: Rename columns
    df = df.rename(columns=rename_dict)

    print("Step 2: Removing duplicate rows")
    logger.debug("Step 2: Removing duplicate rows")

    # Step 2: Remove duplicates
    print("Before removing duplicates:", len(df))
    logger.debug(f"Before removing duplicates: {len(df)}")
    len_df_before = len(df)
    # df = df.drop_duplicates()
    df = df.drop_duplicates(subset=["id"])

    len_df_after = len(df)

    print("After removing duplicates:", len(df))
    logger.debug(f"After removing duplicates: {len(df)}")
    removed = len_df_before - len_df_after
    print("Duplicates removed:", removed)
    logger.debug(f"Duplicates removed: {removed}")
    

    if endpoint_name == 'team_time_cards':
        df = transform_team_time_cards(df)
        df = df[df["entry_date"].notna()]
    
    # df = df[df["time_period_start_date"] != '2025-10-11']

    logger.debug(f"Exporting df result to: {region}_ADP_DataLake_{endpoint_name}_{date_time.strftime('%m%d%y')}")

    export_to_files(
        df,
        f"{region}_ADP_DataLake_{endpoint_name}_{date_time.strftime('%m%d%y')}",
        from_datalake_path,
        logger,
        [False, True, True],
    )
    return(df)


regions_list = {
    "Southeast": 1,
    "Central":7
}

endpoints = [
    "workers",
    "team_time_cards",
    # "pay_statements",
    # "pay_statement_details"
]
    

def main():
    date_time = datetime.now()
    # date_time = datetime.now() - timedelta(days=1)
    
    if len(sys.argv) == 2:
        region_name = sys.argv[1]
        print(sys.argv)
    
        logger = setup_logging(f"{log_path}{region_name}_{script_name}.log")
        logger.info(f"-------- Executing {script_name} ---------")
        logger.info(f"Datetime = {date_time.strftime('%m-%d-%y %H:%M:%S')}")

    # for region in regions_list:
        logger.info(F"Starting for region {region_name}")
        for endpoint in endpoints:
            logger.info(F"Starting for endpoint {endpoint}")
            df = pd.read_parquet(
                f"{base_path}/files/{region_name}_{endpoint}_{date_time.strftime('%m%d%y')}.parquet",
            )
            df_output = transform_and_schema_assign(region_name, endpoint, df, date_time)
            if endpoint == 'team_time_cards':
                logger.debug(f'min_start_date: {df_output["time_period_start_date"].min()}')
                logger.debug(f'max_start_date: {df_output["time_period_start_date"].max()}')
                logger.debug(f'max_start_date: {df_output["time_period_start_date"].unique()}')
                print(f'min_start_date: {df_output["time_period_start_date"].min()}')
                print(f'max_start_date: {df_output["time_period_start_date"].max()}')
                print(f'max_start_date: {df_output["time_period_start_date"].unique()}')
            elif endpoint == 'pay_statements':
                logger.debug(f'min_pay_date: {df_output["pay_date"].min()}')
                logger.debug(f'min_pay_date: {df_output["pay_date"].max()}')
                logger.debug(f'unique_pay_date: {df_output["pay_date"].unique()}')
                print(f'min_pay_date: {df_output["pay_date"].min()}')
                print(f'min_pay_date: {df_output["pay_date"].max()}')
                print(f'unique_pay_date: {df_output["pay_date"].unique()}')



if __name__ == "__main__":
    start = timeit.default_timer()
    main()
    end = timeit.default_timer()
    print(f"Duration: {end - start} secs")
    print(f"Duration: {(end - start) / 60} mins")
    logger.info(f"Duration: {end - start} secs")
    logger.info(f"Duration: {(end - start) / 60} mins")


