from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.orm import declarative_base
import datetime

Base = declarative_base()

class AMQPLog(Base):
    __tablename__ = "amqp_logs"

    id = Column(Integer, primary_key=True, index=True)
    message = Column(Text, nullable=False)  # ✅ This must have a value
    ip_address = Column(String, nullable=False)
    port = Column(Integer, nullable=False)
    protocol_name = Column(String, nullable=False)
    request_param = Column(String, nullable=False)
    response_value = Column(Text, nullable=False)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)
