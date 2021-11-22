import os
import traceback
import pandas as pd
from models import Sparcs, Error, Visit
from config import HTML_FILE_DIR, ERROR_FILE_DIR, VISIT_FILE_DIR, VISIT_COLUMNS


def parseRecordsFromHtmlFile(filePath, fileName):
    dfs = pd.read_html(filePath + fileName, header = 0)
    for df in dfs:
        if df.columns.to_list() == ['Unit #', 'Patient Account Number', 'Patient Name', 'Statement Dates', 'Amount', 'Disposition']:
            df = df.dropna().drop(columns='Unit #')
            df['fileName'] = fileName
            df.columns = Sparcs.__table__.columns.keys()
            df.amount = pd.to_numeric(df.amount.str.replace('$', '').str.replace(',',''))
            print("Successfully Parsed: {}".format(fileName))
            return df.to_dict('r')


def parseRecordsFromErrorFile(filePath, fileName):
    df = pd.read_csv(filePath + fileName, header = 0)
    df = df[['Patient Account Number', 'Error or Message Code', 'Error or Message Text']]
    df['fileName'] = fileName
    df.columns = Error.__table__.columns.keys()
    df['error_text'] = df['error_text'].str[:100]
    print("Successfully Parsed: {}".format(fileName))
    return df.to_dict('r')


def parseRecordsFromVisitFile(filePath, fileName, hospital="interfaith"):
    sep = ',' if fileName.endswith('.csv') else '\t'
    df = pd.read_csv(filePath + fileName, header = 0, sep=sep)
    visitColumns = VISIT_COLUMNS.get(hospital.lower())
    df = df[visitColumns]
    if 'BarStatus' not in df.columns:
        df['BarStatus'] = ''
    df.columns = Visit.__table__.columns.keys()
    df = df[df['discharge_date'].notna()]
    print("Successfully Parsed: {}".format(fileName))
    return df.to_dict('r')


def retrieveDatafromHtmlFiles(schema="public"):
    """Retrieve data from html files from "Html Files" directory, containing Patient Account Number and Disposition Status"""

    filePath = HTML_FILE_DIR.format(hospital=schema)
    for root, _, files in os.walk(filePath):
        if not ('Processed' in root or 'Errored' in root):
            for fileName in files:
                print("Retreiving data from file: {}".format(fileName))
                try:
                    records = parseRecordsFromHtmlFile(filePath, fileName)
                    if records:
                        print(filePath)
                        print(fileName)
                        os.rename(filePath + fileName, filePath + "Processed/" + fileName)
                        return True
                except Exception as e:
                    print("Parsing Failed for {}".format(fileName))
                    print(e)
                    print(traceback.print_exc())
                    os.rename(filePath + fileName, filePath + "Errored/" + fileName)
                    return False


def retrieveDatafromErrorFiles(schema="public"):
    """Retrieve data from csv files from "Error Files" directory, containing rejected Patient Account Number and the rejected reason"""

    filePath = ERROR_FILE_DIR.format(hospital=schema)
    for root, _, files in os.walk(filePath):
        if not ('Processed' in root or 'Errored' in root):
            for fileName in files:
                print("Retreiving data from file: {}".format(fileName))
                try:
                    records = parseRecordsFromErrorFile(filePath, fileName)
                    if records:
                        os.rename(filePath + fileName, filePath + "Processed/" + fileName)
                        return True
                except Exception as e:
                    print("Parsing Failed for {}".format(fileName))
                    print(e)
                    print(traceback.print_exc())
                    os.rename(filePath + fileName, filePath + "Errored/" + fileName)
                    return False


def retrieveDatafromVisitFiles(schema="public"):
    """Retrieve data from visit files from "Visits" directory, containing Patient Account Number of all people who visited the hospital"""

    filePath = VISIT_FILE_DIR.format(hospital=schema)
    for root, _, files in os.walk(filePath):
        if not ('Processed' in root or 'Errored' in root):
            for fileName in files:
                print("Retreiving data from file: {}".format(fileName))
                try:
                    records = parseRecordsFromVisitFile(filePath, fileName, hospital=schema)
                    if records:
                        os.rename(filePath + fileName, filePath + "Processed/" + fileName)
                        return True
                except Exception as e:
                    print("Parsing Failed for {}".format(fileName))
                    print(e)
                    print(traceback.print_exc())
                    os.rename(filePath + fileName, filePath + "Errored/" + fileName)
                    return False


def run(hospital="interfaith"):
    retrieveDatafromHtmlFiles(schema=hospital)
    retrieveDatafromErrorFiles(schema=hospital)
    retrieveDatafromVisitFiles(schema=hospital)