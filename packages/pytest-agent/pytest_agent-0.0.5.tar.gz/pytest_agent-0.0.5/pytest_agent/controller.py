"""
This module is responsible to run tests on host device.
"""
import re
from typing import List

from pytest_agent.commands import execute_command
from pytest_agent.drivers import executor
from pytest_agent.dtos import TestStatus
from pytest_agent.repository import TestsRepository

TEST_PATTERN = re.compile(
    r"(?P<fullname>(?P<modulename>[\w/\.]+)(?:::(?P<classname>\w+))?::(?P<funcname>\w+))"
)


class ControllerException(Exception):
    """
    Base exception for TestsController
    """


class TestCollectException(ControllerException):
    """
    Raise when something wrong happens in TestsController.collect_and_update_tests
    """


class TestsController:
    """
    Helper class to perform tests.
    """

    @staticmethod
    def collect_and_update_tests():
        """
        Use pytest to collect tests in current directory and add these tests to test repository.
        """
        output, returncode = execute_command(
            "python -m pytest --collect-only -q", capture_stderr=False
        )
        if returncode not in (0, 5):
            raise TestCollectException("Failed to collect tests")

        for match in TEST_PATTERN.finditer(output):
            TestsRepository.update_test_status(
                status=TestStatus.N_A, **match.groupdict()
            )

    @staticmethod
    def run_test(test_fullname: str):
        """
        Run a test given its fullname, then store its output.
        """
        TestsRepository.update_test_status(
            fullname=test_fullname, status=TestStatus.RUNNING
        )
        output, returncode = execute_command(
            f"python -m pytest -v {test_fullname}", capture_stderr=True
        )
        new_status = TestStatus.SUCCEED if returncode == 0 else TestStatus.FAILED
        TestsRepository.update_test_status(
            fullname=test_fullname, status=new_status, output=output
        )

    @classmethod
    def schedule_tests(cls, test_fullnames: List[str]):
        """
        Set tests status to pending, then they are added to executor
        that will run it as soon as it will be available.
        """
        for test_fullname in test_fullnames:
            TestsRepository.update_test_status(
                fullname=test_fullname, status=TestStatus.PENDING
            )

        for test_fullname in test_fullnames:
            executor.submit(cls.run_test, test_fullname)
