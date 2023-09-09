import os

# Use the host machine's IP address to connect to PostgreSQL
SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'postgresql://ajay:ajay@192.168.1.28:5800/todo')
SQLALCHEMY_TRACK_MODIFICATIONS = False
