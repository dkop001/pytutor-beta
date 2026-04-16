from flask import Flask, render_template, request, jsonify, redirect, url_for, session
import database
import os
import uuid
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)
app.secret_key = os.urandom(24) # Vital for Flask sessions
database.init_db(app)

from data import mock_lessons, get_user_units

def get_current_user():
    """Helper to fetch the current user's session data via abstract database"""
    if 'user_id' not in session:
        # Give visitors a temporary unique ID
        session['user_id'] = str(uuid.uuid4())
    return database.get_user(session['user_id'])

@app.route('/')
def index():
    user = get_current_user()
    user_units = get_user_units(user)
    return render_template('index.html', user=user, units=user_units)

@app.route('/notes')
def notes():
    return render_template('notes.html')

@app.route('/lesson/<int:lesson_id>')
def lesson(lesson_id):
    if lesson_id not in mock_lessons:
        return redirect(url_for('index'))
    
    user = get_current_user()
    question_idx = int(request.args.get('q', 0))
    lesson_data = mock_lessons[lesson_id]
    questions = lesson_data['questions']
    
    if question_idx >= len(questions):
        return redirect(url_for('index'))
        
    progress = question_idx / len(questions)
    question = questions[question_idx]
    options_with_idx = list(enumerate(question['options']))
    
    return render_template('lesson.html', 
                           user=user, 
                           lesson=lesson_data, 
                           question=question,
                           question_idx=question_idx,
                           progress=progress,
                           options_with_idx=options_with_idx)

@app.route('/api/check_answer', methods=['POST'])
def check_answer():
    if 'user_id' not in session:
        return jsonify({"error": "Unauthorized"}), 401
        
    user_id = session['user_id']
    user = database.get_user(user_id)
    
    req_data = request.get_json()
    lesson_id = req_data.get('lesson_id')
    question_idx = int(req_data.get('question_idx', 0))
    answer_idx = int(req_data.get('answer_id'))
    
    lesson_data = mock_lessons.get(lesson_id)
    if not lesson_data:
        return jsonify({"error": "Lesson not found"}), 404
        
    question = lesson_data['questions'][question_idx]
    correct = (answer_idx == question['correct_option_idx'])
    correct_text = question['options'][question['correct_option_idx']]
    
    next_url = url_for('index')
    is_lesson_complete = False
    
    # Store pending updates.
    # We do a deep update to mock the Supabase .update() cycle
    updated_fields = {}
    
    if correct:
        updated_fields['xp'] = user['xp'] + 15
        
        if question_idx + 1 < len(lesson_data['questions']):
            next_url = url_for('lesson', lesson_id=lesson_id, q=question_idx+1)
        else:
            is_lesson_complete = True
            
            # Safe append handling
            completed = list(user['completed_lessons'])
            if lesson_id not in completed:
                completed.append(lesson_id)
                updated_fields['completed_lessons'] = completed
                
                next_lesson = lesson_id + 1
                if next_lesson in mock_lessons:
                    updated_fields['current_lesson_id'] = next_lesson
                    
            next_url = url_for('index')
    else:
        updated_fields['hearts'] = max(0, user['hearts'] - 1)
        
    if updated_fields:
        database.update_user(user_id, updated_fields)
        # Fetch fresh data right after update
        user = database.get_user(user_id)

    return jsonify({
        "correct": correct,
        "correct_answer_text": correct_text,
        "explanation": question['explanation'],
        "xp": user["xp"],
        "hearts": user["hearts"],
        "next_url": next_url,
        "is_lesson_complete": is_lesson_complete
    })

if __name__ == '__main__':
    app.run(debug=True, port=5000)
