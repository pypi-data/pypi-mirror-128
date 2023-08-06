import logging
import time
from typing import Callable, NamedTuple, Union

import paho.mqtt.client as mqtt

'''
    pip install paho-mqtt
'''

class MQTTConfig(NamedTuple):
    HOST: str
    TPPIC: str
    PORT: int = 1883    #使用SSL/TLS的默认端口是 8883
    USER: str = None
    PSW: str = None
    CLIENT_ID: str = ''
    KEEP_ALIVE: int = 60

class MQTTAccessor:

    def __init__(self, config: MQTTConfig):
        self.config = config
        self.call_back = None

    def on_connect(self, client, userdata, flags, rc):
        pass

    def on_message(self, client, userdata, message):
        if self.call_back is not None:
            self.call_back(message.topic, message.payload)

    def on_subscribe(self, client, userdata, mid, granted_qos):
        pass    #("On Subscribed: qos = %d" % granted_qos)

    def on_disconnect(self, client, userdata, rc):
        pass

    def _get_mqtt_client(self):
        if self.config.CLIENT_ID is None or len(self.config.CLIENT_ID) == 0:
            client = mqtt.Client(client_id='', clean_session = True)
        else:
            client = mqtt.Client(self.config.CLIENT_ID)
        if self.config.USER is not None and self.config.PSW is not None:
            client.username_pw_set(self.config.USER, self.config.PSW)
        client.on_connect = self.on_connect
        client.on_message = self.on_message
        client.on_subscribe = self.on_subscribe
        client.on_disconnect = self.on_disconnect
        client.connect(self.config.HOST, self.config.PORT, self.config.KEEP_ALIVE)
        return client

    def publish_topic(self, topic: str, message: str, qos: int = 0):
        client = self._get_mqtt_client()
        client.publish(topic, payload=message, qos=qos)
        client.disconnect()

    def subscribe_topics(self, topics: Union[str, list], qos: int = 0, retry_interval: int=10, callback: Callable = None):
        self.call_back = callback
        while True:
            try:
                client = self._get_mqtt_client()
                client.subscribe(topics, qos=qos)
                client.loop_forever()
                client.disconnect()
            except Exception:
                logging.error(f'topics={topics} exception', exc_info=True)
            time.sleep(retry_interval)
