def export_to_files(df, file_name, output_path, logger, export_selection=[True, True, False]):
    if (export_selection[0]):
        logger.debug(f"Exporting to CSV: {file_name}")
        df.to_csv(
            f'{output_path}/csv/{file_name}.csv.gz', index=False, compression="gzip")
    if (export_selection[1]):

        logger.debug(f"Exporting to Parquet: {file_name}")
        df.to_parquet(
            f'{output_path}/parquet/{file_name}.parquet', index=False)
    if (export_selection[2]):
        logger.debug(f"Exporting to Excel: {file_name}")
        df.to_excel(
            f'{output_path}/excel/{file_name}.xlsx', index=False)
