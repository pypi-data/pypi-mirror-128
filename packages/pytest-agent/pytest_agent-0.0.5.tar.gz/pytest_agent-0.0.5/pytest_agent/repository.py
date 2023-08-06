"""
Defines repositories (class that abstract storage of objects)
"""
from datetime import datetime
from typing import Dict

import sqlalchemy

from pytest_agent.database import DBTest
from pytest_agent.drivers import Session
from pytest_agent.dtos import TestStatus, TestStatusReadDTO


# pylint: disable=no-member
class TestsRepository:
    """
    Defines how to store/retrieve tests and their output.
    """

    @staticmethod
    def update_test_status(
        fullname: str,
        status: TestStatus,
        modulename: str = None,
        classname: str = None,
        funcname: str = None,
        output: str = None,
    ):
        """
        Update test status and/or output.
        """
        with Session() as session:
            test_instance = session.query(DBTest).filter_by(fullname=fullname).first()

            if test_instance is None:
                test_instance = DBTest(
                    fullname=fullname,
                    status=status.value,
                    output=output,
                    modulename=modulename,
                    classname=classname,
                    funcname=funcname,
                )
                session.add(test_instance)

            # only status/output/refresh_date can be updated
            test_instance.status = status.value
            test_instance.output = output

            if TestStatus(test_instance.status) == TestStatus.N_A:
                test_instance.refresh_date = None
            else:
                test_instance.refresh_date = datetime.utcnow().isoformat() + "Z"

            session.commit()

    @staticmethod
    def get_statuses() -> Dict[str, TestStatusReadDTO]:
        """
        Get statuses for all tests.
        """
        with Session() as session:
            tests = session.query(DBTest).all()
            return [TestStatusReadDTO.from_orm(test) for test in tests]

    @staticmethod
    def get_output(fullname: str):
        """
        Get output of a test given its fullname.
        """
        with Session() as session:
            test_instance = session.query(DBTest).filter_by(fullname=fullname).first()
            if not test_instance:
                return None
            return test_instance.output
