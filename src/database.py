import os
from src.models import Base
from dotenv import load_dotenv
from sqlalchemy import create_engine, text


# Load variables from .env
load_dotenv()


# Read database credentials from environment variables
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")

# Path to the Aiven CA certificate
CA_CERT_PATH = os.path.join(
    os.path.dirname(os.path.dirname(__file__)),
    "aiven-ca.pem"
)


# Create PostgreSQL connection URL
DATABASE_URL = (
    f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}"
    f"@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)


# Create SQLAlchemy engine
engine = create_engine(
    DATABASE_URL,
    connect_args={
        "sslmode": "verify-ca",
        "sslrootcert": CA_CERT_PATH,
    },
    pool_pre_ping=True,
)


# Simple database connection test
def test_connection():
    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))

        print("PostgreSQL connection successful!")

    except Exception as e:
        print("PostgreSQL connection failed.")
        print("Error:", e)
        
def create_tables():
    try:
        Base.metadata.create_all(bind=engine)
        print("Database tables created successfully!")

    except Exception as e:
        print("Table creation failed.")
        print("Error:", e)