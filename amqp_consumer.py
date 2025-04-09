import pika
import json
import random
import time
from database import store_data_in_db

RABBITMQ_HOST = 'localhost'
QUEUE_NAME = 'sensor_data_queue'

def generate_sensor_data(sensor_type):
    """Simulate continuous sensor readings."""
    data = {
        "temperature": round(random.uniform(20, 35), 2),
        "humidity": round(random.uniform(40, 80), 2),
        "pressure": round(random.uniform(950, 1050), 2)
    }
    return data.get(sensor_type, "Invalid Parameter")

def callback(ch, method, properties, body):
    try:
        if not body:
            print("❌ Received an empty message!")
            return

        request = json.loads(body.decode())

        if not isinstance(request, dict):
            print(f"❌ Invalid message format: {body}")
            return

        sensor_type = request.get("sensor_type", "unknown")

        if sensor_type not in ["temperature", "humidity", "pressure"]:
            print(f"⚠️ Unknown sensor type received: {sensor_type}")
            return

        # ✅ Generate random sensor value
        response_value = generate_sensor_data(sensor_type)
        print(f"📥 Received: {sensor_type} → Responding with: {response_value}")

        # ✅ Store in PostgreSQL ONLY if FastAPI requests it
        if properties.correlation_id == "fastapi_request":
            store_data_in_db("192.168.1.100", sensor_type, response_value)
            print(f"✅ Stored in DB: {sensor_type} = {response_value}")

    except json.JSONDecodeError as e:
        print(f"❌ JSON Decode Error: {e}")
        print(f"🚨 Raw message received: {body}")

# ✅ RabbitMQ Setup
connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBITMQ_HOST))
channel = connection.channel()
channel.queue_declare(queue=QUEUE_NAME)

# ✅ Start Consumer
channel.basic_consume(queue=QUEUE_NAME, on_message_callback=callback, auto_ack=True)

print("🚀 AMQP Consumer Running...")
channel.start_consuming()
