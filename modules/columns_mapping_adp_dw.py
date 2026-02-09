southeast_team_time_cards_columns_list = [
    {"name": "associateOID", "alias": "associate_oid", "type": "str"},
    {"name": "workerID", "alias": "worker_id", "type": "str"},
    {"name": "formattedName", "alias": "formatted_name", "type": "str"},
    {"name": "familyName", "alias": "family_name", "type": "str"},
    {"name": "givenName", "alias": "given_name", "type": "str"},
    {
        "name": "processingStatusCode",
        "alias": "processing_status_code",
        "type": "str",
    },
    {"name": "periodCode", "alias": "period_code", "type": "str"},
    {
        "name": "periodCodeShortName",
        "alias": "period_code_short_name",
        "type": "str",
    },
    {
        "name": "timePeriodStartDate",
        "alias": "time_period_start_date",
        "type": "date",
    },
    {
        "name": "timePeriodEndDate",
        "alias": "time_period_end_date",
        "type": "date",
    },
    {"name": "periodStatus", "alias": "period_status", "type": "str"},
    {
        "name": "REGULAR_periodTimeDuration",
        "alias": "regular_period_time_duration",
        "type": "str",
    },
    {
        "name": "OVERTIME_periodTimeDuration",
        "alias": "overtime_period_time_duration",
        "type": "str",
    },
    {"name": "entryDate", "alias": "entry_date", "type": "date"},
    {
        "name": "REGULAR_timeDuration",
        "alias": "regular_time_duration",
        "type": "str",
    },
    {
        "name": "OVERTIME_timeDuration",
        "alias": "overtime_time_duration",
        "type": "str",
    },
    {
        "name": "HOLIDAY_periodTimeDuration",
        "alias": "holiday_period_time_duration",
        "type": "str",
    },
    {
        "name": "HOLIDAY_timeDuration",
        "alias": "holiday_time_duration",
        "type": "str",
    },
    {
        "name": "PTO_periodTimeDuration",
        "alias": "pto_period_time_duration",
        "type": "str",
    },
    {"name": "PTO_timeDuration", "alias": "pto_time_duration", "type": "str"},
    {
        "name": "BEREAV_periodTimeDuration",
        "alias": "bereavement_period_time_duration",
        "type": "str",
    },
    {
        "name": "BEREAV_timeDuration",
        "alias": "bereavement_time_duration",
        "type": "str",
    },
    {
        "name": "REGSAL_periodTimeDuration",
        "alias": "regsal_period_time_duration",
        "type": "str",
    },
    {
        "name": "REGSAL_timeDuration",
        "alias": "regsal_time_duration",
        "type": "str",
    },
    # REGULAR
    {
        "name": "REGULAR_periodRateBaseMultiplier",
        "alias": "regular_period_rate_base_multiplier",
        "type": "float",
    },
    {
        "name": "REGULAR_periodRateAmount",
        "alias": "regular_period_rate_amount",
        "type": "float",
    },

    # PTO
    {
        "name": "PTO_periodRateAmount",
        "alias": "pto_period_rate_amount",
        "type": "float",
    },
    {
        "name": "PTO_periodRateBaseMultiplier",
        "alias": "pto_period_rate_base_multiplier",
        "type": "float",
    },

    # OVERTIME
    {
        "name": "OVERTIME_periodRateBaseMultiplier",
        "alias": "overtime_period_rate_base_multiplier",
        "type": "float",
    },
    {
        "name": "OVERTIME_periodRateAmount",
        "alias": "overtime_period_rate_amount",
        "type": "float",
    },
    
    # REGULAR
    {
        "name": "REGULAR_rateBaseMultiplier",
        "alias": "regular_rate_base_multiplier",
        "type": "float",
    },
    {
        "name": "REGULAR_rateAmount",
        "alias": "regular_rate_amount",
        "type": "float",
    },

    # PTO
    {
        "name": "PTO_rateBaseMultiplier",
        "alias": "pto_rate_base_multiplier",
        "type": "float",
    },
    {
        "name": "PTO_rateAmount",
        "alias": "pto_rate_amount",
        "type": "float",
    },

    # OVERTIME
    {
        "name": "OVERTIME_rateBaseMultiplier",
        "alias": "overtime_rate_base_multiplier",
        "type": "float",
    },
    {
        "name": "OVERTIME_rateAmount",
        "alias": "overtime_rate_amount",
        "type": "float",
    },
    
    {
        "name": "BEREAV_periodRateBaseMultiplier",
        "alias": "bereavement_period_rate_base_multiplier",
        "type": "float",
    },
    {
        "name": "BEREAV_periodRateAmount",
        "alias": "bereavement_period_rate_amount",
        "type": "float",
    },

    {
        "name": "BEREAV_rateBaseMultiplier",
        "alias": "bereavement_rate_base_multiplier",
        "type": "float",
    },
    {
        "name": "BEREAV_rateAmount",
        "alias": "bereavement_rate_amount",
        "type": "float",
    },
    
    {
        "name": "REGSAL_periodRateBaseMultiplier",
        "alias": "regsal_period_rate_base_multiplier",
        "type": "float",
    },
    {
        "name": "REGSAL_periodRateAmount",
        "alias": "regsal_period_rate_amount",
        "type": "float",
    },

    {
        "name": "REGSAL_rateBaseMultiplier",
        "alias": "regsal_rate_base_multiplier",
        "type": "float",
    },
    {
        "name": "REGSAL_rateAmount",
        "alias": "regsal_rate_amount",
        "type": "float",
    },
    
    
    {"name": "DW_ERP_System", "alias": "dw_erp_system", "type": "str"},
    {"name": "DW_Timestamp", "alias": "dw_timestamp", "type": "datetime"},
    {
        "name": "DW_ERP_Source_Table",
        "alias": "dw_erp_source_table",
        "type": "str",
    },
    {"name": "Region_Id", "alias": "region_id", "type": "int"},
    {"name": "id", "alias": "id", "type": "str"},
]

southeast_team_time_cards_additional_columns_list = [
    {"alias": "regular_period_time_duration_minutes", "type": "float"},
    {"alias": "regular_time_duration_minutes", "type": "float"},
    {"alias": "overtime_period_time_duration_minutes", "type": "float"},
    {"alias": "overtime_time_duration_minutes", "type": "float"},
    {"alias": "holiday_period_time_duration_minutes", "type": "float"},
    {"alias": "holiday_time_duration_minutes", "type": "float"},
    {"alias": "pto_period_time_duration_minutes", "type": "float"},
    {"alias": "pto_time_duration_minutes", "type": "float"},
    {"alias": "bereavement_period_time_duration_minutes", "type": "float"},
    {"alias": "bereavement_time_duration_minutes", "type": "float"},
    {"alias": "regsal_period_time_duration_minutes", "type": "float"},
    {"alias": "regsal_time_duration_minutes", "type": "float"},
]

central_team_time_cards_columns_list = [
    {"name": "associateOID", "alias": "associate_oid", "type": "str"},
    {"name": "workerID", "alias": "worker_id", "type": "str"},
    {"name": "formattedName", "alias": "formatted_name", "type": "str"},
    {"name": "familyName", "alias": "family_name", "type": "str"},
    {"name": "givenName", "alias": "given_name", "type": "str"},
    {
        "name": "processingStatusCode",
        "alias": "processing_status_code",
        "type": "str",
    },
    {"name": "periodCode", "alias": "period_code", "type": "str"},
    {
        "name": "periodCodeShortName",
        "alias": "period_code_short_name",
        "type": "str",
    },
    {
        "name": "timePeriodStartDate",
        "alias": "time_period_start_date",
        "type": "date",
    },
    {
        "name": "timePeriodEndDate",
        "alias": "time_period_end_date",
        "type": "date",
    },
    {"name": "periodStatus", "alias": "period_status", "type": "str"},
    {"name": "entryDate", "alias": "entry_date", "type": "date"},
    {
        "name": "REGULAR_periodTimeDuration",
        "alias": "regular_period_time_duration",
        "type": "str",
    },
    {
        "name": "REGULAR_timeDuration",
        "alias": "regular_time_duration",
        "type": "str",
    },
    {
        "name": "SIC_periodTimeDuration",
        "alias": "sick_period_time_duration",
        "type": "str",
    },
    {
        "name": "SIC_timeDuration",
        "alias": "sick_time_duration",
        "type": "str",
    },
    {
        "name": "OVERTIME_periodTimeDuration",
        "alias": "overtime_period_time_duration",
        "type": "str",
    },
    {
        "name": "OVERTIME_timeDuration",
        "alias": "overtime_time_duration",
        "type": "str",
    },
    {
        "name": "VAC_periodTimeDuration",
        "alias": "pto_period_time_duration",
        "type": "str",
    },
    {"name": "VAC_timeDuration", "alias": "pto_time_duration", "type": "str"},
    {
        "name": "BEREAV_periodTimeDuration",
        "alias": "bereavement_period_time_duration",
        "type": "str",
    },
    {
        "name": "BEREAV_timeDuration",
        "alias": "bereavement_time_duration",
        "type": "str",
    },
    {
        "name": "FLA_periodTimeDuration",
        "alias": "fla_period_time_duration",
        "type": "str",
    },
    {
        "name": "FLA_timeDuration",
        "alias": "fla_time_duration",
        "type": "str",
    },
    {"name": "DW_ERP_System", "alias": "dw_erp_system", "type": "str"},
    {"name": "DW_Timestamp", "alias": "dw_timestamp", "type": "datetime"},
    {
        "name": "DW_ERP_Source_Table",
        "alias": "dw_erp_source_table",
        "type": "str",
    },
    {"name": "Region_Id", "alias": "region_id", "type": "int"},
    {"name": "id", "alias": "id", "type": "str"}
]

central_team_time_cards_additional_columns_list = [
    {"alias": "regular_period_time_duration_minutes", "type": "float"},
    {"alias": "regular_time_duration_minutes", "type": "float"},
    {"alias": "overtime_period_time_duration_minutes", "type": "float"},
    {"alias": "overtime_time_duration_minutes", "type": "float"},
    {"alias": "sick_period_time_duration_minutes", "type": "float"},
    {"alias": "sick_time_duration_minutes", "type": "float"},
    {"alias": "pto_period_time_duration_minutes", "type": "float"},
    {"alias": "pto_time_duration_minutes", "type": "float"},
    {"alias": "bereavement_period_time_duration_minutes", "type": "float"},
    {"alias": "bereavement_time_duration_minutes", "type": "float"},
    {"alias": "fla_period_time_duration_minutes", "type": "float"},
    {"alias": "fla_time_duration_minutes", "type": "float"},
]		

central_pay_statement_details_columns = [
    {"name": "associateOID", "alias": "associate_oid", "type": "str"},
    {"name": "region", "alias": "region", "type": "str"},
    {"name": "payStatementId", "alias": "pay_statement_id", "type": "str"},
    {"name": "payDetailUri", "alias": "pay_detail_uri", "type": "str"},
    {"name": "payDate", "alias": "pay_date", "type": "date"},
    {
        "name": "payPeriodStartDate",
        "alias": "pay_period_start_date",
        "type": "date",
    },
    {
        "name": "payPeriodEndDate",
        "alias": "pay_period_end_date",
        "type": "date",
    },
    {"name": "netPayAmount", "alias": "net_pay_amount", "type": "float"},
    {"name": "grossPayAmount", "alias": "gross_pay_amount", "type": "float"},
    {
        "name": "grossPayYTDAmount",
        "alias": "gross_pay_ytd_amount",
        "type": "float",
    },
    {"name": "totalHours", "alias": "total_hours", "type": "float"},
    # Regular
    {"name": "Regular_amount", "alias": "regular_amount", "type": "float"},
    {
        "name": "Regular_ytdAmount",
        "alias": "regular_ytd_amount",
        "type": "float",
    },
    {"name": "Regular_hours", "alias": "regular_hours", "type": "float"},
    {"name": "Regular_payRate", "alias": "regular_pay_rate", "type": "float"},
    {
        "name": "Regular_preTaxIndicator",
        "alias": "regular_pre_tax_indicator",
        "type": "bool",
    },
    # Overtime
    {"name": "Overtime_amount", "alias": "overtime_amount", "type": "float"},
    {
        "name": "Overtime_ytdAmount",
        "alias": "overtime_ytd_amount",
        "type": "float",
    },
    {"name": "Overtime_hours", "alias": "overtime_hours", "type": "float"},
    {"name": "Overtime_payRate", "alias": "overtime_pay_rate", "type": "float"},
    {
        "name": "Overtime_preTaxIndicator",
        "alias": "overtime_pre_tax_indicator",
        "type": "bool",
    },
    # Holiday
    {"name": "Holiday_amount", "alias": "holiday_amount", "type": "float"},
    {
        "name": "Holiday_ytdAmount",
        "alias": "holiday_ytd_amount",
        "type": "float",
    },
    {"name": "Holiday_hours", "alias": "holiday_hours", "type": "float"},
    {"name": "Holiday_payRate", "alias": "holiday_pay_rate", "type": "float"},
    {
        "name": "Holiday_preTaxIndicator",
        "alias": "holiday_pre_tax_indicator",
        "type": "bool",
    },
    # Dividend
    {"name": "Dividends_amount", "alias": "dividend_amount", "type": "float"},
    {
        "name": "Dividends_ytdAmount",
        "alias": "dividend_ytd_amount",
        "type": "float",
    },
    {"name": "Dividends_hours", "alias": "dividend_hours", "type": "float"},
    {"name": "Dividends_payRate", "alias": "dividend_pay_rate", "type": "float"},
    {
        "name": "Dividends_preTaxIndicator",
        "alias": "dividend_pre_tax_indicator",
        "type": "bool",
    },
    # Bereavement
    {
        "name": "Bereavemen_amount",
        "alias": "bereavement_amount",
        "type": "float",
    },
    {
        "name": "Bereavemen_ytdAmount",
        "alias": "bereavement_ytd_amount",
        "type": "float",
    },
    {
        "name": "Bereavemen_hours",
        "alias": "bereavement_hours",
        "type": "float",
    },
    {
        "name": "Bereavemen_payRate",
        "alias": "bereavement_pay_rate",
        "type": "float",
    },
    {
        "name": "Bereavemen_preTaxIndicator",
        "alias": "bereavement_pre_tax_indicator",
        "type": "bool",
    },
    # Bonus
    {
        "name": "Bonus_amount",
        "alias": "bonus_amount",
        "type": "float",
    },
    {
        "name": "Bonus_ytdAmount",
        "alias": "bonus_ytd_amount",
        "type": "float",
    },
    {
        "name": "Bonus_hours",
        "alias": "bonus_hours",
        "type": "float",
    },
    {
        "name": "Bonus_payRate",
        "alias": "bonus_pay_rate",
        "type": "float",
    },
    {
        "name": "Bonus_preTaxIndicator",
        "alias": "bonus_pre_tax_indicator",
        "type": "bool",
    },
    # Commission
    {
        "name": "Commissions_amount",
        "alias": "commission_amount",
        "type": "float",
    },
    {
        "name": "Commissions_ytdAmount",
        "alias": "commission_ytd_amount",
        "type": "float",
    },
    {"name": "Commissions_hours", "alias": "commission_hours", "type": "float"},
    {
        "name": "Commissions_payRate",
        "alias": "commission_pay_rate",
        "type": "float",
    },
    {
        "name": "Commissions_preTaxIndicator",
        "alias": "commission_pre_tax_indicator",
        "type": "bool",
    },
    # Retroactive
    {
        "name": "Retro_Pay_amount",
        "alias": "retroactive_amount",
        "type": "float",
    },
    {
        "name": "Retro_Pay_ytdAmount",
        "alias": "retroactive_ytd_amount",
        "type": "float",
    },
    {
        "name": "Retro_Pay_hours",
        "alias": "retroactive_hours",
        "type": "float",
    },
    {
        "name": "Retro_Pay_payRate",
        "alias": "retroactive_pay_rate",
        "type": "float",
    },
    {
        "name": "Retro_Pay_preTaxIndicator",
        "alias": "retroactive_pre_tax_indicator",
        "type": "bool",
    },
    # Severance
    {
        "name": "Severance_amount",
        "alias": "severance_amount",
        "type": "float",
    },
    {
        "name": "Severance_ytdAmount",
        "alias": "severance_ytd_amount",
        "type": "float",
    },
    {
        "name": "Severance_hours",
        "alias": "severance_hours",
        "type": "float",
    },
    {
        "name": "Severance_payRate",
        "alias": "severance_pay_rate",
        "type": "float",
    },
    {
        "name": "Severance_preTaxIndicator",
        "alias": "severance_pre_tax_indicator",
        "type": "bool",
    },
    # PTO
    {
        "name": "Vacation_Paid_amount",
        "alias": "pto_amount",
        "type": "float",
    },
    {
        "name": "Vacation_Paid_ytdAmount",
        "alias": "pto_ytd_amount",
        "type": "float",
    },
    {
        "name": "Vacation_Paid_hours",
        "alias": "pto_hours",
        "type": "float",
    },
    {
        "name": "Vacation_Paid_payRate",
        "alias": "pto_pay_rate",
        "type": "float",
    },
    {
        "name": "Vacation_Paid_preTaxIndicator",
        "alias": "pto_pre_tax_indicator",
        "type": "bool",
    },
    # Pto (variant)
    {
        "name": "VACATIONPAI_amount",
        "alias": "pto_amount_variant",
        "type": "float",
    },
    {
        "name": "VACATIONPAI_ytdAmount",
        "alias": "pto_ytd_amount_variant",
        "type": "float",
    },
    {
        "name": "VACATIONPAI_hours",
        "alias": "pto_hours_variant",
        "type": "float",
    },
    {
        "name": "VACATIONPAI_payRate",
        "alias": "pto_pay_rate_variant",
        "type": "float",
    },
    {
        "name": "VACATIONPAI_preTaxIndicator",
        "alias": "pto_pre_tax_indicator_variant",
        "type": "bool",
    },
    # Car Allowance
    {
        "name": "Auto_Allow_amount",
        "alias": "car_allowance_amount",
        "type": "float",
    },
    {
        "name": "Auto_Allow_ytdAmount",
        "alias": "car_allowance_ytd_amount",
        "type": "float",
    },
    {
        "name": "Auto_Allow_hours",
        "alias": "car_allowance_hours",
        "type": "float",
    },
    {
        "name": "Auto_Allow_payRate",
        "alias": "car_allowance_pay_rate",
        "type": "float",
    },
    {
        "name": "Auto_Allow_preTaxIndicator",
        "alias": "car_allowance_pre_tax_indicator",
        "type": "bool",
    },
    # Cell Allowance
    {
        "name": "Cell_Allowance_amount",
        "alias": "cell_allowance_amount",
        "type": "float",
    },
    {
        "name": "Cell_Allowance_ytdAmount",
        "alias": "cell_allowance_ytd_amount",
        "type": "float",
    },
    {
        "name": "Cell_Allowance_hours",
        "alias": "cell_allowance_hours",
        "type": "float",
    },
    {
        "name": "Cell_Allowance_payRate",
        "alias": "cell_allowance_pay_rate",
        "type": "float",
    },
    {
        "name": "Cell_Allowance_preTaxIndicator",
        "alias": "cell_allowance_pre_tax_indicator",
        "type": "bool",
    },

    # Deceased Pay
    {
        "name": "Deceased_Pay_amount",
        "alias": "deceased_pay_amount",
        "type": "float",
    },
    {
        "name": "Deceased_Pay_ytdAmount",
        "alias": "deceased_pay_ytd_amount",
        "type": "float",
    },
    {
        "name": "Deceased_Pay_hours",
        "alias": "deceased_pay_hours",
        "type": "float",
    },
    {
        "name": "Deceased_Pay_payRate",
        "alias": "deceased_pay_rate",
        "type": "float",
    },
    {
        "name": "Deceased_Pay_preTaxIndicator",
        "alias": "deceased_pay_pre_tax_indicator",
        "type": "bool",
    },

    # FMLA
    {
        "name": "FMLA_amount",
        "alias": "fmla_amount",
        "type": "float",
    },
    {
        "name": "FMLA_ytdAmount",
        "alias": "fmla_ytd_amount",
        "type": "float",
    },
    {
        "name": "FMLA_hours",
        "alias": "fmla_hours",
        "type": "float",
    },
    {
        "name": "FMLA_payRate",
        "alias": "fmla_pay_rate",
        "type": "float",
    },
    {
        "name": "FMLA_preTaxIndicator",
        "alias": "fmla_pre_tax_indicator",
        "type": "bool",
    },

    # Mileage
    {
        "name": "Mileage_amount",
        "alias": "mileage_amount",
        "type": "float",
    },
    {
        "name": "Mileage_ytdAmount",
        "alias": "mileage_ytd_amount",
        "type": "float",
    },
    {
        "name": "Mileage_hours",
        "alias": "mileage_hours",
        "type": "float",
    },
    {
        "name": "Mileage_payRate",
        "alias": "mileage_pay_rate",
        "type": "float",
    },
    {
        "name": "Mileage_preTaxIndicator",
        "alias": "mileage_pre_tax_indicator",
        "type": "bool",
    },

    # Office Closure
    {
        "name": "OfficeClosure_amount",
        "alias": "office_closure_amount",
        "type": "float",
    },
    {
        "name": "OfficeClosure_ytdAmount",
        "alias": "office_closure_ytd_amount",
        "type": "float",
    },
    {
        "name": "OfficeClosure_hours",
        "alias": "office_closure_hours",
        "type": "float",
    },
    {
        "name": "OfficeClosure_payRate",
        "alias": "office_closure_pay_rate",
        "type": "float",
    },
    {
        "name": "OfficeClosure_preTaxIndicator",
        "alias": "office_closure_pre_tax_indicator",
        "type": "bool",
    },

    # Restricted Share Vest
    {
        "name": "RestriShareVest_amount",
        "alias": "restricted_share_vest_amount",
        "type": "float",
    },
    {
        "name": "RestriShareVest_ytdAmount",
        "alias": "restricted_share_vest_ytd_amount",
        "type": "float",
    },
    {
        "name": "RestriShareVest_hours",
        "alias": "restricted_share_vest_hours",
        "type": "float",
    },
    {
        "name": "RestriShareVest_payRate",
        "alias": "restricted_share_vest_pay_rate",
        "type": "float",
    },
    {
        "name": "RestriShareVest_preTaxIndicator",
        "alias": "restricted_share_vest_pre_tax_indicator",
        "type": "bool",
    },

    # Sick Time Off
    {
        "name": "Sick_Time_Off_amount",
        "alias": "sick_time_off_amount",
        "type": "float",
    },
    {
        "name": "Sick_Time_Off_ytdAmount",
        "alias": "sick_time_off_ytd_amount",
        "type": "float",
    },
    {
        "name": "Sick_Time_Off_hours",
        "alias": "sick_time_off_hours",
        "type": "float",
    },
    {
        "name": "Sick_Time_Off_payRate",
        "alias": "sick_time_off_pay_rate",
        "type": "float",
    },
    {
        "name": "Sick_Time_Off_preTaxIndicator",
        "alias": "sick_time_off_pre_tax_indicator",
        "type": "bool",
    },

    # Spiff Bonus
    {
        "name": "Spiff_Bonus_amount",
        "alias": "spiff_bonus_amount",
        "type": "float",
    },
    {
        "name": "Spiff_Bonus_ytdAmount",
        "alias": "spiff_bonus_ytd_amount",
        "type": "float",
    },
    {
        "name": "Spiff_Bonus_hours",
        "alias": "spiff_bonus_hours",
        "type": "float",
    },
    {
        "name": "Spiff_Bonus_payRate",
        "alias": "spiff_bonus_pay_rate",
        "type": "float",
    },
    {
        "name": "Spiff_Bonus_preTaxIndicator",
        "alias": "spiff_bonus_pre_tax_indicator",
        "type": "bool",
    },
    # Unpaid Jury Duty
    {
        "name": "Unpd_Juryduty_amount",
        "alias": "unpaid_jury_duty_amount",
        "type": "float",
    },
    {
        "name": "Unpd_Juryduty_ytdAmount",
        "alias": "unpaid_jury_duty_ytd_amount",
        "type": "float",
    },
    {
        "name": "Unpd_Juryduty_hours",
        "alias": "unpaid_jury_duty_hours",
        "type": "float",
    },
    {
        "name": "Unpd_Juryduty_payRate",
        "alias": "unpaid_jury_duty_pay_rate",
        "type": "float",
    },
    {
        "name": "Unpd_Juryduty_preTaxIndicator",
        "alias": "unpaid_jury_duty_pre_tax_indicator",
        "type": "bool",
    },
    # DW / Region
    {"name": "DW_ERP_System", "alias": "dw_erp_system", "type": "str"},
    {"name": "DW_Timestamp", "alias": "dw_timestamp", "type": "datetime"},
    {
        "name": "DW_ERP_Source_Table",
        "alias": "dw_erp_source_table",
        "type": "str",
    },
    {"name": "Region_Id", "alias": "region_id", "type": "int"},
    {"name": "id", "alias": "id", "type": "str"},
    
]

southeast_pay_statement_details_columns = [
        {"name": "associateOID", "alias": "associate_oid", "type": "str"},
        {"name": "region", "alias": "region", "type": "str"},
        {"name": "payStatementId", "alias": "pay_statement_id", "type": "str"},
        {"name": "payDetailUri", "alias": "pay_detail_uri", "type": "str"},
        {"name": "payDate", "alias": "pay_date", "type": "date"},
        {
            "name": "payPeriodStartDate",
            "alias": "pay_period_start_date",
            "type": "date",
        },
        {
            "name": "payPeriodEndDate",
            "alias": "pay_period_end_date",
            "type": "date",
        },
        {"name": "netPayAmount", "alias": "net_pay_amount", "type": "float"},
        {"name": "grossPayAmount", "alias": "gross_pay_amount", "type": "float"},
        {
            "name": "grossPayYTDAmount",
            "alias": "gross_pay_ytd_amount",
            "type": "float",
        },
        {"name": "totalHours", "alias": "total_hours", "type": "float"},
        # Regular
        {"name": "Regular_amount", "alias": "regular_amount", "type": "float"},
        {
            "name": "Regular_ytdAmount",
            "alias": "regular_ytd_amount",
            "type": "float",
        },
        {"name": "Regular_hours", "alias": "regular_hours", "type": "float"},
        {"name": "Regular_payRate", "alias": "regular_pay_rate", "type": "float"},
        {
            "name": "Regular_preTaxIndicator",
            "alias": "regular_pre_tax_indicator",
            "type": "bool",
        },
        # Overtime
        {"name": "Overtime_amount", "alias": "overtime_amount", "type": "float"},
        {
            "name": "Overtime_ytdAmount",
            "alias": "overtime_ytd_amount",
            "type": "float",
        },
        {"name": "Overtime_hours", "alias": "overtime_hours", "type": "float"},
        {"name": "Overtime_payRate", "alias": "overtime_pay_rate", "type": "float"},
        {
            "name": "Overtime_preTaxIndicator",
            "alias": "overtime_pre_tax_indicator",
            "type": "bool",
        },
        # Paid Time Off
        {
            "name": "Paid_Time_Off_amount",
            "alias": "paid_time_off_amount",
            "type": "float",
        },
        {
            "name": "Paid_Time_Off_ytdAmount",
            "alias": "paid_time_off_ytd_amount",
            "type": "float",
        },
        {
            "name": "Paid_Time_Off_hours",
            "alias": "paid_time_off_hours",
            "type": "float",
        },
        {
            "name": "Paid_Time_Off_payRate",
            "alias": "paid_time_off_pay_rate",
            "type": "float",
        },
        {
            "name": "Paid_Time_Off_preTaxIndicator",
            "alias": "paid_time_off_pre_tax_indicator",
            "type": "bool",
        },
        # Holiday
        {"name": "Holiday_amount", "alias": "holiday_amount", "type": "float"},
        {
            "name": "Holiday_ytdAmount",
            "alias": "holiday_ytd_amount",
            "type": "float",
        },
        {"name": "Holiday_hours", "alias": "holiday_hours", "type": "float"},
        {"name": "Holiday_payRate", "alias": "holiday_pay_rate", "type": "float"},
        {
            "name": "Holiday_preTaxIndicator",
            "alias": "holiday_pre_tax_indicator",
            "type": "bool",
        },
        # Weekend
        {
            "name": "Weekend_Cal_amount",
            "alias": "weekend_cal_amount",
            "type": "float",
        },
        {
            "name": "Weekend_Cal_ytdAmount",
            "alias": "weekend_cal_ytd_amount",
            "type": "float",
        },
        {
            "name": "Weekend_Cal_hours",
            "alias": "weekend_cal_hours",
            "type": "float",
        },
        {
            "name": "Weekend_Cal_payRate",
            "alias": "weekend_cal_pay_rate",
            "type": "float",
        },
        {
            "name": "Weekend_Cal_preTaxIndicator",
            "alias": "weekend_cal_pre_tax_indicator",
            "type": "bool",
        },
        # Retroactive
        {
            "name": "Retroactive_amount",
            "alias": "retroactive_amount",
            "type": "float",
        },
        {
            "name": "Retroactive_ytdAmount",
            "alias": "retroactive_ytd_amount",
            "type": "float",
        },
        {
            "name": "Retroactive_hours",
            "alias": "retroactive_hours",
            "type": "float",
        },
        {
            "name": "Retroactive_payRate",
            "alias": "retroactive_pay_rate",
            "type": "float",
        },
        {
            "name": "Retroactive_preTaxIndicator",
            "alias": "retroactive_pre_tax_indicator",
            "type": "bool",
        },
        # Bereavement
        {
            "name": "Bereavement_amount",
            "alias": "bereavement_amount",
            "type": "float",
        },
        {
            "name": "Bereavement_ytdAmount",
            "alias": "bereavement_ytd_amount",
            "type": "float",
        },
        {
            "name": "Bereavement_hours",
            "alias": "bereavement_hours",
            "type": "float",
        },
        {
            "name": "Bereavement_payRate",
            "alias": "bereavement_pay_rate",
            "type": "float",
        },
        {
            "name": "Bereavement_preTaxIndicator",
            "alias": "bereavement_pre_tax_indicator",
            "type": "bool",
        },
        # International
        {
            "name": "Internation_amount",
            "alias": "international_amount",
            "type": "float",
        },
        {
            "name": "Internation_ytdAmount",
            "alias": "international_ytd_amount",
            "type": "float",
        },
        {
            "name": "Internation_hours",
            "alias": "international_hours",
            "type": "float",
        },
        {
            "name": "Internation_payRate",
            "alias": "international_pay_rate",
            "type": "float",
        },
        {
            "name": "Internation_preTaxIndicator",
            "alias": "international_pre_tax_indicator",
            "type": "bool",
        },
        # Service Salary
        {
            "name": "Service_Sal_amount",
            "alias": "service_sal_amount",
            "type": "float",
        },
        {
            "name": "Service_Sal_ytdAmount",
            "alias": "service_sal_ytd_amount",
            "type": "float",
        },
        {
            "name": "Service_Sal_hours",
            "alias": "service_sal_hours",
            "type": "float",
        },
        {
            "name": "Service_Sal_payRate",
            "alias": "service_sal_pay_rate",
            "type": "float",
        },
        {
            "name": "Service_Sal_preTaxIndicator",
            "alias": "service_sal_pre_tax_indicator",
            "type": "bool",
        },
        # Service Professional
        {
            "name": "Service_Pro_amount",
            "alias": "service_pro_amount",
            "type": "float",
        },
        {
            "name": "Service_Pro_ytdAmount",
            "alias": "service_pro_ytd_amount",
            "type": "float",
        },
        {
            "name": "Service_Pro_hours",
            "alias": "service_pro_hours",
            "type": "float",
        },
        {
            "name": "Service_Pro_payRate",
            "alias": "service_pro_pay_rate",
            "type": "float",
        },
        {
            "name": "Service_Pro_preTaxIndicator",
            "alias": "service_pro_pre_tax_indicator",
            "type": "bool",
        },
        # Service RM
        {
            "name": "Service_RM_amount",
            "alias": "service_rm_amount",
            "type": "float",
        },
        {
            "name": "Service_RM_ytdAmount",
            "alias": "service_rm_ytd_amount",
            "type": "float",
        },
        {"name": "Service_RM_hours", "alias": "service_rm_hours", "type": "float"},
        {
            "name": "Service_RM_payRate",
            "alias": "service_rm_pay_rate",
            "type": "float",
        },
        {
            "name": "Service_RM_preTaxIndicator",
            "alias": "service_rm_pre_tax_indicator",
            "type": "bool",
        },
        # Car Allowance
        {
            "name": "Car_Allowan_amount",
            "alias": "car_allowance_amount",
            "type": "float",
        },
        {
            "name": "Car_Allowan_ytdAmount",
            "alias": "car_allowance_ytd_amount",
            "type": "float",
        },
        {
            "name": "Car_Allowan_hours",
            "alias": "car_allowance_hours",
            "type": "float",
        },
        {
            "name": "Car_Allowan_payRate",
            "alias": "car_allowance_pay_rate",
            "type": "float",
        },
        {
            "name": "Car_Allowan_preTaxIndicator",
            "alias": "car_allowance_pre_tax_indicator",
            "type": "bool",
        },
        # Commission
        {
            "name": "Commission_amount",
            "alias": "commission_amount",
            "type": "float",
        },
        {
            "name": "Commission_ytdAmount",
            "alias": "commission_ytd_amount",
            "type": "float",
        },
        {"name": "Commission_hours", "alias": "commission_hours", "type": "float"},
        {
            "name": "Commission_payRate",
            "alias": "commission_pay_rate",
            "type": "float",
        },
        {
            "name": "Commission_preTaxIndicator",
            "alias": "commission_pre_tax_indicator",
            "type": "bool",
        },
        # Reimbursement
        {
            "name": "Reimbursem_amount",
            "alias": "reimbursement_amount",
            "type": "float",
        },
        {
            "name": "Reimbursem_ytdAmount",
            "alias": "reimbursement_ytd_amount",
            "type": "float",
        },
        {
            "name": "Reimbursem_hours",
            "alias": "reimbursement_hours",
            "type": "float",
        },
        {
            "name": "Reimbursem_payRate",
            "alias": "reimbursement_pay_rate",
            "type": "float",
        },
        {
            "name": "Reimbursem_preTaxIndicator",
            "alias": "reimbursement_pre_tax_indicator",
            "type": "bool",
        },
        # Incentive Program
        {
            "name": "Incentive_Prog_amount",
            "alias": "incentive_prog_amount",
            "type": "float",
        },
        {
            "name": "Incentive_Prog_ytdAmount",
            "alias": "incentive_prog_ytd_amount",
            "type": "float",
        },
        {
            "name": "Incentive_Prog_hours",
            "alias": "incentive_prog_hours",
            "type": "float",
        },
        {
            "name": "Incentive_Prog_payRate",
            "alias": "incentive_prog_pay_rate",
            "type": "float",
        },
        {
            "name": "Incentive_Prog_preTaxIndicator",
            "alias": "incentive_prog_pre_tax_indicator",
            "type": "bool",
        },
        # Bonus Salary
        {
            "name": "Bonus___Sal_amount",
            "alias": "bonus_salary_amount",
            "type": "float",
        },
        {
            "name": "Bonus___Sal_ytdAmount",
            "alias": "bonus_salary_ytd_amount",
            "type": "float",
        },
        {
            "name": "Bonus___Sal_hours",
            "alias": "bonus_salary_hours",
            "type": "float",
        },
        {
            "name": "Bonus___Sal_payRate",
            "alias": "bonus_salary_pay_rate",
            "type": "float",
        },
        {
            "name": "Bonus___Sal_preTaxIndicator",
            "alias": "bonus_salary_pre_tax_indicator",
            "type": "bool",
        },
        # Dividend
        {"name": "Dividend_amount", "alias": "dividend_amount", "type": "float"},
        {
            "name": "Dividend_ytdAmount",
            "alias": "dividend_ytd_amount",
            "type": "float",
        },
        {"name": "Dividend_hours", "alias": "dividend_hours", "type": "float"},
        {"name": "Dividend_payRate", "alias": "dividend_pay_rate", "type": "float"},
        {
            "name": "Dividend_preTaxIndicator",
            "alias": "dividend_pre_tax_indicator",
            "type": "bool",
        },
        # Overnight Shift
        {
            "name": "Overnight_S_amount",
            "alias": "overnight_shift_amount",
            "type": "float",
        },
        {
            "name": "Overnight_S_ytdAmount",
            "alias": "overnight_shift_ytd_amount",
            "type": "float",
        },
        {
            "name": "Overnight_S_hours",
            "alias": "overnight_shift_hours",
            "type": "float",
        },
        {
            "name": "Overnight_S_payRate",
            "alias": "overnight_shift_pay_rate",
            "type": "float",
        },
        {
            "name": "Overnight_S_preTaxIndicator",
            "alias": "overnight_shift_pre_tax_indicator",
            "type": "bool",
        },
        # Bonus
        {
            "name": "Bonus_amount",
            "alias": "bonus_amount",
            "type": "float",
        },
        {
            "name": "Bonus_ytdAmount",
            "alias": "bonus_ytd_amount",
            "type": "float",
        },
        {
            "name": "Bonus_hours",
            "alias": "bonus_hours",
            "type": "float",
        },
        {
            "name": "Bonus_payRate",
            "alias": "bonus_pay_rate",
            "type": "float",
        },
        {
            "name": "Bonus_preTaxIndicator",
            "alias": "bonus_pre_tax_indicator",
            "type": "bool",
        },

        # MED
        {
            "name": "MED_amount",
            "alias": "med_amount",
            "type": "float",
        },
        {
            "name": "MED_ytdAmount",
            "alias": "med_ytd_amount",
            "type": "float",
        },
        {
            "name": "MED_hours",
            "alias": "med_hours",
            "type": "float",
        },
        {
            "name": "MED_payRate",
            "alias": "med_pay_rate",
            "type": "float",
        },
        {
            "name": "MED_preTaxIndicator",
            "alias": "med_pre_tax_indicator",
            "type": "bool",
        },

        # Med Reimburse
        {
            "name": "Med_Reimburse_amount",
            "alias": "med_reimburse_amount",
            "type": "float",
        },
        {
            "name": "Med_Reimburse_ytdAmount",
            "alias": "med_reimburse_ytd_amount",
            "type": "float",
        },
        {
            "name": "Med_Reimburse_hours",
            "alias": "med_reimburse_hours",
            "type": "float",
        },
        {
            "name": "Med_Reimburse_payRate",
            "alias": "med_reimburse_pay_rate",
            "type": "float",
        },
        {
            "name": "Med_Reimburse_preTaxIndicator",
            "alias": "med_reimburse_pre_tax_indicator",
            "type": "bool",
        },

        # PTO
        {
            "name": "PTO_amount",
            "alias": "pto_amount",
            "type": "float",
        },
        {
            "name": "PTO_ytdAmount",
            "alias": "pto_ytd_amount",
            "type": "float",
        },
        {
            "name": "PTO_hours",
            "alias": "pto_hours",
            "type": "float",
        },
        {
            "name": "PTO_payRate",
            "alias": "pto_pay_rate",
            "type": "float",
        },
        {
            "name": "PTO_preTaxIndicator",
            "alias": "pto_pre_tax_indicator",
            "type": "bool",
        },

        # PUCC
        {
            "name": "PUCC_amount",
            "alias": "pucc_amount",
            "type": "float",
        },
        {
            "name": "PUCC_ytdAmount",
            "alias": "pucc_ytd_amount",
            "type": "float",
        },
        {
            "name": "PUCC_hours",
            "alias": "pucc_hours",
            "type": "float",
        },
        {
            "name": "PUCC_payRate",
            "alias": "pucc_pay_rate",
            "type": "float",
        },
        {
            "name": "PUCC_preTaxIndicator",
            "alias": "pucc_pre_tax_indicator",
            "type": "bool",
        },

        # Pto (variant)
        {
            "name": "Pto_amount",
            "alias": "pto_amount_variant",
            "type": "float",
        },
        {
            "name": "Pto_ytdAmount",
            "alias": "pto_ytd_amount_variant",
            "type": "float",
        },
        {
            "name": "Pto_hours",
            "alias": "pto_hours_variant",
            "type": "float",
        },
        {
            "name": "Pto_payRate",
            "alias": "pto_pay_rate_variant",
            "type": "float",
        },
        {
            "name": "Pto_preTaxIndicator",
            "alias": "pto_pre_tax_indicator_variant",
            "type": "bool",
        },

        # STV
        {
            "name": "STV_amount",
            "alias": "stv_amount",
            "type": "float",
        },
        {
            "name": "STV_ytdAmount",
            "alias": "stv_ytd_amount",
            "type": "float",
        },
        {
            "name": "STV_hours",
            "alias": "stv_hours",
            "type": "float",
        },
        {
            "name": "STV_payRate",
            "alias": "stv_pay_rate",
            "type": "float",
        },
        {
            "name": "STV_preTaxIndicator",
            "alias": "stv_pre_tax_indicator",
            "type": "bool",
        },

        # Scorpt
        {
            "name": "Scorpt_amount",
            "alias": "scorpt_amount",
            "type": "float",
        },
        {
            "name": "Scorpt_ytdAmount",
            "alias": "scorpt_ytd_amount",
            "type": "float",
        },
        {
            "name": "Scorpt_hours",
            "alias": "scorpt_hours",
            "type": "float",
        },
        {
            "name": "Scorpt_payRate",
            "alias": "scorpt_pay_rate",
            "type": "float",
        },
        {
            "name": "Scorpt_preTaxIndicator",
            "alias": "scorpt_pre_tax_indicator",
            "type": "bool",
        },

        # Severance
        {
            "name": "Severance_amount",
            "alias": "severance_amount",
            "type": "float",
        },
        {
            "name": "Severance_ytdAmount",
            "alias": "severance_ytd_amount",
            "type": "float",
        },
        {
            "name": "Severance_hours",
            "alias": "severance_hours",
            "type": "float",
        },
        {
            "name": "Severance_payRate",
            "alias": "severance_pay_rate",
            "type": "float",
        },
        {
            "name": "Severance_preTaxIndicator",
            "alias": "severance_pre_tax_indicator",
            "type": "bool",
        },

        # Tech Leads
        {
            "name": "Tech_Leads_amount",
            "alias": "tech_leads_amount",
            "type": "float",
        },
        {
            "name": "Tech_Leads_ytdAmount",
            "alias": "tech_leads_ytd_amount",
            "type": "float",
        },
        {
            "name": "Tech_Leads_hours",
            "alias": "tech_leads_hours",
            "type": "float",
        },
        {
            "name": "Tech_Leads_payRate",
            "alias": "tech_leads_pay_rate",
            "type": "float",
        },
        {
            "name": "Tech_Leads_preTaxIndicator",
            "alias": "tech_leads_pre_tax_indicator",
            "type": "bool",
        },

        # Training
        {
            "name": "Training_amount",
            "alias": "training_amount",
            "type": "float",
        },
        {
            "name": "Training_ytdAmount",
            "alias": "training_ytd_amount",
            "type": "float",
        },
        {
            "name": "Training_hours",
            "alias": "training_hours",
            "type": "float",
        },
        {
            "name": "Training_payRate",
            "alias": "training_pay_rate",
            "type": "float",
        },
        {
            "name": "Training_preTaxIndicator",
            "alias": "training_pre_tax_indicator",
            "type": "bool",
        },
        
        # DW / Region
        {"name": "DW_ERP_System", "alias": "dw_erp_system", "type": "str"},
        {"name": "DW_Timestamp", "alias": "dw_timestamp", "type": "datetime"},
        {
            "name": "DW_ERP_Source_Table",
            "alias": "dw_erp_source_table",
            "type": "str",
        },
        {"name": "Region_Id", "alias": "region_id", "type": "int"},
        {"name": "id", "alias": "id", "type": "str"},
    ]

columns_mapping_dict = {
    "workers": {
        "key_columns": ["associateOID", "positionID", "supervisorWorkerID"],
        "columns_list": [
            {"name": "associateOID", "alias": "associate_oid", "type": "str"},
            {"name": "workerID", "alias": "worker_id", "type": "str"},
            {"name": "statusCode", "alias": "status_code", "type": "str"},
            {
                "name": "originalHireDate",
                "alias": "original_hire_date",
                "type": "date",
            },
            {
                "name": "terminationDate",
                "alias": "termination_date",
                "type": "date",
            },
            {"name": "formattedName", "alias": "formatted_name", "type": "str"},
            {"name": "familyName", "alias": "family_name", "type": "str"},
            {"name": "middleName", "alias": "middle_name", "type": "str"},
            {"name": "givenName", "alias": "given_name", "type": "str"},
            {"name": "assignmentStatus", "alias": "assignment_status", "type": "str"},
            {"name": "region", "alias": "region", "type": "str"},
            {
                "name": "assignmentStatusName",
                "alias": "assignment_status_name",
                "type": "str",
            },
            {"name": "jobCode", "alias": "job_code", "type": "str"},
            {"name": "jobTitle", "alias": "job_title", "type": "str"},
            {"name": "positionID", "alias": "position_id", "type": "str"},
            {
                "name": "supervisorAssociateOID",
                "alias": "supervisor_associate_oid",
                "type": "str",
            },
            {
                "name": "supervisorWorkerID",
                "alias": "supervisor_worker_id",
                "type": "str",
            },
            {"name": "workerTypeCode", "alias": "worker_type_code", "type": "str"},
            {"name": "homeWorkLocation", "alias": "home_work_location", "type": "str"},
            {
                "name": "serviceSupervisorAssociateOID",
                "alias": "service_supervisor_associate_oid",
                "type": "str",
            },
            {
                "name": "workerTimeProfilePositionID",
                "alias": "worker_time_profile_position_id",
                "type": "str",
            },
            {"name": "payCycleCode", "alias": "pay_cycle_code", "type": "str"},
            {"name": "payrollGroupCode", "alias": "payroll_group_code", "type": "str"},
            {"name": "businessUnitCodeValue", "alias": "business_unit_code", "type": "str"},
            {"name": "businessUnitShortName", "alias": "business_unit_name", "type": "str"},
            {"name": "departmentCodeValue", "alias": "department_code", "type": "str"},
            {"name": "departmentShortName", "alias": "department_name", "type": "str"},
            {"name": "costNumberCodeValue", "alias": "cost_number_code", "type": "str"},
            {"name": "costNumberShortName", "alias": "cost_number_name", "type": "str"},
            {"name": "workEmail", "alias": "work_email", "type": "str"},
            {"name": "DW_ERP_System", "alias": "dw_erp_system", "type": "str"},
            {"name": "DW_Timestamp", "alias": "dw_timestamp", "type": "datetime"},
            {
                "name": "DW_ERP_Source_Table",
                "alias": "dw_erp_source_table",
                "type": "str",
            },
            {"name": "Region_Id", "alias": "region_id", "type": "int"},
            {"name": "id", "alias": "id", "type": "str"},
        ],
        "additional_column_list": []
    },
    "team_time_cards": {
        "key_columns": ["associateOID", "workerID", "entryDate", 'timePeriodStartDate', 'timePeriodEndDate'],
        
        "columns_list": { "Central": central_team_time_cards_columns_list,"Southeast": southeast_team_time_cards_columns_list},
        "additional_column_list": { "Central": central_team_time_cards_additional_columns_list,"Southeast": southeast_team_time_cards_additional_columns_list}
    },
    "pay_statements": {
        "key_columns": ["associateOID", "payStatementId"],
        "columns_list": [
            {"name": "associateOID", "alias": "associate_oid", "type": "str"},
            {"name": "region", "alias": "region", "type": "str"},
            {
                "name": "payDate",
                "alias": "pay_date",
                "type": "date",
            },
            {
                "name": "netPayAmount",
                "alias": "net_pay_amount",
                "type": "float",
            },
            {
                "name": "grossPayAmount",
                "alias": "gross_pay_amount",
                "type": "float",
            },
            {
                "name": "totalHours",
                "alias": "total_hours",
                "type": "float",
            },
            {"name": "payDetailUri", "alias": "pay_detail_uri", "type": "str"},
            {"name": "payStatementId", "alias": "pay_statement_id", "type": "str"},
            {
                "name": "statementImageUri",
                "alias": "statement_image_uri",
                "type": "str",
            },
            {"name": "DW_ERP_System", "alias": "dw_erp_system", "type": "str"},
            {"name": "DW_Timestamp", "alias": "dw_timestamp", "type": "datetime"},
            {
                "name": "DW_ERP_Source_Table",
                "alias": "dw_erp_source_table",
                "type": "str",
            },
            {"name": "Region_Id", "alias": "region_id", "type": "int"},
            {"name": "id", "alias": "id", "type": "str"},
        ],
        "additional_column_list": []
    },
    "pay_statement_details": {
        "key_columns": ["associateOID", "payStatementId"],
        "columns_list": { "Central": central_pay_statement_details_columns,"Southeast": southeast_pay_statement_details_columns
            },
        "additional_column_list": { "Central": [],"Southeast": []},
    },
}
