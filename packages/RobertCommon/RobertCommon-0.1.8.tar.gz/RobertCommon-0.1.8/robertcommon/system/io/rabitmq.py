import logging
import time
from typing import Callable, NamedTuple

import pika


class StopConsume(Exception):
    pass


class RabbitMQConfig(NamedTuple):
    HOST: str
    PORT: int
    USER: str
    PASSWORD: str
    VIR_HOST: str = ''


class RabbitMQAccessor:

    def __init__(self, config: RabbitMQConfig):
        self.config = config

    def _get_blocking_connection(self):
        credentials = pika.PlainCredentials(self.config.USER, self.config.PASSWORD)
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(host=self.config.HOST,
                                      port=self.config.PORT,
                                      virtual_host=self.config.VIR_HOST,
                                      credentials=credentials))
        return connection

    def send_exchange(self, exchange: str, routing_key: str, message: str):
        connection = self._get_blocking_connection()
        channel = connection.channel()
        channel.exchange_declare(exchange=str(exchange), exchange_type='topic')
        channel.basic_publish(exchange=str(exchange), routing_key=str(routing_key), body=str(message),
                                  properties=pika.BasicProperties(delivery_mode=2, ))
        channel.close()
        connection.close()

    def send_queue(self, queue_name: str, message: str, exchange: str=''):
        connection = self._get_blocking_connection()
        channel = connection.channel()
        channel.queue_declare(queue=queue_name, durable=True)
        channel.basic_publish(exchange=str(exchange), routing_key=queue_name, body=str(message),
                              properties=pika.BasicProperties(delivery_mode=2, ))
        channel.close()
        connection.close()

    def consume_exchange(self, exchange: str, exchange_type: str = 'topic', routing_key: str = '#',
                         retry_interval: int = 10, callback: Callable = None):

        def real_callback(channel, method, properties, body):
            channel.basic_ack(delivery_tag=method.delivery_tag)
            if callback is not None:
                callback(body)

        while True:
            try:
                connection = self._get_blocking_connection()
                channel = connection.channel()
                channel.exchange_declare(exchange=exchange, exchange_type=exchange_type)  # 声明一个Exchange
                channel.queue_declare(queue=exchange, exclusive=True)  # 声明一个队里
                channel.queue_bind(exchange=exchange, queue=exchange, routing_key=routing_key)  # 绑定一个队列
                channel.basic_consume(exchange, real_callback)
                channel.start_consuming()
            except StopConsume:
                logging.info(f'exchange={exchange} stop consume')
                return
            except Exception:
                logging.error(f'exchange={exchange} exception', exc_info=True)
            time.sleep(retry_interval)

    def consume_queue(self, queue_name: str, retry_interval: int = 10, callback: Callable = None):

        def real_callback(channel, method, properties, body):
            channel.basic_ack(delivery_tag=method.delivery_tag)
            if callback is not None:
                callback(body)

        while True:
            try:
                connection = self._get_blocking_connection()
                channel = connection.channel()
                channel.queue_declare(queue=queue_name, durable=True)
                channel.basic_qos(prefetch_count=1)
                channel.basic_consume(queue=queue_name, on_message_callback=real_callback)
                channel.start_consuming()
            except StopConsume:
                logging.info(f'queue_name={queue_name} stop consume')
                return
            except Exception:
                logging.error(f'queue_name={queue_name} exception', exc_info=True)
            time.sleep(retry_interval)
