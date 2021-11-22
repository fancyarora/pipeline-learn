HTML_FILE_DIR = 'C:\\Users\\fancy\\OneDrive\\Documents\\Pipeline learn\\Prism files\\{hospital}\\Html Files\\'
ERROR_FILE_DIR = 'C:\\Users\\fancy\\OneDrive\\Documents\\Pipeline learn\\Prism files\\{hospital}\\Error Files\\'
VISIT_FILE_DIR = 'C:\\Users\\fancy\\OneDrive\\Documents\\Pipeline learn\\Prism files\\{hospital}\\Visits\\'
END_RESULT_FILE_DIR = 'C:\\Users\\fancy\\OneDrive\\Documents\\Pipeline learn\\Prism files\\{hospital}\\End Result Files\\'

VISIT_COLUMNS = {
    'interfaith' : ['AccountNumber', 'Admit/ServiceDt', 'Discharge/ServiceDt', 'PrimaryInsuranceDesc', 'AccountType', 'BarStatus'],
    'wyckoff'    : ['Account Num', 'Admit DT', 'Discharge DT', 'Pri Ins', 'Acct Type'],
    'test'       : ['AccountNumber', 'Admit/ServiceDt', 'Discharge/ServiceDt', 'PrimaryInsuranceDesc', 'AccountType', 'BarStatus'],
}

SPARCS_CLAIM = {
    'interfaith':{
        'IP' : ['I DETOX', 'I INP', 'I PSY', 'I REHAB'], # Inpatient
        'ER' : ['O ER',], # Emergency Dept
        'AS' : ['O AS',], # Ambulatory Surgery
        'OP' : ['O CDOS', 'O CLINIC', 'O DEN', 'O MMTP', 'O PC', 'O PSY', 'O REC', 'O REFAMB', 'O TELE'], # Outpatient
    },
    'wyckoff':{
        'IP' : ['Inpatient',], # Inpatient
        'ER' : ['Emergency',], # Emergency Dept
        'AS' : ['Same Day Surgery',], # Ambulatory Surgery
        'OP' : ['Clinic', 'Observation', 'Referred'], # Outpatient
    }
}