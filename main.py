from fastapi import FastAPI, HTTPException, Query, Depends,Request
import pika
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String, TIMESTAMP, DECIMAL, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from datetime import datetime
import socket
import random  # ✅ Import random module

app = FastAPI()

# ✅ PostgreSQL Database Configuration
DATABASE_URL = "postgresql://postgres:Ushabs25@localhost:5432/COAP_IOT"
engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# ✅ Define Database Tables
Base = declarative_base()

class AMQPConfig(Base):
    __tablename__ = "amqp_configs"
    id = Column(Integer, primary_key=True, index=True)
    ip_address = Column(String, nullable=False)
    port = Column(Integer, nullable=False)
    connected = Column(Integer, default=0)

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

# ✅ Create Tables if Not Exists
Base.metadata.create_all(bind=engine)

# ✅ Database Dependency
def get_db():
    db = None
    try:
        db = SessionLocal()
        yield db
    finally:
        if db:
            db.close()

# ✅ Set AMQP Configuration
@app.post("/amqp_set_config/")
async def amqp_set_config(ip_address: str, port: int, db: Session = Depends(get_db)):
    new_config = AMQPConfig(ip_address=ip_address, port=port, connected=0)
    db.add(new_config)
    db.commit()
    db.refresh(new_config)
    return {"status": "success", "message": "AMQP config stored successfully", "config_id": new_config.id}

# ✅ Update AMQP Configuration
@app.put("/amqp_update_config/{config_id}/")
async def amqp_update_config(config_id: int, ip_address: str = None, port: int = None, connected: int = None, db: Session = Depends(get_db)):
    config = db.query(AMQPConfig).filter(AMQPConfig.id == config_id).first()
    if not config:
        raise HTTPException(status_code=404, detail="Configuration not found!")
    if ip_address:
        config.ip_address = ip_address
    if port:
        config.port = port
    if connected is not None:
        config.connected = connected
    db.commit()
    db.refresh(config)
    return {"status": "success", "message": "Configuration updated!", "config": config}

# ✅ Connect to AMQP Server
@app.post("/amqp_connect/")
async def amqp_connect(config_id: int, db: Session = Depends(get_db)):
    config = db.query(AMQPConfig).filter(AMQPConfig.id == config_id).first()
    if not config:
        raise HTTPException(status_code=404, detail="Configuration not found!")
    try:
        with socket.create_connection((config.ip_address, config.port), timeout=2):
            config.connected = 1
            db.commit()
            return {"status": "success", "message": "Connected to AMQP server!"}
    except Exception:
        raise HTTPException(status_code=500, detail="AMQP Server is unreachable!")

# ✅ Publish Message to AMQP Queue
@app.post("/amqp_publish/")
async def amqp_publish(
    config_id: int = Query(..., description="Enter the config_id of the active AMQP connection"),
    sensor_type: str = Query(..., description="Enter 'temperature', 'pressure', or 'humidity'"),
    db: Session = Depends(get_db)
):
    try:
        # ✅ Validate if the config_id exists and is connected
        config = db.query(AMQPConfig).filter(AMQPConfig.id == config_id, AMQPConfig.connected == 1).first()
        if not config:
            raise HTTPException(status_code=400, detail="Invalid config_id or AMQP server not connected!")

        # ✅ Validate input sensor type
        valid_sensors = ["temperature", "pressure", "humidity"]
        if sensor_type not in valid_sensors:
            raise HTTPException(status_code=400, detail=f"Invalid sensor type. Use one of {valid_sensors}.")

        # ✅ Generate random sensor values
        sensor_values = {
            "temperature": round(random.uniform(20.0, 40.0), 2),
            "pressure": round(random.uniform(900.0, 1100.0), 2),
            "humidity": round(random.uniform(30.0, 90.0), 2)
        }

        response_value = sensor_values[sensor_type]

        # ✅ Insert into PostgreSQL with the same config_id
        new_log = AMQPLog(
            ip_address=config.ip_address,  # ✅ Use the connected IP
            port=config.port,  # ✅ Use the connected port
            protocol_name="AMQP",
            request_param=sensor_type,
            response_value=str(response_value),
            message=f"Sensor data from config {config_id}: {sensor_type}={response_value}"  # ✅ Store reference to config_id
        )
        db.add(new_log)
        db.commit()
        db.refresh(new_log)

        return {
            "status": "success",
            "config_id": config_id,  # ✅ Show the same config_id
            "sensor": sensor_type,
            "value": response_value,
            "log_id": new_log.id
        }

    except Exception as e:
        print("Error:", str(e))
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")

