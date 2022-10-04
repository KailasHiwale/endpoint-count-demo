import os
from dotenv import load_dotenv

dotenv_path = os.path.join(os.getcwd(), '.env')
load_dotenv(dotenv_path, verbose=True)

host = os.getenv('HOST')
port = os.getenv('PORT')
db_connection_string = os.getenv('MONGO_CONNECTION_STRING')
dbname = os.getenv('MONGO_DB_NAME')