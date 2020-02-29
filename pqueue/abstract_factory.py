from abc import ABC, abstractmethod
from client.log import Log
from database.abstract_database import AbstractDatabase
from enum import Enum
from pqueue.abstract_queue import AbstractQueue


class QueueCreationError(Exception):
    class ErrorCode(Enum):
        cant_create_instance: 1
        parameter_missing: 2

    def __init__(self,
                 p_error_code: ErrorCode,
                 p_module: str = ""):

        self.error_code = p_error_code

        if p_module is None:
            self.module = ""
        else:
            self.module = p_module

    @property
    def message(self) -> str:
        if self.error_code == QueueCreationError.ErrorCode.cant_create_instance:
            return "Can't create " + self.module + " queue instance"
        elif self.error_code == QueueCreationError.ErrorCode.parameter_missing:
            return "Parameters missing, can't create database instance"
        return "Database creation error"


class AbstractQueueFactory:
    @abstractmethod
    def create_queue(self, p_module: str, p_database: AbstractDatabase, p_log: Log) -> AbstractQueue:
        pass
