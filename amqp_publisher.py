import pika
import json
import random
import time

RABBITMQ_HOST = 'localhost'
QUEUE_NAME = 'sensor_data_queue'

def send_request(sensor_type, correlation_id=None):
    """Send sensor request to RabbitMQ."""
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBITMQ_HOST))
    channel = connection.channel()
    channel.queue_declare(queue=QUEUE_NAME)

    message = json.dumps({"sensor_type": sensor_type})
    properties = pika.BasicProperties(correlation_id=correlation_id) if correlation_id else None
    channel.basic_publish(exchange='', routing_key=QUEUE_NAME, body=message, properties=properties)

    print(f"✅ Successfully Sent: {message}")
    connection.close()

# **Continuously send requests**
if __name__ == "__main__":
    while True:
        for sensor in ["temperature", "humidity", "pressure"]:
            send_request(sensor)
        time.sleep(2)  # Send every 2 seconds
