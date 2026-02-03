import pandas as pd
import timeit
from datetime import datetime
from dotenv import dotenv_values
import pyodbc
import timeit
from datetime import datetime, timedelta
import logging
import os
from collections import namedtuple
from tqdm import tqdm
from modules.columns_mapping_adp_dw import columns_mapping_dict
from modules.stg_endpoints_list import stg_endpoints_list
from collections import Counter
import sys



script_name = os.path.splitext(os.path.basename(__file__))[0]

# Get the absolute path of the current script
script_path = os.path.abspath(__file__)
# Get the directory containing the current script
base_path = os.path.dirname(script_path)

# print(f"{base_path}/.env")

config = dotenv_values(f"{base_path}/.env")

log_path = f"{base_path}/logs/"

output_folder = "prod"

output_path = (
    f"E:/Datawarehouse/python_scripts_output/DataLake/{output_folder}/from_salesforce"
)
from_datalake_path = (
    f"E:/Datawarehouse/python_scripts_output/DataLake/{output_folder}/from_datalake"
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

    return logger


def read_sf_parquet_data_from_datalake(region, endpoint_name, date_time):
    print("Executing read_sf_parquet_data_from_datalake")
    logger.debug("Starting function")
    file_name = f"{region}_ADP_DataLake_{endpoint_name}_{date_time.strftime('%m%d%y')}"
    file_path = f"{from_datalake_path}/parquet/{file_name}.parquet"

    if not os.path.exists(file_path):
        print(f"File does not exist: {file_path}")
        logger.error(f"File does not exist: {file_path}")
        return None

    df = pd.read_parquet(f"{file_path}")

    if df.empty:
        print(f"Dataframe is empty for file: {file_path}")
        logger.error(f"Dataframe is empty for file: {file_path}")
        return None

    print(df)
    return df


def sql_insert_process(conn, df, table_name):
    process_result = False
    try:
        logger.debug("Inserting data to SQL Server")
        print("Inserting data to SQL Server")
        cursor = conn.cursor()
        columns_list = df.columns.tolist()
        DataTupple = namedtuple("DataTupple", columns_list)

        for index, row in tqdm(df.iterrows(), total=df.shape[0]):
            # Create a named tuple with the row values
            row_tuple = DataTupple(*row)
            insert_string = (
                "INSERT INTO "
                + table_name
                + " ({}) VALUES ({})".format(
                    ",".join(columns_list), ",".join(["?" for _ in columns_list])
                )
            )
            cursor.execute(insert_string, row_tuple)
            # print(insert_string)
            # print(row_tuple)

        process_result = True
    except Exception as e:
        logger.error("Error: %s", str(e))
        print("Error: %s", str(e))
        print(insert_string)
        print(row_tuple)
        print(row)

        for i, (col_name, val) in enumerate(row_tuple.items()):
            print(
                f"Param {i + 1}: Column = {col_name}, Value = {val}, Type = {type(val)}"
            )

        process_result = False
        # send_email(f"Error 04 Script BC {company_short} {table_name}", str(e))
    finally:
        # Code that is always executed, regardless of whether an exception was raised or not
        logger.debug("Commiting and Closing SQL Server connection (Insert)")
        if process_result:
            conn.commit()
            cursor.close()
        else:
            print("else insert")
            cursor.close()
        return process_result
    
    
def insert_process_v3(conn, df, table_name):
    try:
        print(f"Inserting {len(df):,} rows into {table_name}")
        logger.debug(f"Inserting {len(df):,} rows into {table_name}")

        cursor = conn.cursor()
        cursor.fast_executemany = True

        columns = df.columns.tolist()
        col_list = ", ".join(columns)
        placeholders = ", ".join(["?"] * len(columns))

        insert_sql = f"""
            INSERT INTO {table_name} ({col_list})
            VALUES ({placeholders})
        """

        # Force NVARCHAR(MAX) for all object columns
        sizes = []
        for col in df.columns:
            if df[col].dtype == object:
                sizes.append((pyodbc.SQL_WVARCHAR, 0, 0))
            else:
                sizes.append(None)

        cursor.setinputsizes(sizes)

        data = list(df.itertuples(index=False, name=None))

        cursor.executemany(insert_sql, data)
        conn.commit()
        cursor.close()

        print(f"Inserted {len(df):,} rows into {table_name}")
        logger.debug(f"Inserted {len(df):,} rows into {table_name}")
        return True

    except Exception as e:
        conn.rollback()
        print("Insert failed:", e)
        logger.error("Insert failed:", e)
        # send_email(f"Error Insert {company_short} {table_name}", str(e))
        raise

def create_sql_connection():
    server = config["sql_server"]
    database = config["sql_database"]
    uid = config["sql_uid"]
    pwd = config["sql_pwd"]

    conn = pyodbc.connect(
        "Driver={ODBC Driver 18 for SQL Server};"
        "Server=tcp:" + server + ";"
        "Database=" + database + ";"
        "Uid={" + uid + "};"
        "Pwd={" + pwd + "};"
        "Encrypt=yes;"
        "TrustServerCertificate=no;"
    )
    return(conn)

def delete_records(table_name, region_id):
    print(
        f"Deleting records WHERE (region = {region_id})"
    )
    logger.debug(
       f"Deleting records WHERE (region = {region_id})"
    )
    
    conn = create_sql_connection()
    
    cursor = conn.cursor()

    cursor.execute(f"""
                    DELETE FROM {table_name}
                    WHERE region_id = {region_id};
                """)

    conn.commit()
    conn.close()

def insert_to_sql_dw(df, table_name, action):
    conn = create_sql_connection()

    if action == "insert":
        logger.debug(f"Inserting data process for {table_name}")
        # result = sql_insert_process(conn, df, table_name)
        result = insert_process_v3(conn, df, table_name)
        
def insert_to_sql_row_by_row(df, table_name):
    conn = create_sql_connection()
    sql_insert_process(conn, df, table_name)
        
        
def sql_procedure_truncate(table_name):
    print(
        f"Truncate stage table {table_name}"
    )
    logger.debug(
        f"Truncate stage table {table_name}"
    )
    conn = create_sql_connection()

    cursor = conn.cursor()

    cursor.execute(f"""
                    TRUNCATE TABLE {table_name};
                """)

    conn.commit()
    conn.close()

def sql_procedure_insert(
    df, table_name, company_short=""
):
    conn = create_sql_connection()

    result = insert_process_v3(conn, df, table_name)

    logger.debug(f"Inserting data process COMPLETED for {table_name}")
    conn.close()
    
def get_table_columns(conn, table_name):
    sql = """
    SELECT c.name
    FROM sys.columns c
    JOIN sys.tables t ON c.object_id = t.object_id
    JOIN sys.schemas s ON t.schema_id = s.schema_id
    WHERE s.name = 'dbo'
      AND t.name = ?
    """
    cur = conn.cursor()
    cur.execute(sql, table_name)
    return {row[0] for row in cur.fetchall()}    

def sql_merge_staging_into_silver_auto(
    silver_table,
    staging_table,
    join_keys
):
    logger.debug(F"Starting merge stating to silver")
    
    conn = create_sql_connection()

    silver_cols = get_table_columns(conn, silver_table)
    staging_cols = get_table_columns(conn, staging_table)

    # Only columns that exist in BOTH tables
    common_cols = silver_cols & staging_cols

    # Never update join keys
    update_cols = common_cols - set(join_keys)

    if not update_cols:
        print("No updatable columns found!")
        logger.debug("No updatable columns found!")
        raise Exception("No updatable columns found!")

    on_clause = " AND ".join(
        [f"t.{k} = s.{k}" for k in join_keys]
    )

    update_clause = ",\n".join(
        [f"t.{c} = s.{c}" for c in update_cols]
    )

    insert_cols = ", ".join(common_cols)
    insert_vals = ", ".join([f"s.{c}" for c in common_cols])

    sql = f"""
    MERGE dbo.{silver_table} AS t
    USING dbo.{staging_table} AS s
        ON {on_clause}
    WHEN MATCHED THEN
        UPDATE SET
            {update_clause}
    WHEN NOT MATCHED THEN
        INSERT ({insert_cols})
        VALUES ({insert_vals})
        OUTPUT $action;
    """
    
    print("---- GENERATED MERGE SQL ----")
    print(sql)
    print("-----------------------------")
    logger.debug("---- GENERATED MERGE SQL ----")
    logger.debug(sql)
    logger.debug("-----------------------------")

    cur = conn.cursor()
    cur.execute(sql)
    actions = cur.fetchall()
    conn.commit()
    conn.close()
    
        # Count results
    stats = Counter(row[0] for row in actions)

    print("MERGE results:")
    print(f"  INSERTED: {stats.get('INSERT', 0)}")
    print(f"  UPDATED : {stats.get('UPDATE', 0)}")
    logger.debug("MERGE results:")
    logger.debug(f"  INSERTED: {stats.get('INSERT', 0)}")
    logger.debug(f"  UPDATED : {stats.get('UPDATE', 0)}")
    print(stats)

    return stats


def prepare_df_from_parquet(df, endpoint_name, region):
    logger.info(F"Starting function")
    schema = columns_mapping_dict[endpoint_name]
    columns_list = schema["columns_list"]
    additional_columns_list = schema["additional_column_list"]
    if ((endpoint_name == 'pay_statement_details') | (endpoint_name == 'team_time_cards')):
        columns_list = columns_list[region]
        additional_columns_list = additional_columns_list[region]
    logger.debug(F"Casting fromat based on the schema")
    for col_def in (columns_list + additional_columns_list):
        col = col_def["alias"]
        col_type = col_def["type"]

        if col not in df.columns:
            continue

        # print(col)
        if (col_type == "datetime") & (col != "dw_timestamp"):
            df[col] = pd.to_datetime(df[col], errors="coerce")
            df[col] = df[col].astype(object)
            df[col] = df[col].where(pd.notnull(df[col]), None)

        # elif col_type == "float":
        #     df[col] = df[col].astype(object)
        #     df[col] = df[col].where(pd.notnull(df[col]), None)
        # elif col_type == "int":
        #     # df[col] = pd.to_numeric(df[col], errors="coerce").astype("Int64")

        #     df[col] = df[col].astype(object)
        #     df[col] = df[col].where(pd.notnull(df[col]), None)
        elif col_type == "float":
            df[col] = pd.to_numeric(df[col], errors="coerce")
            df[col] = df[col].apply(lambda x: float(x) if pd.notnull(x) else 0)
        elif col_type == "int":
            df[col] = pd.to_numeric(df[col], errors="coerce")
            df[col] = df[col].apply(lambda x: int(x) if pd.notnull(x) else 0)
        elif col_type == "bool":
            df[col] = df[col].where(pd.notnull(df[col]), False)
            df[col] = df[col].astype(bool)           
        else:  # treat as string
            df[col] = df[col].astype(object)
            df[col] = df[col].where(pd.notnull(df[col]), None)
            
    # df = df.where(pd.notnull(df), None)

    return df

def prepare_df_from_parquet_v2(df, endpoint_name):
    schema = columns_mapping_dict[endpoint_name]

    for col_def in (schema["columns_list"] + schema["additional_column_list"]):
        col = col_def["alias"]
        col_type = col_def["type"]

        if col not in df.columns:
            continue

        # DATETIME
        if col_type == "datetime":
            df[col] = pd.to_datetime(df[col], errors="coerce")
            df[col] = df[col].where(pd.notnull(df[col]), None)

        # FLOAT / DECIMAL
        elif col_type == "float":
            df[col] = pd.to_numeric(df[col], errors="coerce")
            df[col] = df[col].where(pd.notnull(df[col]), None)

        # INT
        elif col_type == "int":
            df[col] = pd.to_numeric(df[col], errors="coerce").astype("Int64")
            df[col] = df[col].where(pd.notnull(df[col]), None)

        # BOOL → BIT
        elif col_type == "bool":
            df[col] = df[col].map(
                lambda x: 1 if x in [True, "true", "True", 1]
                else 0 if x in [False, "false", "False", 0]
                else None
            )

        # STRING
        else:
            df[col] = df[col].astype(object)
            df[col] = df[col].where(pd.notnull(df[col]), None)

    return df


regions_list = {
    "Southeast": 1,
    "Central":7
}

endpoints = [
    {"endpoint_name": "workers", "sql_table_name": "evi_adp_workers"},
    {"endpoint_name": "team_time_cards", "sql_table_name": "evi_adp_team_time_cards"},
    {"endpoint_name": "pay_statements", "sql_table_name": "evi_adp_pay_statements"},
    {
        "endpoint_name": "pay_statement_details",
        "sql_table_name": "evi_adp_pay_statement_details",
    },
]

def execute_stage_table_truncate_insert(region, sql_table_stg_name, df):
    sql_procedure_truncate(sql_table_stg_name)
    sql_procedure_insert(df, sql_table_stg_name, region)
    

def clean_numeric(val):
    if val in ("", None, "None", "nan", "NaN"):
        return None
    return val

def main():
    date_time = datetime.now()
    # date_time = datetime.now() - timedelta(days=1)
    if len(sys.argv) == 2:
        region_name = sys.argv[1]
        print(sys.argv)
    
        logger = setup_logging(f"{log_path}{region_name}_{script_name}.log")
        logger.debug(f"-------- Executing {script_name} ---------")
        logger.debug(f"Datetime = {date_time.strftime('%m-%d-%y %H:%M:%S')}")

    # for region in regions_list:
        region_id = regions_list[region_name]
        logger.info(F"Starting for region {region_name}, region_id: {region_id}")
        print(f'{region_name}, region_id: {region_id}')
        
        for endpoint_data in endpoints:
            endpoint_name = endpoint_data["endpoint_name"]
            sql_table = endpoint_data["sql_table_name"]
            logger.info(F"Starting for endpoint {endpoint_name}, sql_table: {sql_table}")
            
            df = read_sf_parquet_data_from_datalake(region_name, endpoint_name, date_time)
            if df is not None:
                df = prepare_df_from_parquet(df, endpoint_name, region_name)
                # df = prepare_df_from_parquet_v2(df, endpoint_name)
                
                if endpoint_name in stg_endpoints_list:
                    silver_sql_table_name = sql_table
                    sql_table_stg_name = f"stg_{silver_sql_table_name}_{region_name}"
                    sql_key_columns = ['id','region_id']
                    logger.info(F"Starting Stage Table procedure {sql_table_stg_name}")
                    # insert_to_sql_row_by_row(df, sql_table_stg_name)
                    execute_stage_table_truncate_insert(region_name, sql_table_stg_name, df)
                    sql_merge_staging_into_silver_auto(
                        silver_sql_table_name,
                        sql_table_stg_name,
                        sql_key_columns
                    )
                else:
                    print("Overwrite Entire Table")
                    logger.info(F"Overwrite Entire Table {endpoint_name}, sql_table: {sql_table}")
                    delete_records(sql_table, region_id)
                    insert_to_sql_dw(df, sql_table, "insert")


if __name__ == "__main__":
    start = timeit.default_timer()
    main()
    end = timeit.default_timer()
    print(f"Duration: {end - start} secs")
    print(f"Duration: {(end - start) / 60} mins")
    logger.debug(f"Duration: {end - start} secs")
    logger.debug(f"Duration: {(end - start) / 60} mins")
