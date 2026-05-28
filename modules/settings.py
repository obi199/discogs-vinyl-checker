import os
from dotenv import load_dotenv

load_dotenv()

database_url = os.getenv('DATABASE_URL')

if database_url and (database_url.startswith('postgresql://') or database_url.startswith('postgres://')):
    # Fix for SQLAlchemy 1.4+ which requires postgresql:// instead of postgres://
    userdb = database_url.replace('postgres://', 'postgresql://', 1)
else:
    db_user = os.getenv('DATABASE_USER')
    db_pass = os.getenv('DATABASE_PASS')
    db_host = os.getenv('DATABASE_HOST', 'localhost')
    db_name = database_url
    # Construct PostgreSQL URI from components
    userdb = f"postgresql://{db_user}:{db_pass}@{db_host}/{db_name}"
table = os.getenv('TABLE_1') #"users"
SECRET_KEY=os.getenv('SECRET_KEY')
user_agent=os.getenv('USER_AGENT')
table2=os.getenv('TABLE_2') #i.e. "drumbreaks"

