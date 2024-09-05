# # # from huggingface_hub import InferenceClient
# # # import pdfplumber
# # # from flask_sqlalchemy import SQLAlchemy
# # # from flask import Flask, render_template, request, redirect, url_for, flash, session
# # # import os

# # # app = Flask(__name__)
# # # app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:v4chparuma@localhost:5432/MathHack'
# # # app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# # # app.secret_key = 'nokey'

# # # db = SQLAlchemy(app)

# # # # Directory where uploaded files will be stored
# # # UPLOAD_FOLDER = 'static/uploads/'
# # # app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# # # # Allowed file extensions
# # # ALLOWED_EXTENSIONS = {'pdf'}

# # # # User Authentication Model
# # # class Authenticate(db.Model):
# # #     __tablename__ = 'authenticate'  # Specify the table name

# # #     id = db.Column(db.Integer, primary_key=True)
# # #     username = db.Column(db.String(150), nullable=False, unique=True)
# # #     password = db.Column(db.String(150), nullable=False)

# # #     def __init__(self, username, password):
# # #         self.username = username
# # #         self.password = password

# # # # Conversation Model
# # # class Conversation(db.Model):
# # #     __tablename__ = 'conversations'
# # #     id = db.Column(db.Integer, primary_key=True)
# # #     user_id = db.Column(db.Integer, nullable=False)
# # #     user_message = db.Column(db.Text, nullable=True)
# # #     bot_message = db.Column(db.Text, nullable=True)
# # #     pdf_file = db.Column(db.String(150), nullable=True)

# # #     def __init__(self, user_id, user_message=None, bot_message=None, pdf_file=None):
# # #         self.user_id = user_id
# # #         self.user_message = user_message
# # #         self.bot_message = bot_message
# # #         self.pdf_file = pdf_file

# # # def allowed_file(filename):
# # #     return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# # # def get_user_id():
# # #     # Get the current logged-in user's ID
# # #     return session.get('user_id')

# # # def llm(query):
# # #     client = InferenceClient(
# # #         "mistralai/Mistral-Nemo-Instruct-2407",
# # #         token="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",
# # #     )
# # #     a = ""
# # #     for message in client.chat_completion(
# # #         messages=[{"role": "system", "content": "You are an expert and experienced from the healthcare and biomedical domain with extensive medical knowledge and practical experience. Your name is OpenBioLLM, and you were developed by Saama AI Labs. who's willing to help answer the user's query with explanation. In your explanation, leverage your deep medical expertise such as relevant anatomical structures, physiological processes, diagnostic criteria, treatment guidelines, or other pertinent medical concepts. Use precise medical terminology while still aiming to make the explanation clear and accessible to a general audience."},
# # #                   {"role": "user", "content": query}],
# # #         max_tokens=500,
# # #         stream=True,
# # #     ):
# # #         a = a + message.choices[0].delta.content
# # #     return a

# # # def read_pdf(path):
# # #     with pdfplumber.open(path) as pdf:
# # #         text = ""
# # #         for page in pdf.pages:
# # #             text += page.extract_text()
# # #     return text

# # # def generate_bot_response(user_message):
# # #     user_id = get_user_id()

# # #     # Fetch the most recent conversation with a PDF file associated with the current user
# # #     conversation = Conversation.query.filter_by(user_id=user_id).filter(Conversation.pdf_file.isnot(None)).order_by(Conversation.id.desc()).first()

# # #     if conversation and conversation.pdf_file:
# # #         pdf_path = os.path.join(app.config['UPLOAD_FOLDER'], conversation.pdf_file)
# # #         pdf_content = read_pdf(pdf_path)
# # #         full_message = pdf_content + " " + user_message
# # #     else:
# # #         full_message = user_message  # If no PDF is associated, just pass the user's message

# # #     # Generate bot response using LLM
# # #     return llm(full_message)

# # # # Home Page
# # # @app.route('/')
# # # def home():
# # #     return render_template('index.html')

# # # # User Registration
# # # @app.route('/register', methods=['GET', 'POST'])
# # # def register():
# # #     if request.method == 'POST':
# # #         username = request.form['username']
# # #         password = request.form['password']

# # #         # Create a new Authenticate object
# # #         new_user = Authenticate(username=username, password=password)

# # #         try:
# # #             # Add the new user to the authenticate table
# # #             db.session.add(new_user)
# # #             db.session.commit()
# # #             return 'User successfully registered'
# # #         except Exception as e:
# # #             return f'There was an issue adding the user: {str(e)}'
# # #     return render_template('login.html')

# # # # User Login
# # # @app.route('/login', methods=['GET', 'POST'])
# # # def login():
# # #     if request.method == 'POST':
# # #         username = request.form['username']
# # #         password = request.form['password']
# # #         user = Authenticate.query.filter_by(username=username, password=password).first()

# # #         if user:
# # #             session['user_id'] = user.id
# # #             flash('Login successful')
# # #             return redirect(url_for('welcome'))
# # #         else:
# # #             flash('Invalid username or password')

# # #     return render_template('login.html')

# # # # Welcome Page (after login)
# # # @app.route('/welcome', methods=['GET', 'POST'])
# # # def welcome():
# # #     if 'user_id' not in session:
# # #         flash('Please log in first')
# # #         return redirect(url_for('login'))

# # #     user_id = get_user_id()
# # #     if request.method == 'POST':
# # #         user_message = request.form['message']
# # #         file = request.files.get('file')

# # #         pdf_filename = None
# # #         if file and allowed_file(file.filename):
# # #             pdf_filename = file.filename
# # #             file.save(os.path.join(app.config['UPLOAD_FOLDER'], pdf_filename))

# # #         bot_message = generate_bot_response(user_message)

# # #         conversation = Conversation(user_id=user_id, user_message=user_message, bot_message=bot_message, pdf_file=pdf_filename)
# # #         db.session.add(conversation)
# # #         db.session.commit()

# # #     conversations = Conversation.query.filter_by(user_id=user_id).all()
# # #     return render_template('/welcome.html', conversations=conversations)

# # # # Logout
# # # @app.route('/logout')
# # # def logout():
# # #     session.pop('user_id', None)
# # #     flash('You have been logged out')
# # #     return redirect(url_for('login'))

# # # if __name__ == '__main__':
# # #     app.run(debug=True)
# # from huggingface_hub import InferenceClient
# # import pdfplumber
# # from flask_sqlalchemy import SQLAlchemy
# # from flask import Flask, render_template, request, redirect, url_for, flash, session
# # import os

# # app = Flask(__name__)
# # app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:v4chparuma@localhost:5432/MathHack'
# # app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# # app.secret_key = 'nokey'

# # db = SQLAlchemy(app)

# # # Directory where uploaded files will be stored
# # UPLOAD_FOLDER = 'static/uploads/'
# # app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# # # Allowed file extensions
# # ALLOWED_EXTENSIONS = {'pdf'}

# # # User Authentication Model
# # class Authenticate(db.Model):
# #     __tablename__ = 'authenticate'  # Fixed the tablename syntax

# #     id = db.Column(db.Integer, primary_key=True)
# #     username = db.Column(db.String(150), nullable=False, unique=True)
# #     password = db.Column(db.String(150), nullable=False)

# #     def __init__(self, username, password):  # Fixed the constructor method
# #         self.username = username
# #         self.password = password

# # # Conversation Model
# # class Conversation(db.Model):
# #     __tablename__ = 'conversations'  # Fixed the tablename syntax
# #     id = db.Column(db.Integer, primary_key=True)
# #     user_id = db.Column(db.Integer, nullable=False)
# #     user_message = db.Column(db.Text, nullable=True)
# #     bot_message = db.Column(db.Text, nullable=True)
# #     pdf_file = db.Column(db.String(150), nullable=True)

# #     def __init__(self, user_id, user_message=None, bot_message=None, pdf_file=None):  # Fixed the constructor method
# #         self.user_id = user_id
# #         self.user_message = user_message
# #         self.bot_message = bot_message
# #         self.pdf_file = pdf_file

# # def allowed_file(filename):
# #     return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# # def get_user_id():
# #     return session.get('user_id')

# # def llm(query):
# #     client = InferenceClient(
# #         "mistralai/Mistral-Nemo-Instruct-2407",
# #         token="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",
# #     )
# #     a = ""
# #     for message in client.chat_completion(
# #         messages=[{"role": "system", "content": "You are an expert and experienced from the healthcare and biomedical domain with extensive medical knowledge and practical experience. Your name is OpenBioLLM, and you were developed by Saama AI Labs. who's willing to help answer the user's query with explanation. In your explanation, leverage your deep medical expertise such as relevant anatomical structures, physiological processes, diagnostic criteria, treatment guidelines, or other pertinent medical concepts. Use precise medical terminology while still aiming to make the explanation clear and accessible to a general audience."},
# #                   {"role": "user", "content": query}],
# #         max_tokens=500,
# #         stream=True,
# #     ):
# #         a += message.choices[0].delta.content
# #     return a

# # def read_pdf(path):
# #     with pdfplumber.open(path) as pdf:
# #         text = ""
# #         for page in pdf.pages:
# #             text += page.extract_text()
        
# #     return text

# # def generate_bot_response(user_message):
# #     user_id = get_user_id()

# #     # Fetch the most recent conversation with a PDF file associated with the current user
# #     conversation = Conversation.query.filter_by(user_id=user_id).filter(Conversation.pdf_file.isnot(None)).order_by(Conversation.id.desc()).first()

# #     if conversation and conversation.pdf_file:
# #         pdf_path = os.path.join(app.config['UPLOAD_FOLDER'], conversation.pdf_file)
# #         pdf_content = read_pdf(pdf_path)
# #         full_message = pdf_content + " " + user_message
# #     else:
# #         full_message = user_message  # If no PDF is associated, just pass the user's message
# #     response = llm(full_message)
# #     # Generate bot response using LLM
# #     print(response)
# #     return response

# # # Home Page
# # @app.route('/')
# # def home():
# #     return render_template('index.html')

# # # User Registration
# # @app.route('/register', methods=['GET', 'POST'])
# # def register():
# #     if request.method == 'POST':
# #         username = request.form['username']
# #         password = request.form['password']

# #         # Create a new Authenticate object
# #         new_user = Authenticate(username=username, password=password)

# #         try:
# #             # Add the new user to the authenticate table
# #             db.session.add(new_user)
# #             db.session.commit()
# #             # return 'User successfully registered'
# #             return redirect(url_for('login'))
# #         except Exception as e:
# #             return f'There was an issue adding the user: {str(e)}'
# #     return render_template('register.html')

# # # User Login
# # @app.route('/login', methods=['GET', 'POST'])
# # def login():
# #     if request.method == 'POST':
# #         username = request.form['username']
# #         password = request.form['password']
# #         user = Authenticate.query.filter_by(username=username, password=password).first()

# #         if user:
# #             session['user_id'] = user.id
# #             flash('Login successful')
# #             return redirect(url_for('welcome'))
# #         else:
# #             flash('Invalid username or password')

# #     return render_template('login.html')

# # # Welcome Page (after login)
# # @app.route('/welcome', methods=['GET', 'POST'])
# # def welcome():
# #     if 'user_id' not in session:
# #         flash('Please log in first')
# #         return redirect(url_for('login'))

# #     user_id = get_user_id()
# #     if request.method == 'POST':
# #         user_message = request.form['message']
# #         file = request.files.get('file')

# #         pdf_filename = None
# #         if file and allowed_file(file.filename):
# #             pdf_filename = file.filename
# #             file.save(os.path.join(app.config['UPLOAD_FOLDER'], pdf_filename))

# #         bot_message = generate_bot_response(user_message)
# #         print(bot_message)
# #         conversation = Conversation(user_id=user_id, user_message=user_message, bot_message=bot_message, pdf_file=pdf_filename)
# #         db.session.add(conversation)
# #         db.session.commit()

# #     conversations = Conversation.query.filter_by(user_id=user_id).all()
# #     return render_template('welcome.html', conversations=conversations)

# # @app.route('/appointment', methods=['GET', 'POST'])
# # def appointment():
# #     return render_template("appointment.html")

# # # Logout
# # @app.route('/logout')
# # def logout():
# #     session.pop('user_id', None)
# #     flash('You have been logged out')
# #     return redirect(url_for('login'))

# # if __name__ == '__main__':
# #     app.run(debug=True)
# from huggingface_hub import InferenceClient
# import pdfplumber
# from flask_sqlalchemy import SQLAlchemy
# from flask import Flask, render_template, request, redirect, url_for, flash, session
# import os

# app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:v4chparuma@localhost:5432/MathHack'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# app.secret_key = 'nokey'

# db = SQLAlchemy(app)

# # Directory where uploaded files will be stored
# UPLOAD_FOLDER = 'static/uploads/'
# app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# # Allowed file extensions
# ALLOWED_EXTENSIONS = {'pdf'}

# # User Authentication Model
# class Authenticate(db.Model):
#     __tablename__ = 'authenticate'

#     id = db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.String(150), nullable=False, unique=True)
#     password = db.Column(db.String(150), nullable=False)

#     def __init__(self, username, password):
#         self.username = username
#         self.password = password

# # Doctors Model
# class Doctor(db.Model):
#     __tablename__ = 'doctors'
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(150), nullable=False)
#     specialty = db.Column(db.String(150), nullable=False)
#     contact = db.Column(db.String(150), nullable=False)

#     def __init__(self, name, specialty, contact):
#         self.name = name
#         self.specialty = specialty
#         self.contact = contact

# # Mails Model
# class Mail(db.Model):
#     __tablename__ = 'mails'
#     id = db.Column(db.Integer, primary_key=True)
#     user_id = db.Column(db.Integer, nullable=False)
#     email = db.Column(db.String(150), nullable=False)

#     def __init__(self, user_id, email):
#         self.user_id = user_id
#         self.email = email

# # Conversation Model
# class Conversation(db.Model):
#     __tablename__ = 'conversations'
#     id = db.Column(db.Integer, primary_key=True)
#     user_id = db.Column(db.Integer, nullable=False)
#     user_message = db.Column(db.Text, nullable=True)
#     bot_message = db.Column(db.Text, nullable=True)
#     pdf_file = db.Column(db.String(150), nullable=True)

#     def __init__(self, user_id, user_message=None, bot_message=None, pdf_file=None):
#         self.user_id = user_id
#         self.user_message = user_message
#         self.bot_message = bot_message
#         self.pdf_file = pdf_file

# def allowed_file(filename):
#     return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# def get_user_id():
#     return session.get('user_id')

# def llm(query):
#     client = InferenceClient(
#         "mistralai/Mistral-Nemo-Instruct-2407",
#         token="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",
#     )
#     a = ""
#     for message in client.chat_completion(
#         messages=[{"role": "system", "content": "You are an expert and experienced from the healthcare and biomedical domain with extensive medical knowledge and practical experience. Your name is OpenBioLLM, and you were developed by Saama AI Labs. who's willing to help answer the user's query with explanation."},
#                   {"role": "user", "content": query}],
#         max_tokens=500,
#         stream=True,
#     ):
#         a += message.choices[0].delta.content
#     return a

# def read_pdf(path):
#     with pdfplumber.open(path) as pdf:
#         text = ""
#         for page in pdf.pages:
#             text += page.extract_text()
#     return text

# def generate_bot_response(user_message):
#     user_id = get_user_id()

#     if '@appointment' in user_message:
#         doctors = Doctor.query.all()
#         if doctors:
#             doctor_list = "\n".join([f"Doctor: {doc.name}, Specialty: {doc.specialty}, Contact: {doc.contact}" for doc in doctors])
#             bot_response = f"Here are the available doctors:\n{doctor_list}\nPlease provide your email to book an appointment."
#         else:
#             bot_response = "Sorry, no doctors are available at the moment."
#         return bot_response

#     conversation = Conversation.query.filter_by(user_id=user_id).filter(Conversation.pdf_file.isnot(None)).order_by(Conversation.id.desc()).first()
#     if conversation and conversation.pdf_file:
#         pdf_path = os.path.join(app.config['UPLOAD_FOLDER'], conversation.pdf_file)
#         pdf_content = read_pdf(pdf_path)
#         full_message = pdf_content + " " + user_message
#     else:
#         full_message = user_message

#     response = llm(full_message)
#     return response

# # Home Page
# @app.route('/')
# def home():
#     return render_template('index.html')

# # User Registration
# @app.route('/register', methods=['GET', 'POST'])
# def register():
#     if request.method == 'POST':
#         username = request.form['username']
#         password = request.form['password']

#         new_user = Authenticate(username=username, password=password)
#         try:
#             db.session.add(new_user)
#             db.session.commit()
#             return redirect(url_for('login'))
#         except Exception as e:
#             return f'There was an issue adding the user: {str(e)}'
#     return render_template('register.html')

# # User Login
# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     if request.method == 'POST':
#         username = request.form['username']
#         password = request.form['password']
#         user = Authenticate.query.filter_by(username=username, password=password).first()

#         if user:
#             session['user_id'] = user.id
#             flash('Login successful')
#             return redirect(url_for('welcome'))
#         else:
#             flash('Invalid username or password')

#     return render_template('login.html')

# # Welcome Page (after login)
# @app.route('/welcome', methods=['GET', 'POST'])
# def welcome():
#     if 'user_id' not in session:
#         flash('Please log in first')
#         return redirect(url_for('login'))

#     user_id = get_user_id()
#     if request.method == 'POST':
#         user_message = request.form['message']
#         file = request.files.get('file')

#         pdf_filename = None
#         if file and allowed_file(file.filename):
#             pdf_filename = file.filename
#             file.save(os.path.join(app.config['UPLOAD_FOLDER'], pdf_filename))

#         if '@appointment' in user_message:
#             bot_message = generate_bot_response(user_message)
#         elif '@email' in user_message:
#             email = user_message.split("@email")[1].strip()
#             if email:
#                 new_mail = Mail(user_id=user_id, email=email)
#                 db.session.add(new_mail)
#                 db.session.commit()
#                 bot_message = "Your email has been saved successfully."
#             else:
#                 bot_message = "Please provide a valid email."
#         else:
#             bot_message = generate_bot_response(user_message)

#         conversation = Conversation(user_id=user_id, user_message=user_message, bot_message=bot_message, pdf_file=pdf_filename)
#         db.session.add(conversation)
#         db.session.commit()

#     conversations = Conversation.query.filter_by(user_id=user_id).all()
#     return render_template('welcome.html', conversations=conversations)

# # Appointment Page
# @app.route('/appointment', methods=['GET', 'POST'])
# def appointment():
#     return render_template("appointment.html")

# # Logout
# @app.route('/logout')
# def logout():
#     session.pop('user_id', None)
#     flash('You have been logged out')
#     return redirect(url_for('login'))

# if __name__ == '__main__':
#     app.run(debug=True)
from huggingface_hub import InferenceClient
import pdfplumber
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, render_template, request, redirect, url_for, flash, session
import os

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:v4chparuma@localhost:5432/MathHack'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'nokey'

db = SQLAlchemy(app)

# Directory where uploaded files will be stored
UPLOAD_FOLDER = 'static/uploads/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Allowed file extensions
ALLOWED_EXTENSIONS = {'pdf'}

# User Authentication Model
class Authenticate(db.Model):
    __tablename__ = 'authenticate'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), nullable=False, unique=True)
    password = db.Column(db.String(150), nullable=False)

    def __init__(self, username, password):
        self.username = username
        self.password = password

# Doctors Model
class Doctor(db.Model):
    __tablename__ = 'doctors'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    specialty = db.Column(db.String(150), nullable=False)
    contact = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(150), nullable=False)
    def __init__(self, name, specialty, contact,email):
        self.name = name
        self.specialty = specialty
        self.contact = contact
        self.email = email
# Mails Model
class Mail(db.Model):
    __tablename__ = 'mails'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    email = db.Column(db.String(150), nullable=False)

    def __init__(self, user_id, email):
        self.user_id = user_id
        self.email = email

# Conversation Model
class Conversation(db.Model):
    __tablename__ = 'conversations'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    user_message = db.Column(db.Text, nullable=True)
    bot_message = db.Column(db.Text, nullable=True)
    pdf_file = db.Column(db.String(150), nullable=True)
    def __init__(self, user_id, user_message=None, bot_message=None, pdf_file=None):
        self.user_id = user_id
        self.user_message = user_message
        self.bot_message = bot_message
        self.pdf_file = pdf_file

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def get_user_id():
    return session.get('user_id')

def llm(query):
    client = InferenceClient(
        "mistralai/Mistral-Nemo-Instruct-2407",
        token="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",
    )
    a = ""
    for message in client.chat_completion(
        messages=[{"role": "system", "content": "You are an expert and experienced from the healthcare and biomedical domain with extensive medical knowledge and practical experience. Your name is OpenBioLLM, and you were developed by Saama AI Labs. who's willing to help answer the user's query with explanation."},
                  {"role": "user", "content": query}],
        max_tokens=500,
        stream=True,
    ):
        a += message.choices[0].delta.content
    return a

def read_pdf(path):
    with pdfplumber.open(path) as pdf:
        text = ""
        for page in pdf.pages:
            text += page.extract_text()
    return text

def generate_bot_response(user_message):
    user_id = get_user_id()

    # Check if the user is asking for an appointment
    if '@appointment' in user_message:
        doctors = Doctor.query.all()
       
        if doctors:
            # Display the list of doctors with their IDs
            doctor_list = "\n".join([f"{doc.email}: Doctor {doc.name}, Specialty: {doc.specialty}, Contact: {doc.contact}" for doc in doctors])
            bot_response = f"Here are the available doctors:\n{doctor_list}\nPlease select a doctor by typing their ID."
        else:
            bot_response = "Sorry, no doctors are available at the moment."
        return bot_response

    # Check if the user selected a doctor by providing a valid ID
    if user_message.isdigit():
        doctor_id = int(user_message)
        selected_doctor = Doctor.query.filter_by(id=doctor_id).first()
        print(selected_doctor.name)

        if selected_doctor:
            # Inform the user of the selected doctor and prompt for email
            bot_response = (f"You have selected Doctor {selected_doctor.name}, Specialty: {selected_doctor.specialty}. "
                            "Please provide your email for appointment booking by typing '@email <your_email>'.")
        else:
            bot_response = "Invalid doctor ID. Please select a valid doctor ID from the list."
        return bot_response

    # Check if the user is providing an email after selecting the doctor
    if '@email' in user_message:
        email = user_message.split("@email")[1].strip()
        if email:
            new_mail = Mail(user_id=user_id, email=email)
            db.session.add(new_mail)
            db.session.commit()
            bot_response = "Your email has been saved successfully. We'll reach out to you for appointment booking."
            # Mail sending code goes here....
        else:
            bot_response = "Please provide a valid email."
        return bot_response

    # If no appointment request, handle normal message response
    conversation = Conversation.query.filter_by(user_id=user_id).filter(Conversation.pdf_file.isnot(None)).order_by(Conversation.id.desc()).first()
    if conversation and conversation.pdf_file:
        pdf_path = os.path.join(app.config['UPLOAD_FOLDER'], conversation.pdf_file)
        pdf_content = read_pdf(pdf_path)
        full_message = pdf_content + " " + user_message
    else:
        full_message = user_message

    # Generate bot response using LLM
    response = llm(full_message)
    return response

# Home Page
@app.route('/')
def home():
    return render_template('index.html')

# User Registration
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        new_user = Authenticate(username=username, password=password)
        try:
            db.session.add(new_user)
            db.session.commit()
            return redirect(url_for('login'))
        except Exception as e:
            return f'There was an issue adding the user: {str(e)}'
    return render_template('register.html')

# User Login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = Authenticate.query.filter_by(username=username, password=password).first()

        if user:
            session['user_id'] = user.id
            flash('Login successful')
            return redirect(url_for('welcome'))
        else:
            flash('Invalid username or password')

    return render_template('login.html')

# Welcome Page (after login)
@app.route('/welcome', methods=['GET', 'POST'])
def welcome():
    if 'user_id' not in session:
        flash('Please log in first')
        return redirect(url_for('login'))

    user_id = get_user_id()
    if request.method == 'POST':
        user_message = request.form['message']
        file = request.files.get('file')

        pdf_filename = None
        if file and allowed_file(file.filename):
            pdf_filename = file.filename
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], pdf_filename))

        if '@appointment' in user_message:
            bot_message = generate_bot_response(user_message)
        elif '@email' in user_message:
            email = user_message.split("@email")[1].strip()
            if email:
                new_mail = Mail(user_id=user_id, email=email)
                db.session.add(new_mail)
                db.session.commit()
                bot_message = "Your email has been saved successfully."
            else:
                bot_message = "Please provide a valid email."
            
        
        else:
            bot_message = generate_bot_response(user_message)
        
        

        conversation = Conversation(user_id=user_id, user_message=user_message, bot_message=bot_message, pdf_file=pdf_filename)
        db.session.add(conversation)
        db.session.commit()

    conversations = Conversation.query.filter_by(user_id=user_id).all()
    return render_template('welcome.html', conversations=conversations)

# Appointment Page
@app.route('/appointment', methods=['GET', 'POST'])
def appointment():
    if request.method == 'POST':
        doctor_name = request.form['doctor']
        reason = request.form['reason']
        appointment_date = request.form['date']
        user_id = get_user_id()
        
        # Here, you would typically save the appointment details to a database
        flash(f"Appointment with Dr. {doctor_name} for {reason} on {appointment_date} has been booked.")
        return redirect(url_for('appointment'))
    
    doctors = Doctor.query.all()
    return render_template("appointment.html", doctors=doctors)

# Logout
@app.route('/logout')
def logout():
    session.pop('user_id', None)
    flash('You have been logged out')
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
