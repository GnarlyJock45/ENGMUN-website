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


@app.route('/committee/<committee_id>')
def committee(committee_id):
    # Fetch committee data based on committee_id
    committee_data = {
        'name': 'DISEC',
        'full_name': 'Disarmament and International Security',
        'level': 'Beginner',
        'delegates': 30,
        'experience': 'Not Required',
        'description': 'Detailed description...',
        'topics': [
            {
                'title': 'Topic 1',
                'description': 'Description of topic 1...'
            },
            # More topics...
        ],
        'resources': [
            {
                'title': 'Study Guide',
                'description': 'Complete guide for delegates',
                'url': '#'
            },
            # More resources...
        ]
    }
    return render_template('committee.html', committee=committee_data)


if __name__ == '__main__':
    app.run(debug=True)
