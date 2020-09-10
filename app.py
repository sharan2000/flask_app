from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://sharan_temp:/*18981Ach0535*/@localhost/Postsdb' #we are defining the database and the path to store the database file

db = SQLAlchemy(app) #the current app file is linked to the database

#we just linked the database but if we want to eanter any data into the database , we have to design it, we have to create a model
#so now we have to inherit a class from db object and we have to model it like what are the datatypes and names of the variables in the database

class BlogPost(db.Model) :   #we just created a model if we want to use to we have to create a database so we have to run a query in python interpreter by importing the db object and executing the db.create_all() function
                            #when we run that function the model we specified will be seen and a similar database is created where we specified the URI the name of the table in that databaes will be the same as the class name with some small change
  id = db.Column(db.Integer, primary_key = True)
  title = db.Column(db.String(100), nullable=False)
  content = db.Column(db.Text, nullable=False)
  author = db.Column(db.String(20), nullable=False, default='N/A')
  date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow) 

  def __repr__(self):
    return 'Blog Post' + str(self.id)


@app.route("/")
def home() :
  return render_template("index.html")


@app.route("/posts", methods=['GET', 'POST'])
def posts() :

    all_posts = BlogPost.query.order_by(BlogPost.date_posted).all() #order_by makes the values sorted from the model based on the value given to the function
    # .all() function is used to fetch all the values the values

    return render_template("posts.html", posts=all_posts)


@app.route("/posts/delete/<int:id>")
def delete(id) :
  post_to_delete = BlogPost.query.get_or_404(id)
  db.session.delete(post_to_delete)
  db.session.commit()
  return redirect('/posts')


@app.route('/posts/edit/<int:id>', methods=['GET', 'POST'])
def edit(id) :
  post_to_edit = BlogPost.query.get(id)

  if request.method == "POST" :
    
    post_title = request.form['title']
    post_content = request.form['content']
    post_author = request.form['author']
    
    if(post_author == "") :
      post_author = 'N/A'

    post_to_edit.title = post_title
    post_to_edit.content = post_content
    post_to_edit.author = post_author

    db.session.commit()

    return redirect("/posts")

  else :
    return render_template('edit.html', post=post_to_edit)


@app.route('/posts/new', methods=['GET', 'POST'])
def new_post() :
  if(request.method == 'POST') :
    post_title = request.form['title']
    post_content = request.form['content']
    post_author = request.form['author']

    if(post_author == "") :
      post_author = 'N/A'

    new_post = BlogPost(title=post_title, content=post_content, author=post_author) #this is used to create a new row object for the model/table by using the model name
    db.session.add(new_post) #here we are stating a session and adding the new object to that model table
    db.session.commit() #we should commit the session for the changes to be visible in the database
    
    return redirect('/posts') #we are redirecting to the posts page
  
  else :
    return render_template('new_post.html')

# @app.route("/home/users/<string:name>/posts/<int:num>") #using the a part of url as a parameter #used in dynamic url's where we fetch a user record based on his name in the url ,. etc
# def hello_world(name, num) :
#   return "Hello " + name + ", here is your post having post id " + str(num) #we have to change all datatypes to string when returning

# @app.route("/get_page", methods=["GET"]) #if we don't specify the methods keyword the it will take get method for that route #if we specify the methods keyword then it will only take the methods that are specified in that list
# def get_page() :
#   return "this page is using get request"


if __name__ == "__main__" :
  app.run(debug=True)