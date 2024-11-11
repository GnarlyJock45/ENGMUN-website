# app.py
from flask import Flask, render_template, url_for

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html', title='Home')

@app.route('/concert')
def concert():
    return render_template('concert.html', title='Concert Details')

@app.route('/team')
def team():
    return render_template('team.html', title='Our Team')

@app.route('/contact')
def contact():
    return render_template('contact.html', title='Contact Us')

if __name__ == '__main__':
    app.run(debug=True)
