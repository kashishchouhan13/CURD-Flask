from flask import Flask ,render_template,request,redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os
app=Flask(__name__)
base_dir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI']=f'sqlite:///{os.path.join(base_dir,"posts.db")}'
db = SQLAlchemy(app)

class BlogPost(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  title = db.Column(db.String(80), unique=True, nullable=False)
  content = db.Column(db.Text(120), unique=True, nullable=False)
  author = db.Column(db.String(20),unique=True, nullable=False,default='N/A')
  date_posted = db.Column(db.String(80), unique=True, nullable=False,default=datetime.utcnow)

  def __repr__(self):
     return 'BlogPost'+ str(self.id)
  
all_posts= [
   {
      "title":"post 1",
      "content":"hello everyone i am learning flask",
      "author":"kashish"
   },
    {
      "title":"post 2",
      "content":"Feeling happy",
     
   }
]
@app.route('/')
def home():
    return render_template("flask.html")

@app.route('/posts/delete/<int:id>')
def delete(id):
   post=BlogPost.query.get_or_404(id)
   db.session.delete(post)
   db.session.commit()
   return redirect('/posts')

@app.route('/posts/edit/<int:id>',methods=['GET','POST'])
def edit(id):
   
   post=BlogPost.query.get_or_404(id)
   if request.method=='POST':
     post.title=request.form['title']  
     post.content=request.form['content']
     post.author=request.form['author']
     db.session.commit()
     return redirect('/posts')
   else:
     return render_template("edit.html",post=post)
   

@app.route('/posts',methods=['GET','POST'])
def posts():
    if request.method=='POST':  
      post_title=request.form['title']  
      post_content=request.form['content']
      post_author=request.form['author']
      # //object
      new_post=BlogPost(title=post_title,content=post_content,author=post_author)
      db.session.add(new_post)
      db.session.commit()
      return redirect('/posts')
    else:
      all_posts=BlogPost.query.order_by(BlogPost.date_posted).all()
      return render_template("posts.html",post=all_posts ) 
    
@app.route('/posts/new',methods=['GET','POST'])
def new_post():
   if request.method=='POST':
     post.title=request.form['title']  
     post.content=request.form['content']
     post.author=request.form['author']
     new_post=BlogPost(title=post_title,content=post_content,author=post_author)
     db.session.add(new_post)
     db.session.commit()
     return redirect('/posts')
   else:
     return render_template("new_post.html")

if __name__=='__main__':
    port = int(os.environ.get("POST",5000))
    app.run(host='0.0.0.0',port=port,debug=False)