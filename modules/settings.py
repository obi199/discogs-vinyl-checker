import os

userdb = os.getenv('DATABASE_URL') #DATABASE_URL_LOCAL
table = os.getenv('TABLE_1') #"users" #TABLE_1
SECRET_KEY=os.getenv('SECRET_KEY') #"jDuOXpDaXjdF8" #SECRET_KEY
user_agent=os.getenv('USER_AGENT') #"discogs_fast_checker/1.0" #USER_AGENT
table2=os.getenv('TABLE_2') #"drumbreaks" #TABLE_2
