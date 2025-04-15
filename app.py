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
                return json.load(f)
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
        flashcards.append({'question': question, 'answer': answer})
        save_flashcards(flashcards)
        return redirect(url_for('index'))
    return render_template('add.html')

@app.route('/quiz')
def quiz():
    flashcards = load_flashcards()
    if flashcards:
        card = random.choice(flashcards)
        return render_template('quiz.html', card=card)
    return "<h2>No flashcards available. <a href='/add'>Add some</a></h2>"

@app.route('/delete/<int:card_index>', methods=['POST'])
def delete(card_index):
    flashcards = load_flashcards()
    print("flashcards type:", type(flashcards))  
    if 0 <= card_index < len(flashcards):
        del flashcards[card_index]
        save_flashcards(flashcards)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
