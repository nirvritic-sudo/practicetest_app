from flask import Flask, render_template, request, redirect, url_for, session
import os
import json

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')
#subject page
@app.route('/subject', methods=['POST'])
def subject_redirect():
    print("redirecting to subject")
    return redirect("/subject")
@app.route('/subject')
def subject_page():
    return render_template('subject.html')

#load questions

def load_questions_physics():
    """A helper function to load questions from the JSON file."""
    json_file_path = os.path.join(app.root_path, 'sample_physics_questions.json')
    with open(json_file_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def load_questions_math():
    """A helper function to load questions from the JSON file."""
    json_file_path = os.path.join(app.root_path, 'sample_math_questions.json')
    with open(json_file_path, 'r', encoding='utf-8') as f:
        return json.load(f)
def load_questions_chemistry():
    """A helper function to load questions from the JSON file."""
    json_file_path = os.path.join(app.root_path, 'sample_chemistry_questions.json')
    with open(json_file_path, 'r', encoding='utf-8') as f:
        return json.load(f)


#math page
@app.route('/math', methods=['POST'])
def math_redirect():
    print("redirecting to math")
    return redirect("/math")
@app.route('/math')
def math_page():
    questions = load_questions_math()
    return render_template('math.html',questions=questions)
#physics page
@app.route('/physics', methods=['POST'])
def physics_redirect():
    print("redirecting to physics")
    return redirect("/physics")
@app.route('/physics')
def physics_page():
    questions = load_questions_physics()
    return render_template('physics.html', questions=questions)
#chemistry page
@app.route('/chemistry', methods=['POST'])
def chemistry_redirect():
    print("redirecting to chemistry")
    return redirect("/chemistry")
@app.route('/chemistry')
def chemistry_page():
    questions = load_questions_chemistry()
    return render_template('chemistry.html',questions=questions)

if __name__ == '__main__':
    app.run()

