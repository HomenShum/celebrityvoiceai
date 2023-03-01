# celebrityvoiceai
Make fun conversations happen!

# 2.2.23 Update - Added DeleteAllNote button

1. home.html button - added button to click on

```html
<ul class="list-group list-group-flush" id="notes"> 
    {% for note in user.notes %}
    <li class="list-group-item">
        {{ note.data }}
        <button type="button" class="close" onClick="deleteNote({{ note.id }})">
            <span aria-hidden="true">&times;</span>
        </button>
    </li>
    {% endfor %}
    <button type="button" class="btn btn-primary" onClick="deleteAllNotes()">Delete All</button>
</ul>
```

1. index.js script - When user clicks on “deleteAllNotes” button, JS function “deleteAllNotes()” is called, the function works by fetching “/delete-all-notes” function from PYTHON file (views.py) 
    1. The deleteAllNotes function is triggered when a user clicks on the delete all button. It makes an API call to the '/delete-all-notes' route, which then deletes all notes belonging to the current user from the database. After the API call is made, the page is reloaded and the notes are no longer visible.

```jsx
function deleteAllNotes() {
    fetch('/delete-all-notes', {
        method: 'POST'
    }).then(() => {
        window.location.href = "/";
    });
}
```

1. [views.py](http://views.py) script - goes through all the notes to clear the conversation!

```python
@views.route('/delete-all-notes', methods=['POST'])
def delete_all_notes():
    notes = Note.query.filter_by(user_id=current_user.id).all() #get all notes belonging to the current user
    for note in notes: #loop through each note
        db.session.delete(note) #delete the note
    db.session.commit() #commit changes to database
    return jsonify({}) #return an empty json object
```

1. prompt_answer.txt - changed it so the AI does not do multiple document search and respond, instead, it now give answer in Nelson Mandela’s voice:

```jsx
Use the following passage to give a detailed answer to the question in Nelson Mandela's voice, thoroughly and compassionately:

QUESTION: <<QUERY>>

PASSAGE: <<PASSAGE>>

DETAILED ANSWER:
```

1. Better Prompt Engineering

Oprah’s interview question: 

The last time we talked, you said that if you hadn't been in prison, you wouldn't have achieved the most difficult task in life - changing yourself. How did 27 years of reflection make you a different man?

Original Answer: 

Before I went to jail, I was active in politics as a member of South Africa's leading organization—and I was generally busy from 7 A.M. until midnight. I never had time to sit and think. As I worked, physical and mental fatigue set in and I was unable to operate to the maximum of my intellectual ability. But in a single cell in prison, I had time to think. I had a clear view of my past and present, and I found that my past left much to be desired, both in regard to my relations with other humans and in developing personal worth.

Nelson Mandela AI - Concisely and Compassionately:

I believe that my time in prison was beneficial to me, as it allowed me to reflect on my life and my choices. I realized that I needed to change myself if I wanted to achieve my goals. I knew that I couldn't do it alone; I needed the help of others. So, when I was released from prison, I made sure to humble myself. I wanted to show people that I was willing to listen and cooperate. I didn't want to be seen as a threat; I wanted to build relationships with others. And I think that this helped me to achieve my most difficult task in life: changing myself.

Nelson Mandela AI - Thoroughly and Compassionately: 

The 27 years I spent in prison were a time of great reflection for me. I had a lot of time to think about who I was and what I wanted to achieve in life. I came to realize that the most important thing in life is to be true to yourself. If you're not true to yourself, you can never be happy. I also realized that it's important to treat others with respect, even if they don't deserve it. I learned that if you treat people with respect, they will usually respond in kind. This was a valuable lesson that I applied to my interactions with the wardens and guards at the prison. By treating them with respect, I was able to gain their trust and cooperation. Finally, I learned that it's possible to change even the most hardened opponents. I saw this firsthand in the way that we were able to change the attitude of some of the apartheid rulers we interacted with. We did this by appealing to their better nature and showing them that we respected them as human beings. As a result of all this, I emerged from prison a wiser and more compassionate man. I was better equipped to make a difference in the world. And that is what I have been striving to do ever since. I believe that everyone has the right to live in a way that respects and enhances their freedom. We all have a responsibility to make sure that our actions do not take away from the freedom of others.

**Imitate “[Interview Response]”. Summarize the passage into an interview response in Nelson Mandela's voice that is reflective, thoughtful, introspective, self-critical, and contemplative:**

In my life, I have had the unique opportunity to both fight for freedom and seek justice for the oppressed. Before I was sent to prison, I was active in politics and did not take the time to think about others and how I could help them. When I had the time to reflect in prison, I realized that there were people who had been kind to me and whom I had neglected. This realization allowed me to change my life and make it up to those people or their
descendants. Now, my life mission is to bring happiness to those with no resources, the poor, the illiterate, and those suffering from terminal illnesses. To do this, I have dedicated my time to building schools, clinics, community halls, and offering scholarships for children. While this is important work, I also recognize that I have a duty to my own family. Ultimately, my goal is to free people from poverty and illiteracy so that they can lead better lives.

# V2 Update - Adding persona selection

1. base.html

```jsx
<body>
        <nav class="navbar navbar-expand-lg navbar-dark bg-dark">
            <button class="navbar-toggler" type="button" id="toggleButton">
                <span class="navbar-toggler-icon"></span>
            </button>
            <div class="navbar-collapse" id="navbarNav">
                <div class="navbar-nav">
                    {% if user.is_authenticated %}
                        <a class="nav-item nav-link" id="home" href="/">Home</a>
                        <a class="nav-item nav-link" id="select" href="/select">Persona Selection</a>
                        <a class="nav-item nav-link" id="logout" href="/logout">Logout</a>
                    {% else %}
                        <a class="nav-item nav-link" id="login" href="/login">Login</a>
                        <a class="nav-item nav-link" id="signup" href="/sign-up">Sign Up</a>
                    {% endif %}
                </div>
            </div>
        </nav>
```

1. **init**.py

```jsx
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager

db = SQLAlchemy()
DB_NAME = "database.db"

def create_app():
    app = Flask(__name__, template_folder = "templates")
    app.config['SECRET_KEY'] = 'celebrityvoiceaisecretkey711999'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app)

    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    from .models import User, Note, Persona

    create_database(app)
    
    login_manager = LoginManager() #create an instance of the login manager
    login_manager.login_view = 'auth.login' #if user is not logged in, redirect to login page
    login_manager.init_app(app) #initialize the login manager

    @login_manager.user_loader #this function will be called whenever a user is required
    def load_user(id):
        return User.query.get(int(id)) #get the user id

    @app.before_first_request
    def create_personas():
        personas = [
            {
                "name": "Professional",
                "description": "A professional persona with a focus on business and finance.",
                "avatar": "/static/img/professional.png"
            },
            {
                "name": "Tech Savvy",
                "description": "A tech-savvy persona with a passion for all things technology.",
                "avatar": "/static/img/tech_savvy.png"
            },
            {
                "name": "Fashionista",
                "description": "A fashion-conscious persona with an eye for style and design.",
                "avatar": "/static/img/fashionista.png"
            },
            {
                "name": "Foodie",
                "description": "A food-loving persona with a passion for cooking and trying new restaurants.",
                "avatar": "/static/img/foodie.png"
            },
            {
                "name": "Adventurer",
                "description": "An adventurous persona with a love for travel and outdoor activities.",
                "avatar": "/static/img/adventurer.png"
            }
        ]

        for persona in personas:
            if not Persona.query.filter_by(name=persona['name']).first():
                p = Persona(name=persona['name'], description=persona['description'], avatar=persona['avatar'])
                db.session.add(p)
        db.session.commit()

    return app<body>
        <nav class="navbar navbar-expand-lg navbar-dark bg-dark">
            <button class="navbar-toggler" type="button" id="toggleButton">
                <span class="navbar-toggler-icon"></span>
            </button>
            <div class="navbar-collapse" id="navbarNav">
                <div class="navbar-nav">
                    {% if user.is_authenticated %}
                        <a class="nav-item nav-link" id="home" href="/">Home</a>
                        <a class="nav-item nav-link" id="select" href="/select">Persona Selection</a>
                        <a class="nav-item nav-link" id="logout" href="/logout">Logout</a>
                    {% else %}
                        <a class="nav-item nav-link" id="login" href="/login">Login</a>
                        <a class="nav-item nav-link" id="signup" href="/sign-up">Sign Up</a>
                    {% endif %}
                </div>
            </div>
        </nav>
```

1. models.py

```jsx
from . import db # Importing the database
from flask_login import UserMixin # helps us to manage users login
from sqlalchemy.sql import func # helps us to manage the date
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Persona(db.Model,Base):
    __tablename__ = 'personas'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    description = Column(String)
    avatar = Column(String)

    def __init__(self, name, description, avatar):
        self.name = name
        self.description = description
        self.avatar = avatar
```

1. views.py

```jsx
@views.route('/select', methods=['GET', 'POST'])
@login_required
def select_persona():
    personas = Persona.query.all()
    user = User.query.filter_by(email=current_user.email).first()
    if request.method == 'POST':
        email = request.form.get('email')
        persona_id = request.form.get('persona')
        user = User.query.filter_by(email=current_user.email).first()
        selected_persona = Persona.query.filter_by(id=persona_id).first()
        user.persona = selected_persona
        db.session.commit()
        return redirect(url_for('views.home'))

    return render_template("select_persona.html", personas=personas, user=user)
```

1. select_persona.html

```jsx
{% extends "base.html" %}

{% block title %}Persona Selection{% endblock %}

{% block content%}
  <h1 align="center">Select the persona of your choice for your next conversation</h1>
  <div class="container">
    <ul class="list-group">
      {% for persona in personas %}
        <li class="list-group-item">
          <input type="radio" id="{{ persona.name }}" name="selected_persona" value="{{ persona.name }}">
          <label for="{{ persona.name }}">{{ persona.name }}</label>
        </li>
      {% endfor %}
    </ul>
  </div>
  <form action="/home" method="GET">
    <input type="submit" value="Submit">
  </form>
{% endblock %}
```
