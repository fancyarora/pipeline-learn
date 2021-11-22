import datetime
import pandas as pd
from config import END_RESULT_FILE_DIR


def run(sparcsDetailDF, sparcsCurrMonthSummary, sparcsErrorSummary, sparcsStatusDfs, sparcsCurrYearSummary, hospital='interfaith'):
    filePath = END_RESULT_FILE_DIR.format(hospital=hospital)
    with pd.ExcelWriter(filePath + "Sparcs Summary_" + datetime.date.today().strftime('%m%d%Y') + ".xlsx") as writer:
        sparcsDetailDF.to_excel(writer, sheet_name='Sparcs Detail Summary', index=False)
        sparcsCurrMonthSummary.to_excel(writer, sheet_name='Sparcs ' + datetime.date.today().strftime('%b %Y') + ' Summary')
        sparcsCurrYearSummary.to_excel(writer, sheet_name='Sparcs ' + datetime.date.today().strftime('%Y') + ' Summary')
    
    with pd.ExcelWriter(filePath + "SPARCS Rejection Summary_" + datetime.date.today().strftime('%m%d%Y') + ".xlsx") as writer:
        sparcsErrorSummary.to_excel(writer, sheet_name='Monthly Rejection Summary', index=False)
        for sparcsStatus in sparcsStatusDfs:
            if sparcsStatus == 'Rejected':
                sparcsStatusDfs[sparcsStatus].to_excel(writer, sheet_name='Detailed Rejection Summary', index=False)
            else:
                sparcsStatusDfs[sparcsStatus].to_excel(filePath + "SPARCS " + sparcsStatus + " Summary_" + datetime.date.today().strftime("%m%d%Y") + ".xlsx", index=False)
