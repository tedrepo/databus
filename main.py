from database.primal_factory import PrimalDatabaseFactory
from dispatcher.abstract_factory import DispatcherTicket
from dispatcher.primal_factory import PrimalDispatcherFactory
from driver.primal_factory import PrimalDriverFactory
from passenger.primal_factory import PrimalPassengerFactory
from pqueue.primal_factory import PrimalQueueFactory
from puller.primal_factory import PrimalPullerFactory
from pusher.primal_factory import PrimalPusherFactory
from processor.primal_factory import PrimalProcessorFactory

# todo: final
# readme gözden geçir, hatalı klasör veya eksik bilgi vs kalmasın
# dışarıdan databus'e gelen bir programcı, kendi client'ını DB'sini filan verebiliyor mu? ID değil de nesne? bunu örnek bir dış proje ile dene
# ayrı bir external proje açıp (pip vs) test et


_DEFAULT_DATABASE = "database.json_db.json_database"
_DEFAULT_DRIVER = "driver.primal_driver"
_DEFAULT_DISPATCHER = "dispatcher.primal_dispatcher"

_dispatcher_ticket = DispatcherTicket(
    p_database_factory=PrimalDatabaseFactory(),
    p_driver_factory=PrimalDriverFactory(),
    p_passenger_factory=PrimalPassengerFactory(),
    p_queue_factory=PrimalQueueFactory(),
    p_puller_factory=PrimalPullerFactory(),
    p_processor_factory=PrimalProcessorFactory(),
    p_pusher_factory=PrimalPusherFactory(),
    p_database_module=_DEFAULT_DATABASE,
    p_driver_module=_DEFAULT_DRIVER)

PrimalDispatcherFactory().create_dispatcher(
    p_module=_DEFAULT_DISPATCHER,
    p_ticket=_dispatcher_ticket).start()




