import dramatiq
from random import randint
from time import sleep

from dramatiq.brokers.redis import RedisBroker
from dramatiq.results import Results
from dramatiq.results.backends import RedisBackend


broker = RedisBroker(host="redis")
dramatiq.set_broker(broker)

backend = RedisBackend(host="redis")
broker.add_middleware(Results(backend=backend))


@dramatiq.actor(store_results=True)
def heavy_calc(num: float):
    sleep(randint(5,50))
    return num*2
