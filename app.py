from flask import Flask,render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime 

app = Flask(__name__)  # Create the Flask app object
app.config['SQLALCHEMY_DATABASE_URI'] ='sqlite:///todo.db'  # Connect to SQLite database
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db=SQLAlchemy(app)

class Todo(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    desc = db.Column(db.String(500), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow) 

    def __repr__(self) -> str:
        return f"{self.sno} - {self.title}"

@app.route("/", methods=['GET', 'POST'])  # Define a route for the home page
def home():
    if request.method=='POST':
        title=request.form['title']
        desc=request.form['desc']
        todo = Todo(title=title, desc=desc)
        db.session.add(todo)
        db.session.commit()

    allTodo = Todo.query.all()  # Retrieve all todos
    return render_template("index.html", allTodo=allTodo)

@app.route("/show")  # Define a route for the home page
def products():
    allTodo= Todo.query.all()
    print(allTodo)
    return "This is product page"
@app.route("/update/<int:sno>", methods=['GET', 'POST'])
def update(sno):
    if request.method=='POST':
        title=request.form['title']
        desc=request.form['desc']
        todo= Todo.query.filter_by(sno=sno).first()
        todo.title=title 
        todo.desc=desc
        db.session.add(todo)
        db.session.commit()
        return redirect("/")

    todo= Todo.query.filter_by(sno=sno).first()
    return render_template("update.html", todo=todo)


@app.route("/delete/<int:sno>")  
def delete(sno):
    todo= Todo.query.filter_by(sno=sno).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True,)
    
# from flask import Flask, render_template
# from flask_sqlalchemy import SQLAlchemy 
# from datetime import datetime

# app = Flask(__name__)  # Create the Flask app object
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'  # Connect to SQLite database
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# db = SQLAlchemy(app)

# class Todo(db.Model):
#     sno = db.Column(db.Integer, primary_key=True)
#     title = db.Column(db.String(200), nullable=False)
#     desc = db.Column(db.String(500), nullable=False)
#     date_created = db.Column(db.DateTime, default=datetime.utcnow)

#     def __repr__(self) -> str:
#         return f"{self.sno} - {self.title}"

# @app.route("/")  # Define a route for the home page
# def home():
#     # Check if the Todo already exists
#     if not Todo.query.filter_by(title="First Todo").first():
#         todo = Todo(title="First Todo", desc="Invest in Stock Market")
#         db.session.add(todo)
#         db.session.commit()
#     todos = Todo.query.all()  # Retrieve all todos

#     return render_template("index.html", todos=todos)

# @app.route("/show")  # Define a route for the products page
# def products():
#     allTodo=Todo.query.all()
#     print(allTodo)
#     return "This is the product page"

# if __name__ == "__main__":
#     with app.app_context():  # Ensure proper app context for database operations
#         db.create_all()  # Create tables in the database
#     app.run(debug=True)
