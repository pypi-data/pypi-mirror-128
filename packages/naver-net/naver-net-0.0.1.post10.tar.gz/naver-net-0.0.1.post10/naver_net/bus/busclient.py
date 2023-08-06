#!/usr/bin/env python
import pika 


class BusClient():
    def __init__(self, config):
        self.config = config
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host=config.core.getVariable("rabitserver")))
        self.channel = self.connection.channel()
        self.buffer = [] 

    def send(self, msg, queue):
        self.channel.queue_declare(queue=queue)
        self.channel.basic_publish(
            exchange='', routing_key=queue, body=msg)
        self.connection.close()

    def receive(self, queue):
        self.channel.queue_declare(queue=queue)

        def callback(ch, method, properties, body):
            self.buffer.append({ch, method, properties, body})
        self.channel.basic_consume(
            queue=queue, on_message_callback=callback, auto_ack=True)
        self.channel.start_consuming()

    def checkBuffer(self):
        if len(self.buffer) > 0:
            res = self.buffer[0]
            self.buffer.pop(0)
            return res
