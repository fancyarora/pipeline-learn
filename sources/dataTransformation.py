import pandas as pd
from sqlalchemy.orm import Session
from sqlalchemy import extract
from config import ENGINE, SPARCS_CLAIM
from models import Sparcs, Error, Visit
import pandas as pd
import datetime


def getSparcsClaim(accountType, hospital):
    for fileType, accountTypes in SPARCS_CLAIM.get(hospital).items():
        if accountType in accountTypes:
            return fileType


def getSparcsSummary(visitDf, sparcsDf, errorDf, hospital='public'):
    sparcsDetailDF = visitDf.merge(sparcsDf, how='left', on='account_number').merge(errorDf, how='left', on='account_number')
    sparcsDetailDF['sparcs_claim'] = sparcsDetailDF['account_type'].apply(getSparcsClaim, args=(hospital,)).fillna('#N/A')
    sparcsDetailDF['disposition'] = sparcsDetailDF['disposition'].fillna('Not Submitted')
    return sparcsDetailDF


def getMonthlySparscSummary(sparcsDetailDF, currMonth, hospital='public'):
    sparcsDetailDF['discharge_date'] = pd.to_datetime(sparcsDetailDF['discharge_date'])
    sparcsDetailDF['month'] = sparcsDetailDF['discharge_date'].dt.to_period('m')
    sparcsCurrMonthDf = sparcsDetailDF[sparcsDetailDF['discharge_date'].dt.month == currMonth]
    sparcsCurrMonthSummary = pd.pivot_table(sparcsCurrMonthDf, values='account_number', columns = ['month'], index = ['disposition', 'sparcs_claim'], \
        aggfunc=lambda x: len(x.unique()), margins=True, margins_name='Grand Total')
    sparcsCurrMonthSummary = sparcsCurrMonthSummary.rename(columns=lambda x: x.strftime('%b %Y') if not isinstance(x,str) else x)
    return sparcsCurrMonthSummary


def getYearlySparscSummary(sparcsDetailDF, hospital='public'):
    sparcsDetailDF['discharge_date'] = pd.to_datetime(sparcsDetailDF['discharge_date'])
    sparcsDetailDF['month'] = sparcsDetailDF['discharge_date'].dt.to_period('m')
    sparcsCurrYearSummary = pd.pivot_table(sparcsDetailDF, values='account_number', columns = ['month'], index = ['disposition', 'sparcs_claim'], \
        aggfunc=lambda x: len(x.unique()), margins=True, margins_name='Grand Total')
    sparcsCurrYearSummary = sparcsCurrYearSummary.rename(columns=lambda x: x.strftime('%b %Y') if not isinstance(x,str) else x)
    return sparcsCurrYearSummary


def getMonthlySparscRejections(visitDf, errorDf, currMonth, hospital='public'):
    sparcsErrorDF = visitDf.merge(errorDf, how='inner', on='account_number')
    sparcsErrorDF['discharge_date'] = pd.to_datetime(sparcsErrorDF['discharge_date'])
    sparcsErrorDF = sparcsErrorDF[sparcsErrorDF['discharge_date'].dt.month == currMonth]
    if not sparcsErrorDF.empty:
        sparcsErrorSummary = pd.pivot_table(sparcsErrorDF, values='account_number', index = ['error_text', 'error_code'], 
                                        aggfunc=lambda x: len(x.unique()), margins=True, margins_name='Grand Total').reset_index()
        return sparcsErrorSummary
    else:
        sparcsErrorDF = sparcsErrorDF[(col for col in Error.__table__.columns.keys() if col != 'filename')]
        return sparcsErrorDF



def getIndSparscStatus(sparcsDetailDF, hospital='public'):
    sparcsStatusDfs = {}
    sparcsStatusList = sparcsDetailDF['disposition'].unique()
    for sparcsStatus in sparcsStatusList:
        df = sparcsDetailDF[sparcsDetailDF['disposition']==sparcsStatus]
        sparcsStatusDfs[sparcsStatus] = df
    return sparcsStatusDfs


def retrieveVisitDataFromDb(schema="public", year=None):
    '''Get entries from visit table belonging to the specified year'''
    schema_engine = ENGINE.execution_options(schema_translate_map = {"per_user": schema})
    with Session(schema_engine) as session:
        if year:
            visitQueryObj = session.query(Visit).filter(extract('year', Visit.discharge_date)==year)
        else:
            visitQueryObj = session.query(Visit)
        visitDf = pd.read_sql(visitQueryObj.statement, session.bind)
    return visitDf


def retrieveSparcsDataFromDb(schema="public", account_numbers=None):
    '''Get entries from spacrs table for the specified account numbers'''
    schema_engine = ENGINE.execution_options(schema_translate_map = {"per_user": schema})
    with Session(schema_engine) as session:
        if account_numbers:
            sparcsQueryObj = session.query(Sparcs).filter(Sparcs.account_number.in_(account_numbers))
        else:
            sparcsQueryObj = session.query(Sparcs)
        sparcsDf = pd.read_sql(sparcsQueryObj.statement, session.bind)
    return sparcsDf


def retrieveErrorDataFromDb(schema="public", account_numbers=None):
    '''Get entries from error table for the specified account numbers'''
    schema_engine = ENGINE.execution_options(schema_translate_map = {"per_user": schema})
    with Session(schema_engine) as session:
        if account_numbers:
            errorQueryObj = session.query(Error).filter(Error.account_number.in_(account_numbers))
        else:
            errorQueryObj = session.query(Error)
        errorDf = pd.read_sql(errorQueryObj.statement, session.bind)
    return errorDf


def run(hospital='public'):
    inpMonth = datetime.date.today().month - 3 # Data will available for dates prior to 60 days
    currYear = datetime.date.today().year
    
    visitDf = retrieveVisitDataFromDb(schema=hospital, year=currYear)

    sparcsDf = retrieveSparcsDataFromDb(schema=hospital, account_numbers=list(visitDf['account_number'].unique()))
    sparcsDf = sparcsDf.drop(columns='filename')
    
    errorDf = retrieveErrorDataFromDb(schema=hospital, account_numbers=list(visitDf['account_number'].unique()))
    errorDf = errorDf.drop(columns='filename')
    
    sparcsDetailDF = getSparcsSummary(visitDf, sparcsDf, errorDf, hospital=hospital)
    sparcsErrorSummary = getMonthlySparscRejections(visitDf, errorDf, inpMonth, hospital=hospital)
    sparcsStatusDfs = getIndSparscStatus(sparcsDetailDF, hospital=hospital)

    sparcsCurrMonthSummary = getMonthlySparscSummary(sparcsDetailDF.copy(deep=True), inpMonth, hospital=hospital)
    sparcsCurrYearSummary = getYearlySparscSummary(sparcsDetailDF.copy(deep=True), hospital=hospital)

    return sparcsDetailDF, sparcsCurrMonthSummary, sparcsErrorSummary, sparcsStatusDfs, sparcsCurrYearSummary