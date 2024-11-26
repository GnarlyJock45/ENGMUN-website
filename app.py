from flask import Flask, render_template, abort, request, url_for, redirect
from flask_babel import Babel, gettext as _



import os
import json


app = Flask(__name__)

# Configure Babel
app.config['BABEL_DEFAULT_LOCALE'] = 'ar'  # Set default locale to Arabic
app.config['BABEL_SUPPORTED_LOCALES'] = ['en', 'ar']
app.config['BABEL_DEFAULT_TIMEZONE'] = 'UTC'

babel = Babel()

# Locale selector function
def locale_selector():
    lang = request.args.get('lang')
    if lang in app.config['BABEL_SUPPORTED_LOCALES']:
        return lang
    return app.config['BABEL_DEFAULT_LOCALE']  # Default to Arabic

# Initialize Babel with the app and selector
babel.init_app(app, locale_selector=locale_selector)

@app.context_processor
def inject_lang():
    return {'current_lang': locale_selector()}

@app.context_processor
def inject_committees():
    committees = load_committees()
    return dict(committees=committees)


# Load committee data once when the app starts
def load_committees():
    lang = locale_selector()
    filename = f'committees_{lang}.json'
    filepath = os.path.join(app.root_path, 'data', filename)
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        # Convert the list of committees to a dictionary keyed by 'id'
        committees_dict = {committee['id']: committee for committee in data['committees']}
        return committees_dict
    except FileNotFoundError:
        # Fallback to default language if file not found
        default_filepath = os.path.join(app.root_path, 'data', 'committees_en.json')
        with open(default_filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        committees_dict = {committee['id']: committee for committee in data['committees']}
        return committees_dict


# Function to load team members data
def load_team_members():
    lang = locale_selector()
    filename = f'team_members_{lang}.json'
    filepath = os.path.join(app.root_path, 'data', filename)
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        team_members_dict = {member['id']: member for member in data['team_members']}
        return team_members_dict
    except FileNotFoundError:
        # Fallback to default language if file not found
        default_filepath = os.path.join(app.root_path, 'data', 'team_members_en.json')
        with open(default_filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        team_members_dict = {member['id']: member for member in data['team_members']}
        return team_members_dict


@app.route('/')
def home():
    committees = load_committees()
    return render_template('home.html', title=_('Home'))

@app.route('/concert')
def concert():
    return render_template('concert.html', title=_('Event Details'))

@app.route('/team')
def team():
    team_members = load_team_members()
    return render_template('team.html', title=_('Executive Team'), team_members=team_members)



@app.route('/committee/<committee_id>')
def committee(committee_id):
    committees = load_committees()
    committee_data = committees.get(committee_id)
    if not committee_data:
        abort(404)  # Committee not found
    return render_template('committee.html',title=_('Committee'), committee=committee_data)


# Optional: Redirect to default language if no 'lang' parameter
@app.before_request
def ensure_lang_in_url():
    if 'lang' not in request.args and request.endpoint == 'home':
        return redirect(url_for('home', lang=app.config['BABEL_DEFAULT_LOCALE']))
    

@app.context_processor
def override_url_for():
    return dict(url_for=dated_url_for)

def dated_url_for(endpoint, **values):
    if endpoint == 'static':
        filename = values.get('filename', None)
        if filename:
            file_path = os.path.join(app.root_path,
                                   endpoint, filename)
            values['q'] = int(os.stat(file_path).st_mtime)
    return url_for(endpoint, **values)


if __name__ == '__main__':
    app.run()
