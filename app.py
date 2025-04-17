from flask import Flask, render_template, request, redirect, url_for
import json
import random
import os

app = Flask(__name__)
FLASHCARD_FILE = 'flashcards.json'

def load_flashcards():
    if os.path.exists(FLASHCARD_FILE):
        with open(FLASHCARD_FILE, 'r') as f:
            try:
                data = json.load(f)
                # 🔁 If data is in old dictionary format, convert to list
                if isinstance(data, dict):
                    return [{"question": q, "answer": a} for q, a in data.items()]
                return data
            except json.JSONDecodeError:
                return []
    return []

def save_flashcards(data):
    with open(FLASHCARD_FILE, 'w') as f:
        json.dump(data, f, indent=4)

@app.route('/')
def index():
    flashcards = load_flashcards()
    return render_template('index.html', flashcards=flashcards)

@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        question = request.form['question']
        answer = request.form['answer']
        flashcards = load_flashcards()
        # 🔁 If old format, convert to list first
        if isinstance(flashcards, dict):
            flashcards = [{"question": q, "answer": a} for q, a in flashcards.items()]
        flashcards.append({'question': question, 'answer': answer})
        save_flashcards(flashcards)
        return redirect(url_for('index'))
    return render_template('add.html')

@app.route('/quiz')
def quiz():
    flashcards = load_flashcards()
    if flashcards:
        card = random.choice(flashcards)
        print(f"Card loaded: {card}")  # Add this line to debug
        return render_template('quiz.html', card=card)
    return "<h2>No flashcards available. <a href='/add'>Add some</a></h2>"

if __name__ == '__main__':
    app.run(debug=True)

