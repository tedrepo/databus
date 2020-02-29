from abc import ABC, abstractmethod
from client.log import Log
from pqueue.queue_status import PassengerQueueStatus


class AbstractPusher(ABC):
    def __init__(self, p_log: Log = None):
        self.log = p_log

    @abstractmethod
    def push(self, p_passenger: PassengerQueueStatus):
        pass
