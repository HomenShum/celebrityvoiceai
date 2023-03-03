from datetime import datetime
from flask import Blueprint, render_template, request, flash
from flask_login import login_required, current_user
from .models import Note, Persona
from . import db
import json
from flask import jsonify
from .chatbot_nelson_mandela import respond_user

views = Blueprint('views', __name__)


@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    return render_template("home.html", user=current_user)


@views.route('/delete-note', methods=['POST'])
def delete_note():
    note = json.loads(request.data)  # request.data is the json object
    noteId = note['noteId']  # noteId is the key in the json object
    note = Note.query.get(noteId)  # get the note from the database
    if note:  # if the note exists
        if note.user_id == current_user.id:  # if the note belongs to the current user
            db.session.delete(note)  # delete the note
            db.session.commit()  # commit changes to database

    return jsonify({})  # return an empty json object


@views.route('/delete-all-notes', methods=['POST'])
def delete_all_notes():
    # get all notes belonging to the current user
    notes = Note.query.filter_by(user_id=current_user.id).all()
    for note in notes:  # loop through each note
        db.session.delete(note)  # delete the note
    db.session.commit()  # commit changes to database
    return jsonify({})  # return an empty json object


@views.route('/select', methods=['GET', 'POST'])
@login_required
def select_persona():
    personas = Persona.query.all()
    selected_persona = None
    if request.method == 'POST':
        current_user.email = request.form.get('email')
        persona_id = request.form.get('selected_persona')
        selected_persona = Persona.query.filter_by(name=persona_id).first()
        current_user.persona = selected_persona
        db.session.commit()
    return render_template("select_persona.html", personas=personas, user=current_user, selectedPersona=selected_persona)

@views.route('/NelsonMandelaChat', methods=['GET', 'POST'])
@login_required
def nelson_mandela():
    if request.method == 'POST':
        note = request.form.get('note')

        if note is None or len(note) < 1:
            flash('Message is too short!', category='error')
        elif len(note) > 500:
            flash('Message is too long!', category='error')
        else: # submit user's note to the database and display it on the page
            date = datetime.now().strftime("%m/%d/%Y %H:%M:%S")
            new_note = Note(
                data=f"{date} {current_user.first_name}: {note}", user_id=current_user.id)
            db.session.add(new_note)
            db.session.commit()
            flash('Message sent! Please wait for your reply ~ 45 seconds', category='success')
        # then show response to user in the following:
        # -> extends from chatbot.py file 
            response = respond_user(note)
            new_note_response = Note(
                data=f"{date} Nelson Mandela: {response}", user_id=current_user.id)
            db.session.add(new_note_response)
            db.session.commit()
    return render_template("nelson_mandela.html", user=current_user)

@views.route('/AITutoring', methods=['GET', 'POST'])
@login_required
def AI_tutor():
    if request.method == 'POST':
        note = request.form.get('note')

        if note is None or len(note) < 1:
            flash('Message is too short!', category='error')
        elif len(note) > 500:
            flash('Message is too long!', category='error')
        else: # submit user's note to the database and display it on the page
            date = datetime.now().strftime("%m/%d/%Y %H:%M:%S")
            new_note = Note(
                data=f"{date} {current_user.first_name}: {note}", user_id=current_user.id)
            db.session.add(new_note)
            db.session.commit()
            flash('Message sent! Please wait for your reply ~ 30 seconds', category='success')
        # then show response to user in the following:
        # -> extends from chatbot.py file 
            response = respond_user(note)
            new_note_response = Note(
                data=f"{date} Nelson Mandela: {response}", user_id=current_user.id)
            db.session.add(new_note_response)
            db.session.commit()
    return render_template("persona_tutor.html", user=current_user)

@views.route('/textextraction', methods=['GET', 'POST'])
@login_required
def text_extraction():
    return render_template("text_extraction.html", user=current_user)
