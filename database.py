from sqlalchemy import create_engine, Column, Integer, String, DECIMAL, TIMESTAMP, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import psycopg2

DATABASE_URL = "postgresql://postgres:Ushabs25@localhost:5432/COAP_IOT"

# Create Database Connection
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)

Base = declarative_base()

# ✅ Define AMQP Configuration Table
class AMQPConfig(Base):
    __tablename__ = "amqp_configs"

    id = Column(Integer, primary_key=True, index=True)
    ip_address = Column(String, nullable=False)
    port = Column(Integer, nullable=False)
    connected = Column(Integer, default=0)  # ✅ Use Integer (0=False, 1=True)

# ✅ Define AMQP Log Table
class AMQPLog(Base):
    __tablename__ = "amqp_logs"

    id = Column(Integer, primary_key=True, index=True)
    ip_address = Column(String, nullable=False)
    port = Column(Integer, nullable=False)
    protocol_name = Column(String, nullable=False, default="AMQP")
    request_param = Column(String, nullable=False)
    response_value = Column(String, nullable=False)
    message = Column(String, nullable=True)  # ✅ Allow NULL values
    timestamp = Column(TIMESTAMP, server_default=func.now())

# ✅ Function to Store Data
def store_data_in_db(ip_address, request_param, response_value, message="No message provided"):
    try:
        connection = psycopg2.connect(
            dbname="COAP_IOT",
            user="postgres",
            password="Ushabs25",
            host="localhost",
            port="5432"
        )
        cursor = connection.cursor()

        query = """
        INSERT INTO amqp_logs (ip_address, port, protocol_name, request_param, response_value, message)
        VALUES (%s, %s, %s, %s, %s, %s)
        """
        values = (ip_address, None, "AMQP", request_param, response_value, message or "No message provided")

        cursor.execute(query, values)
        connection.commit()
        cursor.close()
        connection.close()

        print(f"✅ Stored in DB: {request_param} = {response_value}")

    except Exception as e:
        print(f"❌ Database Error: {e}")

