import os
from datetime import datetime, timedelta
from pymongo import MongoClient

# Connect to MongoDB (Runs locally on your machine)
MONGO_URI = "mongodb://localhost:27017/"
client = MongoClient(MONGO_URI)
db = client["college"]  # Creates/uses 'college' database

def init_database():
    print("Initializing BiblioBot Database...")
    
    # Clean up any old data before starting fresh
    db.books.drop()
    db.admins.drop()
    db.users.drop()
    db.conversation_logs.drop()

    # Seed initial book catalog matching the report schema
    mock_books = [
        {
            "title": "Introduction to Algorithms",
            "author": "Thomas H. Cormen",
            "genre": "algorithms",
            "isbn": "9780262033848",
            "available": True,
            "issued_to": None,
            "return_date": None,
            "added_on": datetime.utcnow()
        },
        {
            "title": "Clean Code",
            "author": "Robert C. Martin",
            "genre": "software engineering",
            "isbn": "9780132350884",
            "available": False,
            "issued_to": "John Doe",
            "return_date": datetime.utcnow() + timedelta(days=7),
            "added_on": datetime.utcnow()
        },
        {
            "title": "The Pragmatic Programmer",
            "author": "Andrew Hunt",
            "genre": "software engineering",
            "isbn": "9780135957059",
            "available": True,
            "issued_to": None,
            "return_date": None,
            "added_on": datetime.utcnow()
        }
    ]
    db.books.insert_many(mock_books)
    print("✔ Database initialized successfully!")

if __name__ == "__main__":
    init_database()