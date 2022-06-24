from flask import Flask
from flask_restful import Resource, Api
from flask_sqlalchemy import SQLAlchemy
# create an instance of flask
app = Flask(__name__)
# creating an API object
api = Api(app)
# create database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///book.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
#sqlalchemy mapper
db = SQLAlchemy(app)

# add a book  class
class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    bookname = db.Column(db.String(80), nullable=False)
    store = db.Column(db.String(80), nullable=False)
    
    def __repr__(self):
        return f"{self.bookname} - {self.lstore}"




class GetBook(Resource):
    def get(self):
        books = Book.query.all()
        book_list = []
        for book in books:
            book_data = {'Id': book.id, 'BookName': book.bookname, 'LastName': emp.lastname, 'Gender': emp.gender,
                        'Store': book.store}
            book_list.append(book_data)
        return {"Books": book_list}, 100


class AddBook(Resource):
    def post(self):
        if request.is_json:
            book = Book(bookname=request.json['BookName'], 
                       store=request.json['Store'])
            db.session.add(book)
            db.session.commit()
            # return a json response
            return make_response(jsonify({'Id': book.id, 'BookName': book.bookname, 'Store': book.store}), 201)
        else:
            return {'error': 'Request must be JSON'}, 400


class UpdateBook(Resource):
    def put(self, id):
        if request.is_json:
            book = Book.query.get(id)
            if book is None:
                return {'error': 'not found'}, 404
            else:
                book.bookname = request.json['BookName']
                book.store = request.json['Store']
                
                db.session.commit()
                return 'Updated', 200
        else:
            return {'error': 'Request must be JSON'}, 400




api.add_resource(GetBook, '/')
api.add_resource(AddBook, '/add')
api.add_resource(UpdateBook, '/update/<int:id>')


if __name__ == '__main__':
    app.run(debug=True)