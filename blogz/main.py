from flask import Flask, request, redirect, render_template, session, flash
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://blogz:beproductive@localhost:8889/blogz'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
app.secret_key = 'yxyxy'


class Blog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    post = db.Column(db.String(120))
    title = db.Column(db.String(120))
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    

    def __init__(self, post, title, owner):
        self.post = post
        self.title = title
        self.owner = owner


class User(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(120))
    blogs = db.relationship('Blog', backref='owner')

    def __init__(self, username, password):
        self.username = username
        self.password = password

@app.before_request
def require_login():
    allowed_routes = ['login', 'signup', 'blog', '']
    if request.endpoint not in allowed_routes and 'username' not in session:
        return redirect('/login')



@app.route('/login', methods=["Post", 'GET'])
def login(): #Page to login to current account
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and user.password == password:
            session['username'] = username
            flash("Logged in")
            return redirect('/new') 
        if user and not user.password == pass_word:
            flash('Password is incorrect')
            return redirect('/login')
        if not user:
            flash('User does not exist')
            return redirect('/login')
        
    return render_template('login.html')



@app.route('/signup',  methods=["Post", "GET"])
def signup(): #Page to create a new account
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        verify = request.form['verify']
        existing_user = User.query.filter_by(username=username).first()


        if existing_user:
            return flash('User already exists')
        if len(username) == 0 or len(password) == 0 or len(verify) == 0:
            flash('One or more fields are invalid')
        if not password == verify:
            flash('Passwords do not match')
        if len(username) <= 3:
            flash('Username must be greater than 3 characters')
        if len(password) <=3:
            flash('Password must be greater than 3 characters')


        if not existing_user:
            new_user = User(username, password)
            db.session.add(new_user)
            db.session.commit()
            session['username'] = username
            return redirect('/new') 
    return render_template('signup.html')



@app.route('/logout')
def logout():
    del session['username']
    return redirect('/login')



@app.route('/base', methods=["POST", "GET"])
def base(): #Base page easter egg.
    return render_template('base.html', title="Are You Ready To Join The World Of Blog Building")



@app.route('/', methods=['POST','GET'])
def index(): #Home page displaying all usernames.
    user = User.query.all()
    username = request.args.get('username')
    return render_template('index.html', user=user, username=username, title='Blog Authors')
   




@app.route('/blog', methods=['POST', 'GET'])
def blogs(): #Blog page to show all blogs posted by all users.
    blog = Blog.query.all()
    for post in blog:
        user = User.query.filter_by(id=post.owner_id).first()
        
        return render_template('blogs.html', blog=blog, user=user)
    




@app.route('/new', methods=['POST', 'GET'])
def new(): #Page for new blog to be added.
    owner = User.query.filter_by(username=session['username']).first()
    if request.method == 'POST':
        title = request.form['title']
        post = request.form['blog']
        new_post = Blog(post, title, owner)
        db.session.add(new_post)
        db.session.commit()
        return render_template('new_post.html',blog=new_post)
    return render_template('new.html')



@app.route('/newpost')
def linked(): #Page to display selected post.
    name = request.args.get('id')
    new_post = Blog.query.get(name)
    return render_template('new_post.html', blog=new_post, id=name)

@app.route('/single_user')
def single_user():
    name = request.args.get('owner')
    new_posts = Blog.query.filter_by(owner_id=name).all()
    return render_template('single_user.html', blog=new_posts, id=name)


# while on authors page, clicking a link will take you to a page displaying all of that users post



        









    
if __name__ == '__main__':
    app.run()
