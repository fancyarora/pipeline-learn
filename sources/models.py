from sqlalchemy import Column, Float, String, Date
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class Sparcs(Base):
    __tablename__ = 'sparcs'
    __table_args__ = {'schema': 'per_user'}

    account_number = Column(String, primary_key=True)
    patient_name = Column(String, nullable=False)
    statement_dates = Column(String, nullable=False)
    amount = Column(Float, nullable=False)
    disposition = Column(String, nullable=False)
    filename = Column(String, nullable=False)

    def __repr__(self):
       return f"({self.account_number!r}, {self.patient_name!r}, {self.statement_dates!r}, {self.amount!r}, {self.disposition!r}, {self.filename!r})"


class Error(Base):
    __tablename__ = 'error'
    __table_args__ = {'schema': 'per_user'}

    account_number = Column(String, primary_key=True)
    error_code = Column(String, nullable=False)
    error_text = Column(String(100), nullable=False)
    filename = Column(String, nullable=False)

    def __repr__(self):
       return f"({self.account_number!r}, {self.error_code!r}, {self.error_text!r}, {self.filename!r})"


class Visit(Base):
    __tablename__ = 'visit'
    __table_args__ = {'schema': 'per_user'}

    account_number = Column(String, primary_key=True)
    admit_date = Column(Date, nullable=False)
    discharge_date = Column(Date, nullable=False)
    primary_insurance = Column(String, nullable=False)
    account_type = Column(String, nullable=False)
    bar_status = Column(String, nullable=False)

    def __repr__(self):
       return f"({self.account_number!r}, {self.admit_date!r}, {self.discharge_date!r}, {self.primary_insurance!r}, {self.account_type!r}, {self.bar_status!r})"