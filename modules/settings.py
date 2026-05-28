import os
from dotenv import load_dotenv

load_dotenv()

db_user = os.getenv('DATABASE_USER')
db_pass = os.getenv('DATABASE_PASS')
db_name = os.getenv('DATABASE_URL')
# Construct PostgreSQL URI
userdb = f"postgresql://{db_user}:{db_pass}@localhost/{db_name}"
table = os.getenv('TABLE_1') #"users"
SECRET_KEY=os.getenv('SECRET_KEY')
user_agent=os.getenv('USER_AGENT')
table2=os.getenv('TABLE_2') #i.e. "drumbreaks"

