from flask import Flask,redirect,render_template,url_for,request
from datetime import datetime
from flask_pymongo import PyMongo
from bson import ObjectId
from config import username,password
# import os

#instance of the imported flask 
app = Flask(__name__,template_folder="templates",static_folder="static")

#database connection 

app.config['MONGO_URI'] = 'mongodb://localhost:27017/flaskdb'
# app.config['MONGO_URI'] = 'mongodb+srv://{0}:<{1}>@cluster0-iaim4.gcp.mongodb.net/test?retryWrites=true&w=majority'.format(username,password)
taskdb = PyMongo(app)
#showing Views and functions applied 

@app.route('/' ,methods=['POST','GET'])
def index():
    # checking the method
    if request.method == 'POST':
    # declaring error 
        error = None
    # targeting the contents
        task_todo = request.form['content']
        date_create = datetime.utcnow()
    # Assigning to database 
        add_task = {'task': task_todo,
                    'date_created': date_create
                    }
    # Inserting to the database
        taskdb.db.users.insert_one(add_task)    
        return redirect('/')
    else:
    # to display on the tables after getting the method to be 'GET'
        tasks = taskdb.db.users.find()
        return render_template('index.html', tasks = tasks)

@app.route('/delete/<id>')
def delete(id):
    # targeting the data with the id 
    task_to_delete = taskdb.db.users.find_one({"_id":ObjectId(id)})
    try:
    # deleting it in the database 
        taskdb.db.users.delete_one(task_to_delete)
        return redirect('/')
    except:
        return 'There is an Error '

@app.route('/update/<id>', methods= ['GET','POST'])
def update(id):
        # targeting the data with the id 
    task_to_update = taskdb.db.users.find_one({'_id': ObjectId(id)})
    if request.method == 'POST':
        task_to_up = request.form['content']
        try:
        # updating from the database
            taskdb.db.users.update_one({"_id":ObjectId(id)}, { '$set' :{'task': task_to_up}})
            return redirect('/')
        except:
            return "There was an error updating your request"
    else:
        return render_template('update.html' ,task = task_to_update)

@app.route('/search' )
def searchresult():
    key = request.values.get('search')
    refer = request.values.get('refer')
    if (refer == '_id'):
        error = "No result found"
        todo_l = taskdb.db.users.find_one({refer:ObjectId(key)})
        return render_template('searchresult.html' , error = error)
    else:
        todo_l = taskdb.db.users.find_one({refer:key})
    return render_template('searchresult.html' ,task = todo_l)

@app.errorhandler(404)
def page_not_found(error):
    return "This page could not be found! Enter a valid one!",404


if __name__ == "__main__":
    app.run(debug=True)    