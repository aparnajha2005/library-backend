from flask import Flask, request, jsonify
from flask_cors import CORS
from pymongo import MongoClient
from bson import ObjectId

app = Flask(__name__)
CORS(app)

client = MongoClient("mongodb://localhost:27017/")
db = client["lib-database"]
books_collection = db["books"]

BOOKS_PER_PAGE = 100  # or increase to 100 if you want

def serialize_book(book):
    book["_id"] = str(book["_id"])
    return book

@app.route('/api/books')
def api_books():
    page = int(request.args.get('page', 1))
    query = {}

    skip = (page - 1) * BOOKS_PER_PAGE

    cursor = books_collection.find(query).skip(skip).limit(BOOKS_PER_PAGE)
    books = [serialize_book(book) for book in cursor]

    total_books = books_collection.count_documents(query)
    total_pages = (total_books + BOOKS_PER_PAGE - 1) // BOOKS_PER_PAGE

    return jsonify({
        "books": books,
        "page": page,
        "total_pages": total_pages,
        "total_books": total_books,
    })

if __name__ == '__main__':
    app.run(debug=True, use_reloader=False)
