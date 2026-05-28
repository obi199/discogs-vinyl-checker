import os
from dotenv import load_dotenv
from modules import create_app, db
from passlib.hash import sha256_crypt

def initialize_database():
    load_dotenv()
    
    app = create_app()
    with app.app_context():
        print("Initializing database...")
        db.dbase.create_all()
        print("Tables created successfully.")

        # Add demo user
        username = os.getenv("DEMO_USER", "demo")
        password = os.getenv("DEMO_PASS", "password123")
        
        # Check if user already exists
        existing_user = db.User.query.filter_by(username=username).first()
        if not existing_user:
            print(f"Creating demo user: {username}")
            hashed_password = sha256_crypt.encrypt(password)
            new_user = db.User(
                username=username,
                password=hashed_password,
                consumer_key='',
                consumer_secret='',
                oauth_token='',
                oauth_token_secret=''
            )
            db.dbase.session.add(new_user)
            db.dbase.session.commit()
            print("Demo user created.")
        else:
            print("Demo user already exists.")

if __name__ == "__main__":
    try:
        initialize_database()
        print("Database initialization complete.")
    except Exception as e:
        print(f"Error during initialization: {e}")
