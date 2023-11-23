# Imports modules from packages
from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .models import Note
from . import db
import json

# Creates a Blueprint named 'views'
views = Blueprint('views', __name__)

# Route for the home page using GET and POST methods
@views.route('/', methods=['GET', 'POST'])
@login_required  # Requires the user to be logged in
def home():
    if request.method == 'POST':
        note = request.form.get('note')
        if len(note) < 1:
            flash('Note is too short!', category='error')
        else:
            # Creates a new Note and associate it with the current user
            new_note = Note(data=note, user_id=current_user.id)
            db.session.add(new_note)
            db.session.commit()
            flash('Note added!', category='success')
    # Renders the home template with the current user context
    return render_template("home.html", user=current_user)

# Route to delete a note using POST method
@views.route('/delete-note', methods=['POST'])
def delete_note():
    note = json.loads(request.data)
    noteId = note['noteId']
    note = Note.query.get(noteId)
    if note:
        if note.user_id == current_user.id:
            # Deletes the note if it belongs to the current user
            db.session.delete(note)
            db.session.commit()
    return jsonify({})

# Route to update/edit a note using POST method
@views.route('/update-note', methods=['POST'])
def edit_note():
    note_data = json.loads(request.data)
    note_id = note_data['noteId']
    new_data = note_data['newData']
    note = Note.query.get(note_id)
    if note:
        if note.user_id == current_user.id:
            # Updates the note data if it belongs to the current user
            note.data = new_data
            db.session.commit()
    return jsonify({})