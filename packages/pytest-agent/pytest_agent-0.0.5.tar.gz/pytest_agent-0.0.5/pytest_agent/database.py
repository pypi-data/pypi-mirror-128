"""
Defines database tables schemas.
"""
from sqlalchemy import Column, String, Text
from sqlalchemy.ext.declarative import declarative_base

DBModel = declarative_base()

# pylint: disable=too-few-public-methods
class DBTest(DBModel):
    """
    Define test table schema.
    """

    __tablename__ = "tests"

    fullname = Column(String, primary_key=True)
    modulename = Column(String, nullable=False)
    classname = Column(String, nullable=True)
    funcname = Column(String, nullable=False)

    status = Column(String, nullable=False)
    refresh_date = Column(String, nullable=True)
    output = Column(Text, nullable=True)
