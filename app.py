from flask import Flask, redirect, render_template, request, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os

# set up application
app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))
# app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{os.path.join(basedir, "instance", "test.db")}'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres.ykholzvnsdlkhpuyillb:KHr-Q3z-4c4-gQM@aws-0-eu-west-2.pooler.supabase.com:6543/postgres'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app) # initialise database with settings from the app


class Todo(db.Model): #initialise a class for our model, inheriting from db.Model
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    # completed = db.Column(db.Integer, default=0)
    date_created = db.Column(db.DateTime, default=datetime.now())

    def __repr__(self):
        return f"<Task {self.id}>" #return the id of the task thats been created
    



# create index route to avoid 404 using decorator
# define a simple function that returns a string 
@app.route('/', methods=['POST','GET']) #method options allows us to add 'POST' functionality
def index():
    if request.method == 'POST': # if the request sent to the route "/" is POST
        task_content = request.form['content'] #pass in the id of the form that we want to get the contents of
        new_task = Todo(content=task_content) #create a new task from the input based on our Todo database model object

        try:
            db.session.add(new_task)
            db.session.commit() #create new task and commit to database
            return redirect('/') #redirect back to the index
        except:
            return 'There was an issue adding your task'

    else:
        tasks = Todo.query.order_by(Todo.date_created).all() #return all database contents in order they were created
        return render_template("index.html", tasks=tasks) # if not a post request, view webpage. pass table variable created to template
    

@app.route('/delete/<int:id>') #create delete route that is called from a link in index.html
def delete(id): #pass in an id from one of the items in the database
    task_to_delete = Todo.query.get_or_404(id) #query the database for that id, returning a database object

    try:
        db.session.delete(task_to_delete) #delete that item from database
        db.session.commit()
        return redirect('/')
    except:
        return 'There was an issue deleting your task'
    
@app.route('/update/<int:id>', methods = ['GET', 'POST'])
def update(id):

    task_to_update = Todo.query.get_or_404(id)

    if request.method == 'POST':
        task_to_update.content = request.form['updatecontent'] # directly edit the content attribute of the task object 
        try:
            db.session.commit() # re commit, no need to do anything else
            return redirect('/')
        except:
            return 'There was an issue updating your task.'
    else:
        return render_template("update.html", task = task_to_update) #we create a new update html page that we get sent to, with an input bar on.pass the task in


# if running the programme directly, run the app, show debugging on webpage
if __name__ == '__main__':
    print("starting app")
    app.run(debug=True)
    
