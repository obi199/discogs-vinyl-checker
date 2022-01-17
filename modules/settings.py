import os
#userdb = r"sqlite:////home/obi/dev/python/discogs-checker/db/user.db"

userdb = os.getenv('DATBASE_URL')
table = "users"
SECRET_KEY="jDuOXpDaXjdF8"
user_agent="discogs_fast_checker/1.0"
table2="drumbreaks"
