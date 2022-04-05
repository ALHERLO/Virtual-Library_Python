from flask import Flask, render_template, request, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired, URL
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///new-books-collection.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False #THIS SILENCES THIS TYPE OF ERROR
db = SQLAlchemy(app)



class Books(db.Model):
   id = db.Column(db.Integer, primary_key = True)
   title = db.Column(db.String(100), unique=True, nullable=False)
   author = db.Column(db.String(50), nullable=False)
   rating = db.Column(db.Integer)

   def __repr__(self): #THIS ALLOWS THE BOOK TO BE REPRESENTED BY THEIR TITLE WHEN PRINTED
      return '<Books %r>' % self.title
      #return f'<Book {drlf.title}>'      THIS THE SAME AS THE PREVIOUS LINE


# db.create_all()

all_books = Books.query.all()


@app.route('/')
def home():
    all_books = db.session.query(Books).all()
    return render_template("index.html", books=all_books)


@app.route("/add", methods = ["GET", "POST"])
def add():
    if request.method == "POST":
        title = request.form["title"]
        author = request.form["author"]
        rating = request.form["rating"]
        new_book = Books(title=title, author=author, rating=rating)
        db.session.add(new_book)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template("add.html")



@app.route('/edit', methods=["GET","POST"])
def edit():
    if request.method == "POST":
        book_id = request.args.get('id') # HERE WE GET ID FROM ARGS
        new_rating = request.form["rating"]
        book_to_update = Books.query.filter_by(id=book_id).first()
        book_to_update.rating = new_rating
        db.session.commit()
        return redirect(url_for('home'))
    book_id = request.args.get('id')
    requested_book = Books.query.filter_by(id=book_id).first()
    return render_template("edit.html", book=requested_book)

@app.route('/delete')
def delete(): #THIS FUNCTION ONLY DELETES A FILE, DOES NOT RENDER HTML
        book_id = request.args.get('id')
        book_to_delete = Books.query.filter_by(id=book_id).first()
        print(f"Book to delete>>>> {book_to_delete}")
        db.session.delete(book_to_delete)
        db.session.commit()
        return redirect(url_for('home'))


if __name__ == "__main__":
    app.run(debug=True)

