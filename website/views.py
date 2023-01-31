from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from .models import Note
from . import db
import json
from flask import jsonify

views = Blueprint('views', __name__)

@views.route('/', methods=['GET', 'POST']) 
@login_required
def home():
    if request.method == 'POST':
        note = request.form.get('note')
        
        if len(note) < 1:
            flash('Note is too short!', category='error')
        else:
            new_note = Note(data=note, user_id=current_user.id)
            db.session.add(new_note)
            db.session.commit()
            flash('Note added!', category='success')
    return render_template("home.html", user=current_user)

@views.route('/delete-note', methods=['POST'])
def delete_note():
    note = json.loads(request.data) #request.data is the json object
    noteId = note['noteId'] #noteId is the key in the json object
    note = Note.query.get(noteId) #get the note from the database
    if note: #if the note exists
        if note.user_id == current_user.id: #if the note belongs to the current user
            db.session.delete(note) #delete the note
            db.session.commit() #commit changes to database
    
    return jsonify({}) #return an empty json object
