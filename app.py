import json
import os
from flask import Flask, render_template, redirect, request
from openAI import openai_service

app = Flask(__name__)




@app.route('/')
def hello_world():
    return render_template('home.html')


@app.route('/destination', methods=['POST'])
def handle_redirect():
    return redirect("/destination")


@app.route('/destination')
def destination_page():
    return render_template('subject.html')


# ==========================================
# PHYSICS ROUTE
# ==========================================
@app.route('/physics', methods=['GET', 'POST'])
def physics_page():
    questions_data = []  # Start empty to trigger error/status message if no data

    if request.method == 'POST':
        print("Physics Form Submitted via POST")
        selected_topics = request.form.getlist('topics')
        raw_difficulty = request.form.get('difficulty_val')

        difficulty_map = {"0": "easy", "1": "medium", "2": "hard"}
        difficulty_level = difficulty_map.get(raw_difficulty, "medium")

        if selected_topics:
            # Attempt to generate questions
            questions_data = openai_service.generate_questions_llm("physics", selected_topics, difficulty_level)
        else:
            # Fallback: No topics selected -> Return empty list to trigger error in HTML
            questions_data = []

    else:
        # GET request: Return empty list so user sees the prompt/error instead of old JSON
        questions_data = []

    return render_template('physics.html', questions=questions_data)


# ==========================================
# CHEMISTRY ROUTE
# ==========================================
@app.route('/chemistry', methods=['GET', 'POST'])
def chemistry_page():
    questions_data = []

    if request.method == 'POST':
        print("Chemistry Form Submitted via POST")
        selected_topics = request.form.getlist('topics')
        raw_difficulty = request.form.get('difficulty_val')

        difficulty_map = {"0": "easy", "1": "medium", "2": "hard"}
        difficulty_level = difficulty_map.get(raw_difficulty, "medium")

        if selected_topics:
            questions_data = openai_service.generate_questions_llm("chemistry", selected_topics, difficulty_level)
        else:
            # Fallback: Return empty to trigger HTML error
            questions_data = []

    else:
        # GET request: Start empty
        questions_data = []

    return render_template('chemistry.html', questions=questions_data)


# ==========================================
# MATH ROUTE
# ==========================================
@app.route('/math', methods=['GET', 'POST'])
def math_page():
    questions_data = []

    if request.method == 'POST':
        print("Math Form Submitted via POST")
        selected_topics = request.form.getlist('topics')
        raw_difficulty = request.form.get('difficulty_val')

        difficulty_map = {"0": "easy", "1": "medium", "2": "hard"}
        difficulty_level = difficulty_map.get(raw_difficulty, "medium")

        if selected_topics:
            questions_data = openai_service.generate_questions_llm("math", selected_topics, difficulty_level)
        else:
            # Fallback: Return empty to trigger HTML error
            questions_data = []

    else:
        # GET request: Start empty
        questions_data = []

    return render_template('math.html', questions=questions_data)


if __name__ == '__main__':
    app.run(port=5001, debug=False)