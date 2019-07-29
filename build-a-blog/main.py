from flask import Flask, request, redirect, render_template, session, flash
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:beproductive@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
app.secret_key = 'yxyxy'


class Blog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    post = db.Column(db.String(120))
    title = db.Column(db.String(120))
    

    def __init__(self, post, title):
        self.post = post
        self.title = title


@app.route('/', methods=["POST", "GET"])
def index():
    return redirect('/blog')


@app.route('/blog', methods=['POST', 'GET'])
def blogs():
    blog = Blog.query.all()
    return render_template('blogs.html', blog=blog)

@app.route('/new', methods=['POST', 'GET'])
def new():
    if request.method == 'POST':
        title = request.form['title']
        post = request.form['blog']
        new_post = Blog(post, title)
        db.session.add(new_post)
        db.session.commit()
        return render_template('new_post.html',blog=new_post)
    return render_template('new.html')


@app.route('/newpost')
def linked(): #Page to display selected post.
    name = request.args.get('id')
    new_post = Blog.query.get(name)
    return render_template('new_post.html', blog=new_post, id=name)
        
    
    
if __name__ == "__main__":
    app.run()