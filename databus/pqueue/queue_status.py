from databus.client.client_passenger import ClientPassenger
from enum import Enum
from databus.passenger.abstract_passenger import AbstractPassenger
from typing import List


class QueueStatus(Enum):
    undefined = 0
    incomplete = 1
    complete = 2


class ProcessorQueueStatus:
    def __init__(self, p_processor_module: str, p_status: QueueStatus = QueueStatus.undefined):
        self.processor_module = p_processor_module
        self.status = p_status


class PusherQueueStatus:
    def __init__(self, p_pusher_module: str, p_status: QueueStatus = QueueStatus.undefined):
        self.pusher_module = p_pusher_module
        self.status = p_status


class PassengerQueueStatus:
    def __init__(self,
                 p_passenger: AbstractPassenger,
                 p_pusher_statuses: List[PusherQueueStatus] = None,
                 p_processor_statuses: List[ProcessorQueueStatus] = None,
                 p_puller_notified: bool = False):

        self.passenger = p_passenger

        if p_pusher_statuses is None:
            self.pusher_statuses = []
        else:
            self.pusher_statuses = p_pusher_statuses

        if p_processor_statuses is None:
            self.processor_statuses = []
        else:
            self.processor_statuses = p_processor_statuses

        self.puller_notified = p_puller_notified

    @property
    def all_processors_complete(self) -> bool:
        for processor_status in self.processor_statuses:
            if processor_status.status != QueueStatus.complete:
                return False
        return True

    @property
    def all_pushers_complete(self) -> bool:
        for pusher_status in self.pusher_statuses:
            if pusher_status.status != QueueStatus.complete:
                return False
        return True

    def set_all_processor_statuses(self, p_status: QueueStatus):
        for processor_status in self.processor_statuses:
            processor_status.status = p_status

    def set_all_pusher_statuses(self, p_status: QueueStatus):
        for pusher_status in self.pusher_statuses:
            pusher_status.status = p_status

    def set_processor_status(self, p_processor_module: str, p_status: QueueStatus):
        for processor_status in self.processor_statuses:
            if processor_status.processor_module == p_processor_module:
                processor_status.status = p_status

    def set_pusher_status(self, p_pusher_module: str, p_status: QueueStatus):
        for pusher_status in self.pusher_statuses:
            if pusher_status.pusher_module == p_pusher_module:
                pusher_status.status = p_status


class QueueStatusFactory:
    @staticmethod
    def get_passenger_queue_status(p_passenger: AbstractPassenger,
                                   p_client_passenger: ClientPassenger
                                   ) -> PassengerQueueStatus:
        output = PassengerQueueStatus(p_passenger)
        for processor_module in p_client_passenger.processor_modules:
            output.processor_statuses.append(ProcessorQueueStatus(processor_module, QueueStatus.incomplete))
        for pusher_module in p_client_passenger.pusher_modules:
            output.pusher_statuses.append(PusherQueueStatus(pusher_module, QueueStatus.incomplete))
        return output


class QueueStatusError(Exception):
    class ErrorCode(Enum):
        module_missing = 1

    def __init__(self,
                 p_error_code: ErrorCode,
                 p_queue_status_type: str,
                 p_passenger_id: str):
        self.error_code = p_error_code
        self.queue_status_type = p_queue_status_type
        self.passenger_id = p_passenger_id

    @property
    def message(self) -> str:
        if self.error_code == QueueStatusError.ErrorCode.module_missing:
            return "Passenger " + self.passenger_id + " is missing " + self.queue_status_type + " module"
        return "Passenger error"


class Validator:
    @staticmethod
    def validate_queue_module(p_queue_status_type: str,
                              p_passenger_id: str,
                              p_module: str):

        if p_module is None or p_module == "":
            raise QueueStatusError(p_passenger_id=p_passenger_id,
                                   p_error_code=QueueStatusError.ErrorCode.module_missing,
                                   p_queue_status_type=p_queue_status_type)
