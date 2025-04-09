# AMQP Protocol Integration with FastAPI and PostgreSQL

This project demonstrates the integration of FastAPI with RabbitMQ (using the AMQP protocol) and PostgreSQL. It includes:

- **FastAPI**: A modern, fast web framework for building APIs with Python.
- **RabbitMQ**: A message broker implementing the AMQP protocol.
- **PostgreSQL**: A powerful, open-source relational database system.

## Features

- **AMQP Publisher (`amqp_publisher.py`)**: Sends messages to RabbitMQ.
- **AMQP Consumer (`amqp_consumer.py`)**: Listens for messages from RabbitMQ and processes them.
- **Database Models (`models.py`)**: Defines the structure of the database tables using SQLAlchemy.
- **Database Connection (`database.py`)**: Handles the connection to the PostgreSQL database.
- **API Endpoints (`main.py`)**: Implements API routes using FastAPI.

## Getting Started

### Prerequisites

Ensure you have the following installed:

- Python 3.8 or higher
- PostgreSQL
- RabbitMQ

### Installation

1. **Clone the Repository**:

   ```bash
   git clone https://github.com/UBS25/AMQP_Protocol_FastAPI_PostgreSQL.git
   cd AMQP_Protocol_FastAPI_PostgreSQL
Set Up a Virtual Environment:

bash
Copy
Edit
python -m venv venv
source venv/bin/activate  # On Windows use 'venv\Scripts\activate'
Install Dependencies:

Create a requirements.txt file with the following content:

nginx
Copy
Edit
fastapi
uvicorn
pika
sqlalchemy
psycopg2
Then, install the dependencies:

bash
Copy
Edit
pip install -r requirements.txt
Configure Environment Variables:

Set up the following environment variables:

DATABASE_URL: PostgreSQL connection string (e.g., postgresql://user:password@localhost/dbname)

RABBITMQ_URL: RabbitMQ connection string (e.g., amqp://guest:guest@localhost/)

Database Setup
Apply Migrations:

If using Alembic for migrations:

bash
Copy
Edit
alembic upgrade head
Alternatively, create tables directly from models.py:

python
Copy
Edit
from database import engine
from models import Base

Base.metadata.create_all(bind=engine)
Running the Application
Start RabbitMQ:

Ensure RabbitMQ is running. You can start it with:

bash
Copy
Edit
rabbitmq-server
Run the FastAPI Application:

bash
Copy
Edit
uvicorn main:app --reload
The API will be accessible at http://127.0.0.1:8000.

Start the AMQP Consumer:

In a separate terminal, run:

bash
Copy
Edit
python amqp_consumer.py
This will start the consumer that listens for messages from RabbitMQ.

API Endpoints
POST /send-message/: Sends a message to RabbitMQ.

Example using curl:

bash
Copy
Edit
curl -X POST "http://127.0.0.1:8000/send-message/" -H "Content-Type: application/json" -d '{"message": "Hello, RabbitMQ!"}'
Contributing
Contributions are welcome! Please fork the repository and submit a pull request with your changes.

License
This project is licensed under the MIT License. See the LICENSE file for details.

python
Copy
Edit

**Notes**:

- Ensure that the `requirements.txt` file is created with the specified dependencies before running the installation commands.
- The environment variables `DATABASE_URL` and `RABBITMQ_URL` should be set appropriately for your setup.
- If you're using Alembic for database migrations, ensure it's configured correctly. Otherwise, you can create tables directly from the models as shown.

Feel free to customize this README to better fit the specifics of your project!
::contentReference[oaicite:0]{index=0}
