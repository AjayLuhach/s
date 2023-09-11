import os

# Use the host machine's IP address to connect to PostgreSQL
SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'postgresql://postgres:ajay@localhost:5432/todo')
SQLALCHEMY_TRACK_MODIFICATIONS = False
#  'postgresql://postgres:ajay@host.docker.internal:5433/todo')