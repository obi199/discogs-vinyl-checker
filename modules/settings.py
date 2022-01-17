import os
#userdb = r"sqlite:////home/obi/dev/python/discogs-checker/db/user.db"
userdb = r'postgres://gscikpcgepjvqm:f02461c199a6a555a6846025c2de077f7b8a6af02830a3ddf764a67f2c7281b7@ec2-18-234-17-166.compute-1.amazonaws.com:5432/dbpltgqbgksg4t'
#userdb = os.getenv('DATBASE_URL')
table = "users"
SECRET_KEY="jDuOXpDaXjdF8"
user_agent="discogs_fast_checker/1.0"
table2="drumbreaks"
