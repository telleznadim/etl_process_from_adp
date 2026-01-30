import pyodbc
import os
from dotenv import dotenv_values
from pathlib import Path
import logging

logger = logging.getLogger(__name__)

# Path to this file
current_file = Path(__file__).resolve()

# Go up to project root
project_root = current_file.parents[2]

config = dotenv_values(f"{project_root}/.env")


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


def get_team_time_cards_max_start_date(region_id):
    logger.info("Starting get_team_time_cards_max_start_date")
    
    query = f"""
    SELECT MAX(time_period_start_date) AS max_start_date
    FROM evi_adp_team_time_cards
    WHERE region_id = ?;
    """
    conn = create_sql_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(query, region_id)
        result = cursor.fetchone()
        result_to_return = result[0] if result else None
        
        print(f"Returning result, MAX(time_period_start_date) = '{result_to_return}'")
        logger.debug(f"Returning result, MAX(time_period_start_date) = '{result_to_return}'")
        return result_to_return

    finally:
        cursor.close()
        conn.close()
    