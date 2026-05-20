from flask import Flask, request, jsonify
from flask_cors import CORS
from pymongo import MongoClient
from datetime import datetime
from nlp_module import classify_intent, extract_entities

import nltk
nltk.download('punkt')
nltk.download('punkt_tab')
nltk.download('stopwords')

app = Flask(__name__)
CORS(app, origins=["http://localhost:5173", "http://localhost:5174", "http://127.0.0.1:5173", "http://127.0.0.1:5174"]) # Allows your React interface to contact this server cleanly

# Connect to database collections
client = MongoClient("mongodb://localhost:27017/")
db = client["college"]

def query_books(intent, user_input, session_id):
    clean_query = user_input.lower()
    
    if intent == 'GENERAL_QUERY':
        return "The Central Library is open Monday through Saturday, from 9:00 AM to 6:00 PM."

    elif intent == 'SEARCH_BOOK':
        books = list(db.books.find({
            "$or": [
                {"title": {"$regex": clean_query, "$options": "i"}},
                {"author": {"$regex": clean_query, "$options": "i"}}
            ]
        }))
        if not books:
            return "I couldn't find any matching books in the catalog."
        
        # Log searched book history to profile database for recommendations
        for b in books:
            db.users.update_one(
                {"session_id": session_id},
                {"$addToSet": {"search_history": b["genre"]}, "$set": {"last_active": datetime.utcnow()}},
                upsert=True
            )
            
        reply = "Here is what I found:\n"
        for b in books:
            status = "Available" if b["available"] else "Issued"
            reply += f"- **{b['title']}** by {b['author']} [{status}]\n"
        return reply

    elif intent == 'CHECK_AVAILABILITY':
        book = db.books.find_one({"title": {"$regex": clean_query, "$options": "i"}})
        if not book:
            return "That book doesn't appear to exist in our library management index."
        if book["available"]:
            return f"Yes! '{book['title']}' is currently available on the shelf."
        else:
            return f"'{book['title']}' is currently out. Expected return: {book['return_date'].strftime('%Y-%m-%d')}."

    elif intent == 'GET_RECOMMENDATION':
        user_profile = db.users.find_one({"session_id": session_id})
        if user_profile and user_profile.get("search_history"):
            fav_genres = user_profile["search_history"]
            recommendations = list(db.books.find({"genre": {"$in": fav_genres}, "available": True}).limit(3))
        else:
            recommendations = list(db.books.find({"available": True}).limit(3))
            
        if not recommendations:
            return "I don't have enough history to make custom recommendations yet!"
            
        reply = "Here are a few books you might enjoy:\n"
        for r in recommendations:
            reply += f"- **{r['title']}** by {r['author']}\n"
        return reply

    return "I am configured to help you find books, check system availability, or offer suggestions. Could you please rephrase?"

@app.route('/api/chat', methods=['POST'])
def chat():
    data = request.get_json() or {}
    user_input = data.get('message', '')
    session_id = data.get('session_id', 'default')
    
    intent = classify_intent(user_input)
    reply = query_books(intent, user_input, session_id)
    
    # Save a record of the conversation in MongoDB
    db.conversation_logs.insert_one({
        "session_id": session_id,
        "user_query": user_input,
        "bot_reply": reply,
        "detected_intent": intent,
        "timestamp": datetime.now()
    })
    
    return jsonify({'reply': reply, 'intent': intent})

if __name__ == '__main__':
    app.run(debug=True, port=5000, host='0.0.0.0')