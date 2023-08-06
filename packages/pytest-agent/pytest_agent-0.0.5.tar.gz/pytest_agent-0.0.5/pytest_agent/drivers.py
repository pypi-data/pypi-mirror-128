"""
Instanciate all drivers used in applications as singletons.
"""
from concurrent.futures import ProcessPoolExecutor
from typing import Callable, ContextManager, Type

import sqlalchemy
import sqlalchemy.orm

from pytest_agent.database import DBModel
from pytest_agent.settings import MAX_WORKER_PROCESSES, SQLALCHEMY_DATABASE_URL

executor = ProcessPoolExecutor(MAX_WORKER_PROCESSES)

engine = sqlalchemy.create_engine(SQLALCHEMY_DATABASE_URL)
DBModel.metadata.create_all(engine)
session_factory = sqlalchemy.orm.sessionmaker(bind=engine)

class Session(ContextManager[sqlalchemy.orm.Session]):        
    def __enter__(self):
        self.session = sqlalchemy.orm.Session(engine)
        return self.session

    def __exit__(self, exc_type: Type[Exception], exception: Exception, traceback):
        if exception is not None:
            self.session.rollback()
        
        self.session.close()

        if exception is not None:
            raise exception
