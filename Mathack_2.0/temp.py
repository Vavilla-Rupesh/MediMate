from flask import Flask, render_template, request, redirect, url_for,flash
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:Lakshman123@localhost:5432/MathHack'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'nokey'
# Initialize the database
db = SQLAlchemy(app)

class Authenticate(db.Model):
    __tablename__ = 'authenticate'  # Specify the table name

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), nullable=False, unique=True)
    password = db.Column(db.String(150), nullable=False)

    def __init__(self, username, password):
        self.username = username
        self.password = password

@app.route('/')
def home():
    return render_template('index.html')

# Directory where uploaded files will be stored
UPLOAD_FOLDER = 'uploads/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Allowed file extensions
ALLOWED_EXTENSIONS = {'pdf'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # Check if the post request has the file part
        if 'file' not in request.files:
            return 'No file part'
        file = request.files['file']
        # If the user does not select a file, the browser submits an empty file without a filename
        if file.filename == '':
            return 'No selected file'
        if file and allowed_file(file.filename):
            filename = file.filename
            # Save the file to the uploads folder
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return 'File successfully uploaded'
    return render_template('upload.html')

@app.route('/register', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Create a new Authenticate object
        new_user = Authenticate(username=username, password=password)

        try:
            # Add the new user to the authenticate table
            db.session.add(new_user)
            db.session.commit()
            return 'User successfully registered'
        except Exception as e:
            return f'There was an issue adding the user: {str(e)}'

    return render_template('register.html')
@app.route('logini')
def logini():
    return render_template("login.html")
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Query the database for the user
        user = Authenticate.query.filter_by(username=username, password=password).first()

        if user:
            flash('Login successful')
            return redirect(url_for('home'))
        else:
            flash('Invalid username or password')

    return render_template('login.html')

if __name__ == '__main__':
    app.run(debug=True)
