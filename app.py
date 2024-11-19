from flask import Flask, render_template, abort, request
from flask_babel import Babel, gettext as _

import json
import os

app = Flask(__name__)

# Configure Babel
app.config['BABEL_DEFAULT_LOCALE'] = 'en'
app.config['BABEL_SUPPORTED_LOCALES'] = ['en', 'ar']
app.config['BABEL_DEFAULT_TIMEZONE'] = 'UTC'

babel = Babel()

# Locale selector function
def locale_selector():
    return request.args.get('lang', 'en')

# Initialize Babel with the app and selector
babel.init_app(app, locale_selector=locale_selector)

# Load committee data once when the app starts
def load_committees():
    data_file = os.path.join(app.root_path, 'data', 'committees.json')
    with open(data_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    committees = {committee['id']: committee for committee in data.get('committees', [])}
    return committees

committees = load_committees()

# Function to load team members data
def load_team_members():
    data_file = os.path.join(app.root_path, 'data', 'team_members.json')
    try:
        with open(data_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        team_members_dict = {member['id']: member for member in data.get('team_members', [])}
        return team_members_dict
    except FileNotFoundError:
        print(f"Error: {data_file} not found.")
        return {}
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")
        return {}

team_members = load_team_members()


@app.route('/')
def home():
    return render_template('home.html', title=_('Home'), committees=committees)

@app.route('/concert')
def concert():
    return render_template('concert.html', title=_('Concert Details'))

@app.route('/team')
def team():
    return render_template('team.html', title=_('Our Team'), team_members=team_members)

@app.route('/contact')
def contact():
    return render_template('contact.html', title=_('Contact Us'))

@app.route('/committee/<committee_id>')
def committee(committee_id):
    committee_data = committees.get(committee_id)
    if not committee_data:
        abort(404)  # Committee not found
    return render_template('committee.html', committee=committee_data)


if __name__ == '__main__':
    app.run(debug=True)
