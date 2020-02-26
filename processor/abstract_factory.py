from abc import ABC, abstractmethod
from enum import Enum
from processor.abstract_processor import AbstractProcessor


class ProcessorCreationError(Exception):
    class ErrorCode(Enum):
        cant_create_instance: 1
        parameter_missing: 2

    def __init__(self, p_error_code: ErrorCode, p_module: str = None):
        self.error_code = p_error_code

        if p_module is None:
            self.module = ""
        else:
            self.module = p_module

    @property
    def message(self) -> str:
        if self.error_code == ProcessorCreationError.ErrorCode.cant_create_instance:
            return "Can't create " + self.module + " processor instance"
        elif self.error_code == ProcessorCreationError.ErrorCode.parameter_missing:
            return "Parameters missing, can't create processor instance"
        return "Processor creation error"


class AbstractProcessorFactory(ABC):
    @abstractmethod
    def create_processor(self, p_module: str) -> AbstractProcessor:
        pass